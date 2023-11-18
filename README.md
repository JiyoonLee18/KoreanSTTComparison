# Korean STT Comparison
현재 작성 중인 논문에서 필요한 STT API를 비교 분석하기 위해 작성한 코드를 넣어두는 저장소 (추후 추가 작성 예정)

- Sampling
  - 노트북  파일 3개
  - 각 데이터셋을 1000개씩 샘플링

- STT_API.py
  - 여러 개의 API를 호출하는 py 파일

- test.py
  - STT_API 실행 파일

- KoreanPreprocess.py
  - 한국어 전처리 py 파일
  - recognized text에 따라 cer이 가장 낮도록 answer_text를 전처리해 modified_text 추출

- KoreanPreprocess_231114.ipynb
  - 한국어 전처리 파이썬 노트북

- duration.ipynb
  - 각 dataset 음원의 길이를 기록해 저장하는 노트북

- KoreanSTT_analyze.ipynb
  - 비교 분석