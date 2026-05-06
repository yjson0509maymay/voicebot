# 🎙️ 음성 비서 프로그램 (Voice Assistant Program)

> AI 기반 음성 대화 비서 | An AI-powered voice assistant

---

## 📌 프로그램 소개 | Overview

**한국어**
마이크로 질문을 녹음하면 AI가 텍스트로 변환하고, GPT가 답변을 생성한 뒤 음성으로 다시 읽어주는 음성 비서 프로그램입니다.

**English**
A voice assistant that records your question via microphone, converts it to text using Whisper AI, generates a response with GPT, and reads it back using text-to-speech.

---

## 🛠️ 사용 기술 | Tech Stack

| 역할 | 기술 |
|------|------|
| UI 프레임워크 | [Streamlit](https://streamlit.io/) |
| 음성 녹음 | [streamlit-audiorecorder](https://github.com/theevann/streamlit-audiorecorder) |
| 음성 → 텍스트 (STT) | [OpenAI Whisper](https://openai.com/research/whisper) |
| 답변 생성 (LLM) | [OpenAI GPT](https://platform.openai.com/) |
| 텍스트 → 음성 (TTS) | [gTTS (Google Text-to-Speech)](https://gtts.readthedocs.io/) |

---

## 🚀 설치 및 실행 방법 | Installation & Setup

### 1. Python 3.11 가상환경 생성 | Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 2. 패키지 설치 | Install dependencies
```bash
pip install -r requirements.txt
```

### 3. ffmpeg 설치 | Install ffmpeg
```bash
# Mac
brew install ffmpeg

# Windows
winget install ffmpeg
```

### 4. 실행 | Run
```bash
streamlit run voicebot.py
```

---

## 💡 사용 방법 | How to Use

1. 사이드바에 **OpenAI API 키** 입력
2. 사용할 **GPT 모델** 선택 (gpt-4o 권장)
3. 🎙️ 버튼 클릭 후 질문 녹음
4. ⏹️ 버튼으로 녹음 중지
5. 자동으로 **텍스트 변환 → GPT 답변 → 음성 재생** 진행
6. 대화 내역은 오른쪽 화면에서 확인 가능
7. **초기화** 버튼으로 대화 내역 리셋 가능

---

## ⚠️ 주의사항 | Notes

- OpenAI API 키가 필요합니다 ([발급받기](https://platform.openai.com/api-keys))
- 마이크가 연결된 환경에서 사용하세요
- Python **3.11** 버전을 권장합니다 (3.12 이상은 일부 라이브러리 호환 문제 있음)
- API 키는 코드에 직접 입력하지 말고 사이드바에서 입력하세요

---

## 📁 프로젝트 구조 | Project Structure

```
voicebot/
├── voicebot.py        # 메인 코드 | Main application
├── requirements.txt   # 패키지 목록 | Dependencies
├── .gitignore         # 깃 제외 파일 | Git ignore rules
└── README.md          # 프로젝트 설명 | Project description
```

---

## 📦 주요 라이브러리 버전 | Key Library Versions

- `streamlit` >= 1.0
- `openai` >= 1.0
- `gtts` >= 2.0
- `streamlit-audiorecorder` >= 0.0.5
- `pydub` >= 0.25

---

*Made with ❤️ using Streamlit + OpenAI*
