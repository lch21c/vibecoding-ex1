import streamlit as st
import pandas as pd

def main():
    st.title('👋 이름 기반 인사말 앱 (수평 정렬 버전)')
    st.markdown('---')

    # 1. 페이지를 두 개의 열로 나눕니다.
    # col1에는 입력창을, col2에는 버튼을 배치하여 수평 정렬합니다.
    # 열의 너비를 조정하여 입력창이 더 넓게 보이도록 비율을 설정할 수 있습니다. (예: [3, 1])
    col1, col2 = st.columns([3, 1]) 

    # 2. 첫 번째 열(col1)에 텍스트 입력 위젯 배치
    # 여기서는 레이블을 비우고, st.write()를 사용하여 별도로 설명을 추가합니다.
    with col1:
        st.write('이름을 입력하세요:')
        user_name = st.text_input(
            label='숨겨진 레이블', # 실제 레이블은 숨기거나(label_visibility='hidden') 비워둡니다.
            value='', 
            key='name_input', 
            label_visibility='hidden' # 레이블을 숨겨서 공간을 절약합니다.
        )
        
    # 3. 두 번째 열(col2)에 버튼 배치
    # 버튼이 입력창과 수평하게 정렬되도록 col2에 배치합니다.
    with col2:
        # st.empty()를 사용하여 버튼이 입력창과 수직으로 잘 정렬되도록 빈 공간을 추가할 수 있습니다.
        # st.empty()를 사용하는 대신, st.markdown('<br>', unsafe_allow_html=True)로 강제 개행을 할 수도 있습니다.
        # Streamlit은 상단에서 아래로 위젯을 쌓기 때문에, 버튼이 입력창의 중앙에 오도록 약간의 트릭이 필요합니다.
        st.write('') # 빈 줄을 하나 추가하여 버튼을 입력창 중앙에 가깝게 내립니다.
        if st.button('결과 확인!'):
            # 4. 버튼 클릭 시 로직 실행
            if user_name:
                # 🎈 애니메이션 효과
                st.balloons()
                
                # 🎉 인사말 메시지 출력
                greeting_message = f'Hello, **{user_name}**!'
                st.success(greeting_message)
                
            else:
                # 이름이 비어있을 경우 경고 메시지 출력
                st.warning('이름을 입력해 주세요!')

# 파이썬 스크립트가 직접 실행될 때 main 함수를 호출
if __name__ == '__main__':
    main()
