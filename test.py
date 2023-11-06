import pandas as pd
from STT_API import etri_stt, returnzero_stt, naver_stt, azure_stt, google_stt, whisper_stt

predict_path='predict/'
data_path='data/'

# sample txt 파일 불러오기
dataset=input("데이터 선택 입력해주세요: (저음질, eval_clean, eval_other, 감성발화 택1) ")
if dataset=="저음질":
    file_name=data_path+"저음질 전화 음성/저음질_random.txt"
    predict=predict_path+'저음질_'
elif dataset=="eval_clean":
    file_name=data_path+"한국어 음성/sample/eval_clean.txt"
    predict=predict_path+'eval_clean_'
elif dataset=="eval_other":
    file_name=data_path+"한국어 음성/sample/eval_other.txt"
    predict=predict_path+'eval_other_'
elif dataset=="감성발화":
    file_name=data_path+"감성 발화/감성발화_random.txt"
    predict=predict_path+'감성발화_'
else:
    print("틀렸습니다. 이 파일을 재실행해주세요")

try:
    with open(file_name, 'r') as file:
        # 파일의 각 줄을 읽어와 리스트에 저장
        loaded_list = [line.strip() for line in file.readlines()]
    print(f"{file_name} 파일을 성공적으로 불러왔습니다.")
except Exception as e:
    print(f"파일 불러오기 중 오류가 발생했습니다: {e}")

## 예측
model=input("모델 선택 입력해주세요: (etri, returnzero, naver, azure, google, whisper 택1) ")
if model=="etri":
    # 예측
    pdf=etri_stt(loaded_list, dataset)
    # 저장
    predict=predict+'etri.csv'
    pdf.to_csv(predict, index=False)

elif model=="returnzero":
    # 예측
    pdf=returnzero_stt(loaded_list, dataset)

    # 저장
    predict=predict+'returnzero.csv'
    # pdf.to_csv(predict, index=False)

elif model=="naver":
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