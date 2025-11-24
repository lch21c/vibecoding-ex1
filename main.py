import streamlit as st
import time # 결과를 애니메이션으로 보여주기 위해 time 모듈 추가

def main():
    st.title('👋 이름 기반 인사말 앱 (가로 배치 버전)')
    st.markdown('---')

    # 1. 두 개의 열(Column)을 정의합니다. 
    # 첫 번째 열은 입력 필드를 위해 더 넓게 (예: 3), 두 번째 열은 버튼을 위해 좁게 (예: 1) 비율을 지정합니다.
    col1, col2 = st.columns([3, 1])

    # 2. 첫 번째 열(col1)에 텍스트 입력 위젯 배치
    with col1:
        # key를 사용하여 세션 상태에서 이 위젯을 식별합니다.
        user_name = st.text_input(
            '여기에 당신의 이름을 입력하세요:', 
            value='', 
            key='name_input',
            label_visibility="collapsed" # 레이블을 숨겨서 공간을 절약합니다.
        )
        
    # 3. 두 번째 열(col2)에 버튼 위젯 배치
    with col2:
        # 버튼을 입력창과 같은 높이에 위치시키기 위해 st.button() 앞에 빈 공간을 추가하여 수직 정렬을 맞춥니다.
        # st.markdown('&nbsp;')
        # st.button 대신 st.form을 사용하면 더 정확한 수직 정렬이 가능하지만, 여기서는 간단하게 버튼만 사용합니다.
        st.markdown("<br>", unsafe_allow_html=True) # 줄 바꿈 태그를 사용해 버튼의 위치를 조정합니다.
        
        button_clicked = st.button('확인!')

    # 4. 버튼 클릭 시 로직 실행
    if button_clicked:
        if user_name:
            # ⏳ 잠시 로딩하는 듯한 애니메이션 효과
            with st.spinner(f'**{user_name}**님을 위한 인사말을 준비 중입니다...'):
                time.sleep(1) # 1초 동안 대기
            
            # 🎉 "Hello, [이름]!" 메시지를 st.success 형태로 출력
            greeting_message = f'Hello, **{user_name}**!'
            st.success(greeting_message)
            
            # 🎈 애니메이션 효과: 풍선 애니메이션을 실행합니다.
            st.balloons()
            
        else:
            # 이름이 비어있을 경우 경고 메시지 출력 (가로 배치 아래에 출력)
            st.warning('이름을 입력해 주세요!')

# 파이썬 스크립트가 직접 실행될 때 main 함수를 호출
if __name__ == '__main__':
    if 'name_input' not in st.session_state:
        st.session_state.name_input = ''
        
    main()
