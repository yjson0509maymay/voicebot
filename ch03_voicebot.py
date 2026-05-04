import streamlit as st

##### 메인함수 #####
def main():
    #기본설정
    st.set_page_config(
        page_title="음성 비서 프로그램",
        layout="wide")
    
    #제목
    st.header("음성 비서 프로그램")
    
    #구분선
    st.markdown("---")
    
    #기본 설명
    with st.exapander("음성비서 프로그램에 관하여", expanded=True):    st.write(
        """
        -음성 비서 프로그램의 UI는 스트림릿을 활용했습니다.
        -STT(Speech-To-Text)는 OpenAI의 Whisper AI를 활용했습니다.
        -답변은 OpenAI 의 GPT  모델을 활용했습니다.
        -TTS(Text-To-Speech)는 구글의 Google Translate TTS를 활용했습니다.
        """
        )
    
    st.markdown("")
    
if __name__=="__main__":
     main()