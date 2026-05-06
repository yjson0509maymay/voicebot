import streamlit as st
from audiorecorder import audiorecorder
import openai
import os
from datetime import datetime
from gtts import gTTS
import base64
import hashlib

def STT(audio, apikey):
    filename = 'input.mp3'
    audio.export(filename, format="mp3")
    audio_file = open(filename, "rb")
    client = openai.OpenAI(api_key=apikey)
    response = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    audio_file.close()
    os.remove(filename)
    return response.text

def ask_gpt(prompt, model, apikey):
    client = openai.OpenAI(api_key=apikey)
    response = client.chat.completions.create(
        model=model,
        messages=prompt
    )
    return response.choices[0].message.content

def TTS(response):
    filename = "output.mp3"
    tts = gTTS(text=response, lang='ko')
    tts.save(filename)
    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)
    os.remove(filename)

def main():
    st.set_page_config(page_title="음성 비서 프로그램", layout="wide")

    if "chat" not in st.session_state:
        st.session_state["chat"] = []
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""
    if "message" not in st.session_state:
        st.session_state["message"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in Korean"}]
    if "check_reset" not in st.session_state:
        st.session_state["check_reset"] = False
    # ✅ 추가: 중복 녹음 처리 방지용 hash
    # → 오리지널은 같은 녹음을 매 rerun마다 재처리하는 문제가 있음
    # → hash로 새 녹음인지 판별
    if "last_audio_hash" not in st.session_state:
        st.session_state["last_audio_hash"] = None

    st.header("손연정 음성 비서 프로그램")
    st.markdown("---")

    with st.expander("음성 비서 프로그램에 관하여", expanded=True):
        st.write(
            """
            - 음성 비서 프로그램의 UI는 스트림릿을 활용했습니다.
            - STT(Speech-To-Text) 기능은 OpenAI의 Whisper AI를 활용했습니다.
            - TTS(Text-To-Speech) 기능은 gTTS(Google Text-to-Speech)를 활용했습니다.
            - 답변은 OpenAI의 GPT 모델을 활용했습니다.
            """
        )

    st.markdown("---")

    with st.sidebar:
        st.session_state["OPENAI_API"] = st.text_input(
            label="OPENAI API KEY",
            placeholder="Enter Your API Key",
            value="",
            type="password"
        )
        st.markdown("---")
        model = st.radio(label="GPT 모델", options=["gpt-4o", "gpt-3.5-turbo"])
        st.markdown("---")
        if st.button(label="초기화"):
            st.session_state["chat"] = []
            st.session_state["message"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in Korean"}]
            # ✅ 초기화 시 hash도 리셋 → 다음 녹음 새것으로 인식
            st.session_state["last_audio_hash"] = None
            st.session_state["check_reset"] = False
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("질문하기")
        # audio = audiorecorder("🎙️ 클릭하여 녹음 시작", "⏹️ 클릭하여 녹음 중지", pause_prompt="")
        audio = audiorecorder("🎙️ 클릭하여 녹음 시작", "⏹️ 클릭하여 녹음 중지")

        # ✅ 오리지널 구조 유지: rerun 없이 col1→col2 순서로 흘러내려감
        # → rerun을 쓰면 col2 렌더링 전에 재시작되어 TTS 타이밍이 꼬임
        if (len(audio) > 0) and (not st.session_state["check_reset"]):
            audio_bytes = audio.export().read()
            st.audio(audio_bytes)

            current_hash = hashlib.md5(audio_bytes).hexdigest()

            # ✅ 새 녹음일 때만 STT/GPT/TTS 처리
            # → 오리지널은 hash 없어서 같은 녹음을 계속 재처리함
            if current_hash != st.session_state["last_audio_hash"]:
                st.session_state["last_audio_hash"] = current_hash

                if not st.session_state["OPENAI_API"]:
                    st.warning("⚠️ 사이드바에 API 키를 먼저 입력해주세요.")
                else:
                    with st.spinner("음성 인식 중..."):
                        question = STT(audio, st.session_state["OPENAI_API"])

                    st.success(f"📝 인식된 텍스트: {question}")
                    now = datetime.now().strftime("%H:%M")
                    st.session_state["chat"] += [("user", now, question)]
                    st.session_state["message"] += [{"role": "user", "content": question}]

    with col2:
        st.subheader("질문/답변")

        # ✅ 오리지널과 동일한 구조: col2에서 audio 재참조
        # → rerun 없이 순차 실행되므로 audio 변수가 살아있음
        # → 새 녹음(hash 변경)일 때만 GPT+TTS 실행
        if (len(audio) > 0) and (not st.session_state["check_reset"]):
            current_hash = hashlib.md5(audio.export().read()).hexdigest()

            # chat에 user 메시지가 있고 방금 새로 추가된 경우에만 GPT 호출
            if (st.session_state["chat"] and
                st.session_state["chat"][-1][0] == "user" and
                current_hash == st.session_state["last_audio_hash"]):

                with st.spinner("🤖 GPT 답변 생성 중..."):
                    response = ask_gpt(
                        st.session_state["message"],
                        model,
                        st.session_state["OPENAI_API"]
                    )

                now = datetime.now().strftime("%H:%M")
                st.session_state["message"] += [{"role": "assistant", "content": response}]
                st.session_state["chat"] += [("bot", now, response)]

                # ✅ 채팅 시각화
                for sender, t, msg in st.session_state["chat"]:
                    if sender == "user":
                        st.markdown(
                            f'<div style="display:flex;align-items:center;margin-bottom:8px;">'
                            f'<div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{msg}</div>'
                            f'<div style="font-size:0.8rem;color:gray;">{t}</div></div>',
                            unsafe_allow_html=True)
                    else:
                        st.markdown(
                            f'<div style="display:flex;align-items:center;justify-content:flex-end;margin-bottom:8px;">'
                            f'<div style="background-color:#3a3a3a;color:white;border-radius:12px;padding:8px 12px;margin-left:8px;">{msg}</div>'
                            f'<div style="font-size:0.8rem;color:gray;">{t}</div></div>',
                            unsafe_allow_html=True)

                # ✅ TTS: rerun 없이 이 시점에 바로 재생 → 오리지널과 동일한 타이밍
                TTS(response)

        else:
            # 새 녹음 없을 때는 기존 채팅 기록만 표시
            for sender, t, msg in st.session_state["chat"]:
                if sender == "user":
                    st.markdown(
                        f'<div style="display:flex;align-items:center;margin-bottom:8px;">'
                        f'<div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{msg}</div>'
                        f'<div style="font-size:0.8rem;color:gray;">{t}</div></div>',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div style="display:flex;align-items:center;justify-content:flex-end;margin-bottom:8px;">'
                        f'<div style="background-color:#3a3a3a;color:white;border-radius:12px;padding:8px 12px;margin-left:8px;">{msg}</div>'
                        f'<div style="font-size:0.8rem;color:gray;">{t}</div></div>',
                        unsafe_allow_html=True)

if __name__ == "__main__":
    main()