import urllib3
import json
import base64
import time
from tqdm import tqdm
import requests
import pandas as pd

# 텍스트 파일 및 오디오 파일 세팅
def get_text(file_name, dataset):
    if dataset=="저음질":
        with open(file_name, 'r') as file:
            answer_text = [line.strip() for line in file.readlines()][0]
    elif dataset=="eval_clean" or dataset=="eval_other":
        answer_text=file_name.split(':: ')[1]
    elif dataset=="감성발화":
        with open(file_name, 'r', encoding='utf-8') as file:
            answer_text = json.load(file)
            answer_text=answer_text['전사정보']['OrgLabelText']
    return answer_text

def get_audioPath(file_name, dataset):
    if dataset=="저음질":
        audioFilePath = file_name.split('.')[0]+'.wav'
    elif dataset=="eval_clean" or dataset=="eval_other":
        audioFilePath='data/한국어 음성/sample/'+file_name.split('KsponSpeech_eval/')[1].split(' ::')[0].split('pcm')[0]+'wav'
    elif dataset=="감성발화":
        audioFilePath=file_name.replace('라벨링데이터','원천데이터').replace('json','wav')
    return audioFilePath

#etri
def etri_stt(loaded_list, dataset):

    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    accessKey = input("api_key를 입력해주세요: ")
    languageCode = "korean"

    predicted_list=[]
    for file_name in tqdm(loaded_list):
        
        # 시작 시간 기록
        start_time = time.time()

        answer_text=get_text(file_name, dataset)
        audioFilePath = get_audioPath(file_name, dataset)
        file = open(audioFilePath, "rb")
        audioContents = base64.b64encode(file.read()).decode("utf8")
        file.close()

        requestJson = {    
          "argument": {
              "language_code": languageCode,
              "audio": audioContents
          }
        }

        http = urllib3.PoolManager()
        response = http.request(
          "POST",
          openApiURL,
          headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
          body=json.dumps(requestJson)
        )

        data = json.loads(str(response.data,"utf-8"))
        try:
            recognized_text = data["return_object"]["recognized"]
        except:
            recognized_text=''

        # 종료 시간 기록
        end_time = time.time()

        # 실행 시간 계산
        execution_time = end_time - start_time
        predicted_list.append([file_name, answer_text, recognized_text, execution_time])
    pdf=pd.DataFrame(predicted_list, columns=['file_name','answer_text', 'recognized_text', 'execution_time'])
    return pdf

# returnzero
def returnzero_stt(loaded_list, dataset):
    token= input("token을 입력해주세요: ")
    predicted_list=[]
    for file_name in tqdm(loaded_list):
        
        # text, audiopath가져오기
        answer_text=get_text(file_name, dataset)
        audioFilePath = get_audioPath(file_name, dataset)
        
        start_time = time.time()

        config = {}
        resp1 = requests.post(
            'https://openapi.vito.ai/v1/transcribe',
            headers={'Authorization': 'bearer '+token},
            data={'config': json.dumps(config)},
            files={'file': open(audioFilePath, 'rb')}
        )
        voiceid=resp1.json()['id']
        while True:
            resp2 = requests.get(
            'https://openapi.vito.ai/v1/transcribe/'+voiceid,
            headers={'Authorization': 'bearer '+token})
            if resp2.json()['status'] == 'transcribing':
                time.sleep(0.2)
            else:
                break

        try:
            recognized_text=resp2.json()['results']['utterances'][0]['msg']
        except:
            recognized_text=''
        
        # 종료 시간 기록
        end_time = time.time()

        # 실행 시간 계산
        execution_time = end_time - start_time
        predicted_list.append([file_name, answer_text, recognized_text, execution_time])

    pdf=pd.DataFrame(predicted_list, columns=['file_name','answer_text', 'recognized_text', 'execution_time'])
    return pdf

# 네이버
def naver_stt(loaded_list, dataset):
    client_id= input("client_id를 입력해주세요: ")
    client_secret = input("client_secret를 입력해주세요: ")
    lang = "Kor" # 언어 코드 ( Kor, Jpn, Eng, Chn )
    url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
    
    predicted_list=[]
    
    headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/octet-stream"
}
    
    for file_name in tqdm(loaded_list):

        # text, audiopath가져오기
        answer_text=get_text(file_name, dataset)
        audioFilePath = get_audioPath(file_name, dataset)
        
        # 시작 시간 기록
        start_time = time.time()
        
        data = open(audioFilePath, 'rb')
        response = requests.post(url,  data=data, headers=headers)
        try:
            recognized_text=json.loads(response.text)['text']
        except:
            recognized_text=''
        
        # 종료 시간 기록
        end_time = time.time()

        # 실행 시간 계산
        execution_time = end_time - start_time
        predicted_list.append([file_name, answer_text, recognized_text, execution_time])
    pdf=pd.DataFrame(predicted_list, columns=['file_name','answer_text', 'recognized_text', 'execution_time'])
    return pdf