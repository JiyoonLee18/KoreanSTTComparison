import urllib3
import json
import base64
import time
from tqdm import tqdm
import requests

def etri_stt(loaded_list):

    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    accessKey = input("api_key를 입력해주세요: ")
    languageCode = "korean"

    predicted_list=[]
    for file_name in tqdm(loaded_list):
        
        # 시작 시간 기록
        start_time = time.time()

        with open(file_name, 'r') as file:
            answer_text = [line.strip() for line in file.readlines()][0]
        audioFilePath = file_name.split('.')[0]+'.wav'
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
        recognized_text = data["return_object"]["recognized"]

        # 종료 시간 기록
        end_time = time.time()

        # 실행 시간 계산
        execution_time = end_time - start_time
        predicted_list.append([file_name, answer_text, recognized_text, execution_time])
    return predicted_list

def returnzero_stt(loaded_list):
    token= input("token을 입력해주세요: ")
    predicted_list=[]
    for file_name in tqdm(loaded_list):
         # 텍스트 파일 열기
        with open(file_name, 'r') as file:
            answer_text = [line.strip() for line in file.readlines()][0]
        audioFilePath=file_name.split('.')[0]+'.wav'
        
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
        recognized_text=resp2.json()['results']['utterances'][0]['msg']
        # 종료 시간 기록
        end_time = time.time()

        # 실행 시간 계산
        execution_time = end_time - start_time
        predicted_list.append([file_name, answer_text, recognized_text, execution_time])
    return predicted_list