import pandas as pd
from eng_STT_API import naver_stt, azure_stt, google_stt, whisper_stt

predict_path='predict/english/'
data_path='data/'

# sample txt 파일 불러오기
dataset=input("데이터 선택 입력해주세요: (1, 2, 3, 4 택1) ")
if dataset=="1":
    predict=predict_path+'1_'
    loaded_list=list(pd.read_csv(data_path+"common voice/sample/sample.csv")['filename'])
elif dataset=="2":
    with open(data_path+"2_VCTK-Corpus/sample.txt", 'r') as file:
        # 파일의 각 줄을 읽어와 리스트에 저장
        loaded_list = [line.strip() for line in file.readlines()]
    predict=predict_path+'2_'
elif dataset=="3":
    predict=predict_path+'3_'
    loaded_list=list(pd.read_csv(data_path+"3_CMU/sample.csv")["file_path"])
elif dataset=="4":
    predict=predict_path+'4_'
    loaded_list=list(pd.read_csv(data_path+"4_IEMOCAP/sample.csv")["titre"])
else:
    print("틀렸습니다. 이 파일을 재실행해주세요")

## 예측
model=input("모델 선택 입력해주세요: (naver, azure, google, whisper 택1) ")
if model=="naver":
    # 예측
    pdf=naver_stt(loaded_list, dataset)

    # 저장
    predict=predict+'naver.csv'
    pdf.to_csv(predict, index=False)

elif model=="azure":
    # 예측
    pdf=azure_stt(loaded_list, dataset)

    # 저장
    predict=predict+'azure.csv'
    pdf.to_csv(predict, index=False)

elif model=="google":
    # 예측
    pdf=google_stt(loaded_list, dataset)

    # 저장
    predict=predict+'google.csv'
    pdf.to_csv(predict, index=False)

elif model=="whisper":
    # 예측
    pdf=whisper_stt(loaded_list, dataset)

    # 저장
    predict=predict+'whisper.csv'
    pdf.to_csv(predict, index=False)

else:
    print("틀렸습니다. 이 파일을 재실행해주세요")