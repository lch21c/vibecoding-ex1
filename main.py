import streamlit as st
import pandas as pd
import base64 # 이미지를 base64로 인코딩하여 CSS에 삽입하기 위해 필요

# 🐶 진돗개 배경 이미지를 base64로 인코딩하는 함수
# 이 함수는 이미지를 CSS에 직접 삽입할 수 있는 형식으로 변환합니다.
@st.cache_data # 이미지를 매번 로드하지 않도록 캐싱합니다.
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 🐶 CSS 스타일을 생성하는 함수
def set_background_image(image_file):
    bin_str = get_base64_of_bin_file(image_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover; # 배경 이미지가 전체 화면을 덮도록 설정
        background-position: center; # 이미지를 중앙에 배치
        background-repeat: no-repeat; # 이미지가 반복되지 않도록 설정
        background-attachment: fixed; # 스크롤해도 배경 이미지가 고정되도록 설정
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# 🐶 메인 Streamlit 앱 함수
def main():
    # 1. 배경 이미지 설정 함수 호출
    # 'Jindo_Dog_Background.jpg' 파일을 스크립트와 같은 폴더에 넣어주세요.
    set_background_image('Jindo_Dog_Background.jpg') 

    # 앱의 콘텐츠 시작
    st.title('👋 이름 기반 인사말 앱 (진돗개 배경)')
    st.markdown('---')

    # 컨텐츠의 가독성을 위해 배경색이 있는 컨테이너를 사용할 수 있습니다.
    # st.container()를 사용하면 위젯들을 그룹화할 수 있습니다.
    with st.container(border=True): # border=True로 컨테이너에 테두리 추가
        # 1. 페이지를 두 개의 열로 나눕니다.
        col1, col2 = st.columns([3, 1]) 

        # 2. 첫 번째 열(col1)에 텍스트 입력 위젯 배치
        with col1:
            st.write('이름을 입력하세요:')
            user_name = st.text_input(
                label='숨겨진 레이블', 
                value='', 
                key='name_input', 
                label_visibility='hidden'
            )
            
        # 3. 두 번째 열(col2)에 버튼 배치
        with col2:
            st.write('') 
            if st.button('결과 확인!'):
                # 4. 버튼 클릭 시 로직 실행
                if user_name:
                    st.balloons()
                    greeting_message = f'Hello, **{user_name}**!'
                    st.success(greeting_message)
                    
                else:
                    st.warning('이름을 입력해 주세요!')

# 파이썬 스크립트가 직접 실행될 때 main 함수를 호출
if __name__ == '__main__':
    main()
