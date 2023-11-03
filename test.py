import pandas as pd
from STT_API import etri_stt, returnzero_stt

predict_path='predict/'
data_path='data/'

# sample txt 파일 불러오기
data=input("데이터 선택 입력해주세요: (저음질, eval_clean, eval_other, 감성발화 택1) ")
if data=="저음질":
    file_name=data_path+"저음질 전화 음성/저음질_random.txt"
    predict=predict_path+'저음질_'
elif data=="eval_clean":
    file_name=data_path+"한국어 음성/eval_clean.txt"
    predict=predict_path+'eval_clean_'
elif data=="eval_other":
    file_name=data_path+"한국어 음성/eval_other.txt"
    predict=predict_path+'eval_other_'
elif data=="감성발화":
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
model=input("모델 선택 입력해주세요: (etri, returnzero 택1) ")
if model=="etri":
    # 예측
    predicted_list=etri_stt(loaded_list)
    pdf=pd.DataFrame(predicted_list)
    # 저장
    predict=predict+'etri.csv'
    pdf.to_csv(predict, index=False)

elif model=="returnzero":
    # 예측
    predicted_list=returnzero_stt(loaded_list)
    pdf=pd.DataFrame(predicted_list)
    # 저장
    predict=predict+'returnzero.csv'
    pdf.to_csv(predict, index=False)
else:
    print("틀렸습니다. 이 파일을 재실행해주세요")