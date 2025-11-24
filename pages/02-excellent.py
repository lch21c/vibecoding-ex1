import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.colored_header import colored_header
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.badges import badge
from streamlit_extras.metric_cards import style_metric_cards

# --- 1. 데이터 로드 및 전처리 ---
@st.cache_data
def load_data():
    # 파일 이름을 사용합니다.
    df = pd.read_csv("countriesMBTI_16types.csv")
    # 'Country' 열을 인덱스로 설정
    df = df.set_index('Country')
    # 열 이름(MBTI) 대문자 변환
    df.columns = df.columns.str.upper()
    return df

# MBTI 설명 데이터 (간결하게 주요 특징만)
mbti_info = {
    'ISTJ': {'title': '만능 재주꾼', 'desc': '청렴결백한 논리주의자, 사실에 근거하여 계획하고 실행하며 책임감이 강합니다.', 'icon': 'fas fa-hammer', 'color': 'gray-80'},
    'ISFJ': {'title': '용감한 수호자', 'desc': '세심하고 따뜻한 배려심으로 주변 사람들을 돕고 지키는 헌신적인 사람들입니다.', 'icon': 'fas fa-heart', 'color': 'green-70'},
    'INFJ': {'title': '선의의 옹호자', 'desc': '통찰력과 영감을 통해 이상적인 세상을 꿈꾸며 조용히 세상을 변화시키는 예언자입니다.', 'icon': 'fas fa-lightbulb', 'color': 'blue-70'},
    'INTJ': {'title': '용의주도한 전략가', 'desc': '모든 것에 의문을 던지고 지식을 탐구하며, 큰 그림을 보는 독립적인 전략가입니다.', 'icon': 'fas fa-chess-knight', 'color': 'violet-70'},
    'ISTP': {'title': '만능 재주꾼', 'desc': '도구를 다루는 데 능숙하며, 논리적이고 객관적인 분석으로 문제를 해결하는 제작자입니다.', 'icon': 'fas fa-wrench', 'color': 'gray-50'},
    'ISFP': {'title': '호기심 많은 예술가', 'desc': '현재를 즐기며 예술적인 감각과 유연성을 가진, 따뜻하고 겸손한 성격의 소유자입니다.', 'icon': 'fas fa-palette', 'color': 'green-50'},
    'INFP': {'title': '열정적인 중재자', 'desc': '내면의 가치와 이상에 충실하며, 진정성과 공감 능력이 뛰어난 이상주의자입니다.', 'icon': 'fas fa-feather-alt', 'color': 'blue-50'},
    'INTP': {'title': '논리적인 사색가', 'desc': '지적 호기심이 많고 끝없이 아이디어를 탐구하는, 세상의 복잡성을 이해하려는 철학자입니다.', 'icon': 'fas fa-brain', 'color': 'violet-50'},
    'ESTP': {'title': '모험을 즐기는 사업가', 'desc': '활동적이고 대담하며, 문제를 즉시 해결하고 현실적인 결과를 만들어내는 행동가입니다.', 'icon': 'fas fa-running', 'color': 'gray-30'},
    'ESFP': {'title': '자유로운 영혼의 연예인', 'desc': '에너지가 넘치고 사교적이며, 주변 사람들을 즐겁게 하는 타고난 엔터테이너입니다.', 'icon': 'fas fa-cocktail', 'color': 'green-30'},
    'ENFP': {'title': '재기발랄한 활동가', 'desc': '창의적이고 외향적이며, 가능성을 탐색하고 삶의 즐거움을 추구하는 열정적인 사람들입니다.', 'icon': 'fas fa-fire', 'color': 'blue-30'},
    'ENTP': {'title': '뜨거운 논쟁을 즐기는 변론가', 'desc': '지적인 토론을 즐기고 기존 질서에 도전하며, 새로운 아이디어를 끊임없이 제시합니다.', 'icon': 'fas fa-comments', 'color': 'violet-30'},
    'ESTJ': {'title': '엄격한 관리자', 'desc': '질서를 중시하고 조직적이며, 규칙에 따라 효율적으로 일을 추진하는 현실적인 관리자입니다.', 'icon': 'fas fa-user-tie', 'color': 'gray-70'},
    'ESFJ': {'title': '사교적인 외교관', 'desc': '따뜻하고 인기 많으며, 사람들과의 관계를 중요시하고 공동체를 이끌어가는 조력자입니다.', 'icon': 'fas fa-hands-helping', 'color': 'green-70'},
    'ENFJ': {'title': '정의로운 사회운동가', 'desc': '카리스마 있고 열정적이며, 사람들을 격려하고 이끌어 성장하도록 돕는 타고난 리더입니다.', 'icon': 'fas fa-bullhorn', 'color': 'blue-70'},
    'ENTJ': {'title': '대담한 통솔자', 'desc': '장기적인 계획을 세우고 목표 달성을 위해 사람들을 이끄는, 자신감 넘치는 지도자입니다.', 'icon': 'fas fa-crown', 'color': 'violet-70'}
}

