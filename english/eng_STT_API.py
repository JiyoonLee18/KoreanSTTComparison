import urllib3
import json
import base64
import time
from tqdm import tqdm
import requests
import pandas as pd
import string
import threading
import wave
import azure.cognitiveservices.speech as speechsdk
import io
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
import os
import openai

AudioSegment.converter = "C:/Users/82105/Downloads/ffmpeg-6.0-full_build/bin/ffmpeg.exe"

def get_text(file_name, dataset):
    data_path='data/'
    if dataset=="1":
        df=pd.read_csv(data_path+"common voice/sample/sample.csv")
        answer_text=df[df['filename']==file_name]['text'].values[0].strip()
    elif dataset=="2":
        with open(file_name, 'r') as file:
            # 파일의 각 줄을 읽어와 리스트에 저장
            answer_text = [line.strip() for line in file.readlines()]
            answer_text=answer_text[0].strip()
    elif dataset=="3":
        df=pd.read_csv(data_path+"3_CMU/sample.csv")
        answer_text=df[df['file_path']==file_name]['speech'].values[0].strip()
    elif dataset=="4":
        df=pd.read_csv(data_path+"4_IEMOCAP/sample.csv")
        answer_text=df[df['titre']==file_name]['to_translate'].values[0].strip()
    return answer_text

def get_audioPath(file_name, dataset):
    if dataset=="1":
        audioFilePath ='data/common voice/sample/'+file_name.replace('mp3','wav')
    elif dataset=="2":
        audioFilePath=file_name.replace("txt", "wav")
    elif dataset=="3":
        audioFilePath="data/3_CMU/"+file_name
    elif dataset=="4":
        audioFilePath="data/4_IEMOCAP/IEMOCAP_wav/"+file_name+'.wav'
    return audioFilePath

# 네이버
def naver_stt(loaded_list, dataset):
    client_id= input("client_id를 입력해주세요: ")
    client_secret = input("client_secret를 입력해주세요: ")
    lang = "Eng" # 언어 코드 ( Kor, Jpn, Eng, Chn )
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

# Azure
def azure_stt(loaded_list, dataset):
    speech_key=input("speech_key를 입력해주세요: ")
    service_region="koreacentral"
    
    predicted_list=[]
    
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    
    for file_name in tqdm(loaded_list):
        # text, audiopath가져오기
        answer_text=get_text(file_name, dataset)
        audioFilePath = get_audioPath(file_name, dataset)
        
        # 시작 시간 기록
        start_time = time.time()
        
        audio_config = speechsdk.audio.AudioConfig(filename=audioFilePath)
        # Creates a speech recognizer using a file as audio input, also specify the speech language
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, language="en-US", audio_config=audio_config)

        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text=result.text
        else:
            recognized_text=""
        # 종료 시간 기록
        end_time = time.time()
                
        # 실행 시간 계산
        execution_time = end_time - start_time
        predicted_list.append([file_name, answer_text, recognized_text, execution_time])
    pdf=pd.DataFrame(predicted_list, columns=['file_name','answer_text', 'recognized_text', 'execution_time'])
    return pdf

def google_stt(loaded_list, dataset):
    client_file='sa_speech_demo.json'
    credentials=service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)
    
    predicted_list=[]

    for file_name in tqdm(loaded_list):
        # text, audiopath가져오기
        answer_text=get_text(file_name, dataset)
        audioFilePath = get_audioPath(file_name, dataset)
        
        # 시작 시간 기록
        start_time = time.time()
        
        with wave.open(audioFilePath, "rb") as wav_file:
                sample_rate = wav_file.getframerate()

        # WAV 파일을 읽어와서 스테레오를 모노로 변환
        audio = AudioSegment.from_file(audioFilePath)
        audio = audio.set_channels(1)
        content = audio.raw_data

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code="en-US",
        )

        response = client.recognize(config=config, audio=audio)
        
        try: 
            recognized_text=response.results[0].alternatives[0].transcript
        except:
            recognized_text=''
            
        # 종료 시간 기록
        end_time = time.time()

        # 실행 시간 계산
        execution_time = end_time - start_time
        predicted_list.append([file_name, answer_text, recognized_text, execution_time])
    pdf=pd.DataFrame(predicted_list, columns=['file_name','answer_text', 'recognized_text', 'execution_time'])
    return pdf

def whisper_stt(loaded_list, dataset):
    api_key = input("api_key를 입력해주세요: ")
    openai.api_key = api_key
    
    predicted_list=[]
    
    for file_name in tqdm(loaded_list):
        # text, audiopath가져오기
        answer_text=get_text(file_name, dataset)
        audioFilePath = get_audioPath(file_name, dataset)
        
        try:
            # 시작 시간 기록
            start_time = time.time()
            
            audio_file = open(audioFilePath, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file, language="en")
            
            try: 
                recognized_text=transcript['text']
            except:
                recognized_text=''
                
            # 종료 시간 기록
            end_time = time.time()

            # 실행 시간 계산
            execution_time = end_time - start_time
        except:
            recognized_text="error"
            execution_time="error"
            print("error, file: ",audioFilePath)
        predicted_list.append([file_name, answer_text, recognized_text, execution_time])
    pdf=pd.DataFrame(predicted_list, columns=['file_name','answer_text', 'recognized_text', 'execution_time'])
    return pdf