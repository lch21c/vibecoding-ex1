import streamlit as st
import pandas as pd # st.text_input 버그 해결용 임포트

def main():
    # 🐱 배경 이미지 추가를 위한 CSS 스타일 삽입
    # st.markdown을 사용하여 HTML과 CSS를 주입합니다.
    # unsafe_allow_html=True는 HTML을 안전하지 않은 방식으로 허용한다는 의미이므로 주의해서 사용해야 합니다.
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1518791841217-8f162f1e1131?q=80&w=1770&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed; /* 스크롤 시 배경 이미지가 고정됩니다. */
            background-position: center;
        }
        /* 텍스트 입력창 및 버튼 배경을 반투명하게 만들어 가독성을 높일 수 있습니다. */
        .stTextInput > div > div > input, .stButton > button {
            background-color: rgba(255, 255, 255, 0.7); /* 흰색 배경에 70% 불투명도 */
            color: black; /* 텍스트 색상 */
        }
        /* 성공 메시지 박스도 배경에 맞춰 조정합니다. */
        .stAlert {
            background-color: rgba(200, 255, 200, 0.8); /* 연두색 배경에 80% 불투명도 */
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title('👋 이름 기반 인사말 앱 (고양이 배경 버전)')
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
        st.write('') # 버튼 수직 정렬 보정
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