df_mbti = load_data()
MBTI_TYPES = list(df_mbti.columns)


# --- 2. Streamlit 앱 설정 ---
st.set_page_config(
    page_title="MBTI World Explorer 🗺️",
    page_icon=":brain:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. 사이드바 (사용자 입력) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Myers-Briggs_Type_Indicator_logo.png", width=250)
    st.header("나의 MBTI 유형은? 👇")
    # 4. 처음 접속 시 아무것도 선택되지 않도록 초기값 설정
    selected_mbti = st.selectbox(
        "**16가지 유형 중 하나를 선택하세요.**",
        options=[""] + MBTI_TYPES,
        index=0, # 첫 번째 옵션인 빈 문자열이 기본값
        format_func=lambda x: "유형을 선택하세요..." if x == "" else x
    )

    badge(type="github", name="streamlit", url="https://streamlit.io/")
    st.markdown("---")
    st.markdown("##### 💡 **Data Source**")
    st.caption("첨부된 국가별 MBTI 분포 비율 CSV 파일 사용")


# --- 4. 메인 컨텐츠 (조건부 렌더링) ---
if selected_mbti == "":
    # 4. MBTI가 선택되지 않았을 때의 메시지
    st.title("🤔 MBTI World Explorer 에 오신 것을 환영합니다!")
    st.markdown("---")
    st.info("**🚀 사이드바에서 당신의 MBTI 유형을 선택하고, 전 세계 통계를 확인해 보세요!**")
    st.subheader("🌐 이 앱의 목표")
    st.markdown("""
    * **당신의 MBTI** 유형에 대한 **간단한 설명**을 제공합니다.
    * 첨부된 파일을 기반으로 **국가별 통계 정보**를 보여줍니다.
    * 통계 정보를 바탕으로 당신에게 **맞춤형 멘트**를 전달합니다.
    """)
    st.markdown("---")
    st.image("https://i.imgur.com/gK9qQ4u.png") # MBTI 유형별 아이콘 이미지 예시 (출처: Unsplash)

