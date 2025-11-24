import streamlit as st
import pandas as pd # st.text_input의 버그 해결을 위해 임포트 (실제 사용은 하지 않음)

def main():
    st.title('👋 이름 기반 인사말 앱 (인터랙티브 버전)')
    st.markdown('---')

    # 1. 사용자 입력 필드 생성
    # key를 사용하여 세션 상태에서 이 위젯을 식별합니다.
    user_name = st.text_input('여기에 당신의 이름을 입력하세요:', value='', key='name_input')

    # 2. 결과 출력 버튼 생성
    # 버튼이 클릭되었는지 확인합니다.
    if st.button('결과 확인!'):
        # 3. 버튼 클릭 시 로직 실행
        if user_name:
            # 🎈 애니메이션 효과: 풍선 애니메이션을 실행합니다.
            st.balloons()
            
            # 🎉 "Hello, [이름]!" 메시지를 st.success (성공 메시지 박스) 형태로 출력하여 강조합니다.
            greeting_message = f'Hello, **{user_name}**!'
            st.success(greeting_message)
            
            # (선택 사항) 결과 출력 후 텍스트 필드를 비우려면 st.session_state를 사용합니다.
            # st.session_state.name_input = ''

        else:
            # 이름이 비어있을 경우 경고 메시지 출력
            st.warning('이름을 입력해 주세요!')

# 파이썬 스크립트가 직접 실행될 때 main 함수를 호출
if __name__ == '__main__':
    # Streamlit은 항상 main() 함수를 다시 실행하므로, st.session_state를 초기화합니다.
    if 'name_input' not in st.session_state:
        st.session_state.name_input = ''
        
    main()
