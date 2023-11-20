import pandas as pd
import re
import nlptutti as metrics

# 경우의 수 나누는 함수들
## 이중전사
def check_list(text_list):
    for text in text_list:
        pattern = r'\((.*?)\)/\((.*?)\)'
        match = re.search(pattern, text)
        if match!=None:
            condition=True
            break
        else:
            condition=False
    return condition
        
def make_combi(text_list):
    answer=[]
    
    for text in text_list:
        pattern = r'\((.*?)\)/\((.*?)\)'
        p = re.compile('\(([^)]+)')
        match = re.search(pattern, text)
        try:
            start, end = match.span()
            target=text[start:end]
            m = p.findall(target)
            
            for word in m:
                tmp=text.replace(target, word)
                answer.append(tmp)
        except:
            pass
    return answer


## 단순 괄호
def check_one(text_list):
    for text in text_list:
        pattern = re.compile('\([^)]+\)')
        match = re.search(pattern, text)
        if match!=None:
            condition=True
            break
        else:
            condition=False
    return condition

def remove_gwual_text(text_list):
    answer=[]
    
    for text in text_list:
        pattern = r'\((.*?)\)'
        match = re.search(pattern, text)
        try:
            start, end = match.span()
            target=text[start:end]
            modi_word=target[1:-1]
            
            tmp=text.replace(target, "") # 괄호 속 내용을 아예 없앨때
            answer.append(tmp)
            
            tmp=text.replace(target, modi_word) # 괄호 속 내용을 포함할때
            answer.append(tmp)
        except:
            pass        
    return answer


## 플러스
def check_plus(text_list):
    for text in text_list:
        pattern = r"\b\w+\+"
        match = re.search(pattern, text)
        if match!=None:
            condition=True
            break
        else:
            condition=False
    return condition

def remove_plus(text_list):
    answer=[]
    
    for text in text_list:
        pattern = r"\b\w+\+"
        match = re.search(pattern, text)
        try:
            start, end = match.span()
            target=text[start:end]
            modi_word=target.replace('+','')
            
            tmp=text.replace(target, "") # 괄호 속 내용을 아예 없앨때
            answer.append(tmp)
            
            tmp=text.replace(target, modi_word) # 괄호 속 내용을 포함할때
            answer.append(tmp)
        except:
            pass        
    return answer


# 데이터프레임 전처리 함수
def make_modified(df):
    modified_answer=[]
    for i in range(len(df)):
        file_name=df.iloc[i, 0]
        answer_text=df.iloc[i, 1]
        stt_text=df.iloc[i, -2]

        # o/, n/, l/, b/ 전처리
        answer_text = answer_text.replace('o/', ' ').replace('l/', ' ').replace('b/', ' ').replace('n/', ' ').replace("  ", " ")
        answer_text=answer_text.replace("(())", "")
        answer_text=answer_text.strip()

        # 경우의 수 계산
        text_list=[]
        text_list.append(answer_text)
        condition=check_list(text_list) # 이중전사
        while condition==True:    
            text_list=make_combi(text_list)
            condition=check_list(text_list)
        condition=check_one(text_list) # 단일 괄호 경우의 수 조합
        while condition==True:    
            text_list=remove_gwual_text(text_list)
            condition=check_one(text_list)
        condition=check_plus(text_list) # 플러스 경우의 수 조합
        while condition==True:    
            text_list=remove_plus(text_list)
            condition=check_plus(text_list)

        for text in text_list:
            text=text.replace("  ", " ")
            modified_answer.append([file_name, answer_text, text, stt_text])
    modified_df=pd.DataFrame(modified_answer, columns=['file_name', 'answer_text','modified_text', 'recognized_text'])
    return modified_df

# CER, WER 계산
def get_cerwer(df, modified_df):
    modified_df['cer']=0
    modified_df['wer']=0
    for i in range(len(modified_df)):
        refs=modified_df.iloc[i,2]
        preds=modified_df.iloc[i,3]
        result = metrics.get_cer(refs, preds)
        cer = result['cer']
        result_wer=metrics.get_wer(refs, preds)
        wer=result_wer['wer']
        modified_df.iloc[i, 4]=cer
        modified_df.iloc[i, 5]=wer
        # 그룹별 최솟값 계산
    min_indices = modified_df.groupby(['file_name', 'answer_text'])[['cer', 'wer']].idxmin()
    # 최솟값을 가진 행들 가져오기
    tmp = modified_df.loc[min_indices['cer']]
    tmp.drop(columns=['recognized_text', 'answer_text'], axis=1, inplace=True)
    total=pd.merge(df, tmp, how='inner', on='file_name')
    return total