else:
    # MBTI 정보 가져오기
    info = mbti_info[selected_mbti]
    mbti_df = df_mbti[[selected_mbti]]
    
    # 통계 계산
    avg_proportion = mbti_df[selected_mbti].mean()
    max_country = mbti_df.idxmax().iloc[0]
    max_proportion = mbti_df.max().iloc[0] * 100
    min_country = mbti_df.idxmin().iloc[0]
    min_proportion = mbti_df.min().iloc[0] * 100
    
    # 맞춤 멘트 생성 (3. 멘트 만들기)
    if avg_proportion > 0.06:
        ment = f"**{info['title']}** 유형은 전 세계적으로 비교적 **흔한** 유형에 속해요. 당신의 친화력과 보편적인 매력이 전 세계에서 통하고 있다는 증거랍니다!"
    elif avg_proportion > 0.04:
        ment = f"**{info['title']}** 유형은 전 세계에서 **적절한 비율**을 차지하는 균형 잡힌 유형입니다. 당신의 고유한 특성이 사회에 꼭 필요한 역할을 하고 있어요!"
    else:
        ment = f"**{info['title']}** 유형은 전 세계적으로 **상위 25% 이내의 희귀한** 유형이에요! 당신은 세상의 다양한 시각을 제공하는 **특별한** 사람입니다. 그 희소성을 자랑스럽게 생각하세요!"

    
    # --- 5. 멋진 디자인 적용 (Header, Icon, Metric Cards, DataFrame Explorer) ---
    
    # 5. Colored Header로 섹션 구분 및 아이콘 활용
    colored_header(
        label=f"{selected_mbti} - {info['title']} 유형 분석",
        description=f"🌐 전 세계 {max_country}에서 가장 높은 비율을 보이는 유형!",
        color_name=info['color']
    )
    
    st.markdown(f"## <i class='{info['icon']}'></i> {info['title']}", unsafe_allow_html=True)
    st.markdown(f"**💡 핵심 설명:** *{info['desc']}*")
    st.markdown("---")
    
    # Metric Cards (통계 정보)
    col1, col2, col3, col4 = st.columns(4)
    
    # 5. streamlit_extras.metric_cards 활용
    col1.metric(label="📊 전 세계 평균 분포", value=f"{avg_proportion*100:.2f}%", delta="평균치")
    col2.metric(label="🥇 최고 비율 국가", value=f"{max_country}", delta=f"비율: {max_proportion:.2f}%")
    col3.metric(label="📉 최저 비율 국가", value=f"{min_country}", delta=f"비율: {min_proportion:.2f}%")
    
    # 타입에 따른 맞춤 메시지
    col4.success("🌟 당신을 위한 맞춤 멘트")
    col4.markdown(f"<p style='font-size:16px; font-weight:bold;'>{ment}</p>", unsafe_allow_html=True)
    
    # 5. Metric Card 스타일 적용
    # *** 오류 수정: info['color'] 앞에 붙였던 '#'를 제거합니다. ***
    style_metric_cards(background_color="#FFFFFF", border_left_color=info['color'], border_size_px=2, border_color="#000000", border_radius_px=10, border_hover_color="#0072B5", box_shadow=True)

    st.markdown("---")
    
    # 5. 데이터프레임 탐색기 (streamlit_extras.dataframe_explorer 활용)
    st.subheader(f"🗺️ 국가별 **{selected_mbti}** 유형 분포 상세 정보")
    
    # 비율을 백분율로 보기 쉽게 변환
    mbti_df_display = mbti_df.copy()
    mbti_df_display[selected_mbti] = (mbti_df_display[selected_mbti] * 100).round(2).astype(str) + ' %'
    
    # 데이터 탐색기 위젯 추가
    explorer = dataframe_explorer(mbti_df_display, case=False)
    st.dataframe(explorer, use_container_width=True, height=400)

    # 5. 차트 시각화
    st.markdown("---")
    st.subheader("📈 상위 10개 국가 분포 시각화")
    
    # 상위 10개 국가 데이터 준비
    top_10 = mbti_df.sort_values(by=selected_mbti, ascending=False).head(10)
    top_10['Proportion (%)'] = top_10[selected_mbti] * 100
    
    st.bar_chart(top_10['Proportion (%)'])

# --- Footer (Icon Set Library) ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center;'>
        <p style='font-size: 12px; color: gray;'>
            <i class="fas fa-magic"></i> Powered by Streamlit | 
            <i class="fab fa-python"></i> Python | 
            <i class="fab fa-font-awesome"></i> Font Awesome Icons
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
