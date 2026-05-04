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
    with st.expander("음성비서 프로그램에 관하여", expanded=True):    st.write(
        """
        -음성 비서 프로그램의 UI는 스트림릿을 활용했습니다.
        -STT(Speech-To-Text)는 OpenAI의 Whisper AI를 활용했습니다.
        -답변은 OpenAI 의 GPT  모델을 활용했습니다.
        -TTS(Text-To-Speech)는 구글의 Google Translate TTS를 활용했습니다.
        """
        )
    
    st.markdown("")
    
# if __name__=="__main__":
#      main()
     
#사이드바 생성
with st.sidebar:
    
    #Open AI API 키 입력받기 
    st.session_state["OPENAI_API"] = st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value ="", type="password")
    
    st.markdown("---")
    
    #GPT모델을 선택하기 위한 라디오 버튼 생성
    model=st.radio(label="GPT 모델", options=["gpt-4","gpt-3.5-turbo"])
    
    st.markdown("---")
    
    #리셋 버튼 생성
    if st.button(label="초기화"):
        #리셋 코드 # 'pass'를 넣어 에러를 방지하거나, st.rerun()을 사용해 페이지를 새로고침합니다.
        st.rerun()
        
if __name__=="__main__":
    main()