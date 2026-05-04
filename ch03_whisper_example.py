import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 환경 설정 로드
load_dotenv("API_KEY.env")
api_key = os.getenv("API_KEY")

# 2. 클라이언트 엔진 초기화
# 이제 api_key가 비어있을 경우에 대한 최소한의 방어 코드만 남깁니다.
if not api_key:
    raise ValueError("API_KEY를 찾을 수 없습니다. .env 파일을 확인하세요.")

client = OpenAI(api_key=api_key)

# 3. Whisper 인식 로직
def speech_to_text(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return transcript.text

# 4. 실행 및 결과 출력
if __name__ == "__main__":
    result_text = speech_to_text("output.mp3")
    print(f"인식 결과: {result_text}")