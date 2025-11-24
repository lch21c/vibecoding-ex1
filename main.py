import streamlit as st

def main():
    # 1. 앱 제목 설정
    st.title('👋 이름 기반 인사말 앱 (Hello App)')

    # 2. 사용자에게 텍스트 입력 위젯 제공
    # st.text_input() 함수는 사용자로부터 텍스트를 입력받습니다.
    # label: 입력 필드 위에 표시될 설명 텍스트
    # value: 입력 필드의 기본값
    user_name = st.text_input('여기에 당신의 이름을 입력하세요:', value='World')

    # 3. 입력된 이름에 따라 인사말 출력
    # user_name 변수가 비어있지 않은 경우에만 메시지를 출력합니다.
    if user_name:
        # f-string을 사용하여 입력받은 이름으로 인사말을 만듭니다.
        greeting_message = f'Hello, **{user_name}**!'

        # st.header()를 사용하여 눈에 띄게 큰 글씨로 인사말을 표시합니다.
        st.header(greeting_message)
    else:
        st.write('이름을 입력하시면 인사말이 나타납니다.')

# 파이썬 스크립트가 직접 실행될 때 main 함수를 호출
if __name__ == '__main__':
    main()
