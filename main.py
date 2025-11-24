import streamlit as st
import pandas as pd

# 사용할 배경 이미지 URL
# 이 부분을 실제 태양계 배경 이미지 URL로 변경해주세요!
BACKGROUND_IMAGE_URL = "https://www.pixelstalk.net/wp-content/uploads/2016/06/High-Resolution-Solar-System-Wallpaper.jpg" 
# 또는 로컬 이미지 파일을 base64로 인코딩하여 사용할 수도 있습니다 (더 복잡함).

def main():
    st.set_page_config(layout="wide") # 페이지 레이아웃을 넓게 설정

    # 커스텀 CSS를 사용하여 배경 이미지 설정
    # 이 CSS 코드는 페이지 전체에 적용됩니다.
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{BACKGROUND_IMAGE_URL}");
            background-size: cover;          /* 이미지가 전체 배경을 덮도록 */
            background-repeat: no-repeat;    /* 이미지 반복 안함 */
            background-attachment: fixed;    /* 스크롤 시 배경 고정 */
            background-position: center;     /* 이미지를 중앙에 배치 */
        }}
        /* 앱의 주요 컨텐츠 영역의 배경을 투명하게 만들어 배경 이미지가 보이도록 */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.7); /* 흰색 배경에 투명도 70% */
            border-radius: 10px; /* 컨텐츠 박스 모서리 둥글게 */
            padding: 2rem; /* 내부 여백 추가 */
        }}
        /* 텍스트 입력 필드나 버튼 같은 위젯들이 배경에 묻히지 않도록 스타일 조정 */
        .stTextInput > div > div > input {{
            background-color: rgba(255, 255, 255, 0.9); /* 입력 필드 배경색 */
            color: black; /* 텍스트 색상 */
        }}
        .stButton > button {{
            background-color: #4CAF50; /* 버튼 배경색 */
            color: white; /* 버튼 텍스트 색상 */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title('👋 이름 기반 인사말 앱 (태양계 배경 버전)')
    st.markdown('---')

    col1, col2 = st.columns([3, 1]) 

    with col1:
        st.write('이름을 입력하세요:')
        user_name = st.text_input(
            label='숨겨진 레이블', 
            value='', 
            key='name_input', 
            label_visibility='hidden' 
        )
        
    with col2:
        st.write('') 
        if st.button('결과 확인!'):
            if user_name:
                st.balloons()
                greeting_message = f'Hello, **{user_name}**!'
                st.success(greeting_message)
            else:
                st.warning('이름을 입력해 주세요!')

# 파이썬 스크립트가 직접 실행될 때 main 함수를 호출
if __name__ == '__main__':
    main()
