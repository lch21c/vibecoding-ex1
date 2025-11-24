import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.badges import badge

# 아이콘셋 라이브러리 설치 필요: pip install streamlit-antd-components
# 아이콘셋은 `streamlit-antd-components` 라이브러리를 사용하며, Streamlit의 기본 기능에 포함되어 있지 않으므로 별도 설치가 필요합니다.
# 코드에서는 기본 이모지나 Streamlit의 기본 아이콘을 사용하고, 별도로 설치해야 하는 라이브러리를 요구사항 파일에 명시했습니다.
# 만약 더 많은 아이콘이 필요하다면 `streamlit-antd-components`를 설치하고 사용해 주세요.

# --- 데이터 로드 및 전처리 ---
@st.cache_data
def load_data(file_path):
    """CSV 파일을 로드하고 캐싱합니다."""
    # 파일명은 'countriesMBTI_16types.csv'로 가정
    try:
        df = pd.read_csv(file_path)
        # 국가 이름을 인덱스로 설정
        df = df.set_index('Country')
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# 데이터 로드 (업로드된 파일명을 사용)
DATA_FILE = "countriesMBTI_16types.csv"
mbti_df = load_data(DATA_FILE)

# MBTI 유형 리스트
mbti_types = list(mbti_df.columns)

# MBTI별 설명 (간단 버전)
mbti_descriptions = {
    "INFJ": ("옹호자 🕊️", "선의의 옹호자. 차분하고 신비하며 영감을 주는 이상주의자."),
    "ISFJ": ("수호자 🛡️", "용감하고 헌신적인 수호자. 공동체를 보호하는 따뜻한 사람."),
    "INTP": ("논리술사 🧠", "끊임없이 지식을 탐구하는 혁신가. 뛰어난 지적 호기심을 가짐."),
    "ISFP": ("모험가 🎨", "새로운 것을 탐구하는 유연하고 매력적인 예술가. 항상 현재를 즐김."),
    "ENTP": ("변론가 😈", "지적인 도전을 즐기는 독창적이고 대담한 변론가. 항상 논쟁할 준비가 되어 있음."),
    "INFP": ("중재자 ✨", "항상 선을 행할 방법을 찾는 조용하고 이상주의적인 영혼."),
    "ENTJ": ("대담한 통솔자 👑", "강력한 의지의 소유자. 목표 달성을 위해 계획을 세우는 지도자."),
    "ISTP": ("만능 재주꾼 🛠️", "주변의 도구를 마스터하는 숙련된 기술자. 실용적이고 논리적임."),
    "INTJ": ("건축가 🏰", "상상력이 풍부하고 전략적인 사상가. 모든 것에 대한 계획을 세움."),
    "ESFP": ("연예인 🌟", "삶의 중심에서 주변 사람들에게 기쁨을 주는 자발적이고 활기찬 사람."),
    "ESTJ": ("경영자 👔", "질서를 만들고 관리하는 우수한 행정가. 전통을 존중함."),
    "ENFP": ("활동가 🌈", "열정적이고 창의적인 사교적인 자유로운 영혼. 삶을 즐거움으로 봄."),
    "ESTP": ("사업가 🚀", "에너지가 넘치고 영리하며, 항상 위험을 감수하는 행동파."),
    "ISTJ": ("현실주의자 🧱", "사실에 충실한 실용적인 논리적 분석가. 책임감이 강함."),
    "ENFJ": ("선도자 💖", "카리스마 넘치고 영감을 주는 지도자. 다른 사람들에게 영향을 미치고자 함."),
    "ESFJ": ("친선 도모가 🤝", "주변 사람들을 돌보는 매우 사교적인 인기인. 공동체의 결속력을 다짐.")
}

# --- 스트림릿 웹 앱 구성 ---
st.set_page_config(
    page_title="MBTI 통계 분석 웹 앱",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바: MBTI 선택
with st.sidebar:
    st.title("🔎 MBTI 유형 선택")
    
    # 뱃지 추가 (streamlit-extras.badges)
    badge(type="dark", text="Data Source: Global MBTI Statistics")
    
    selected_mbti = st.selectbox(
        "분석하고 싶은 MBTI를 선택하세요.",
        options=[""] + mbti_types, # 초기에는 빈 문자열
        index=0,
        format_func=lambda x: "--- 선택하세요 ---" if x == "" else x
    )

# 메인 화면: 선택된 MBTI에 따른 콘텐츠 표시
st.title("🌟 MBTI 글로벌 통계 분석 웹 앱")

# 사용자에게 MBTI 선택을 요청하는 초기 화면
if selected_mbti == "":
    st.header("👋 환영합니다!")
    st.info("👈 왼쪽 사이드바에서 **MBTI 유형을 선택**하여 해당 유형의 설명과 글로벌 통계 분석 결과를 확인하세요.")
    # 실제 이미지가 없으므로, 플레이스홀더 주소를 사용했습니다.
    st.image("https://i.imgur.com/G0G0K0D.png", caption="MBTI 유형 선택을 기다리고 있어요.", use_column_width=True) 

else:
    # --- 선택된 MBTI 정보 표시 ---
    mbti_name = selected_mbti
    mbti_title, mbti_desc = mbti_descriptions.get(mbti_name, ("알 수 없음", "정보를 찾을 수 없습니다."))
    
    # 헤더 색상 변경 (streamlit-extras.colored_header)
    colored_header(
        label=f"{mbti_name} : {mbti_title}",
        description="선택하신 MBTI 유형에 대한 간략한 설명입니다.",
        color_name="blue-70"
    )

    st.markdown(f"**{mbti_desc[0]}**")
    st.info(mbti_desc[1])

    # --- 통계 분석 섹션 ---
    st.header(f"📊 {mbti_name} 글로벌 통계")
    
    if not mbti_df.empty and mbti_name in mbti_df.columns:
        
        # 1. 글로벌 평균 비율 계산
        global_avg = mbti_df[mbti_name].mean()
        
        # 2. 가장 비율이 높은 상위 5개 국가
        top_5_countries = mbti_df[mbti_name].nlargest(5)
        
        # 3. 가장 비율이 낮은 하위 5개 국가
        bottom_5_countries = mbti_df[mbti_name].nsmallest(5)
        
        # Metric Cards 스타일 적용 (streamlit-extras.metric_cards)
        style_metric_cards(background_color="#FFFFFF", border_left_color="#1f77b4", border_radius_px=10, box_shadow=True)

        col1, col2, col3 = st.columns(3)
        
        # Metric Card 1: 글로벌 평균
        col1.metric(
            label="🌍 글로벌 평균 비율",
            value=f"{global_avg * 100:.2f}%",
            delta=None, # 변화량은 생략
            help=f"**{mbti_name}** 유형이 전 세계 국가에서 평균적으로 차지하는 비율입니다."
        )

        # Metric Card 2: 최고 비율 국가
        top_country = top_5_countries.index[0]
        top_ratio = top_5_countries.iloc[0] * 100
        col2.metric(
            label="🥇 최고 비율 국가",
            value=f"{top_country} ({top_ratio:.2f}%)",
            delta=f"평균 대비 {(top_ratio - global_avg * 100):.2f}% 높음",
            delta_color="normal"
        )
        
        # Metric Card 3: 최저 비율 국가
        bottom_country = bottom_5_countries.index[0]
        bottom_ratio = bottom_5_countries.iloc[0] * 100
        col3.metric(
            label="🥉 최저 비율 국가",
            value=f"{bottom_country} ({bottom_ratio:.2f}%)",
            delta=f"평균 대비 {(bottom_ratio - global_avg * 100):.2f}% 낮음",
            delta_color="inverse"
        )

        st.markdown("---")
        
        # --- 시각화 (Plotly) ---
        
        # Stylable Container로 시각화 영역 스타일링 (streamlit-extras.stylable_container)
        with stylable_container(
            key="ranking_chart",
            css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: 1rem;
                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                }
                """,
        ):
            st.subheader(f"🌐 상위/하위 국가 비율 비교 (Top 5 vs Bottom 5)")
            
            # 상위 5개와 하위 5개 데이터를 합치기
            ranking_data = pd.concat([top_5_countries, bottom_5_countries])
            ranking_data = ranking_data.reset_index().rename(columns={'index': 'Country', mbti_name: 'Ratio'})
            ranking_data['Rank'] = ranking_data['Ratio'].apply(
                lambda x: 'Top 5' if x >= top_5_countries.min() else 'Bottom 5'
            )
            ranking_data['Ratio_Percent'] = ranking_data['Ratio'] * 100

            # 막대 그래프 (Bar Chart)
            fig = px.bar(
                ranking_data, 
                x='Country', 
                y='Ratio_Percent', 
                color='Rank',
                title=f"**{mbti_name}** 비율이 높은/낮은 국가 순위",
                labels={'Ratio_Percent': f'{mbti_name} 비율 (%)', 'Country': '국가'},
                color_discrete_map={'Top 5': '#2ecc71', 'Bottom 5': '#e74c3c'}, # 색상 지정
                hover_data={'Ratio_Percent': ':.2f'}
            )
            fig.update_layout(xaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        
        # --- 멘트 생성 ---
        st.subheader("💬 맞춤 멘트")
        
        # 멘트 로직 (예시)
        if global_avg > mbti_df[mbti_df.columns].mean().mean(): # 전체 MBTI 유형의 글로벌 평균 비율의 평균보다 높은 경우
            ment = f"**{mbti_name}** 유형은 글로벌 평균 대비 상대적으로 **많은** 국가에서 높은 비율을 보이고 있습니다. 당신의 유형은 전 세계적으로 **뚜렷한 존재감**을 드러내고 있네요! 이 유형이 가진 **{mbti_title}**의 특징이 많은 곳에서 요구되거나 중요하게 여겨지는 것 같습니다."
            st.success(f"🎉 글로벌 **주류**의 힘: {ment}")
        else:
            ment = f"**{mbti_name}** 유형은 글로벌 평균 대비 상대적으로 **적은** 국가에서 높은 비율을 보이고 있습니다. 당신의 유형은 전 세계적으로 **희소성**을 가진 **특별한 유형**입니다! 당신의 **{mbti_title}**로서의 독특한 관점과 재능이 빛을 발할 수 있는 곳을 찾아보세요."
            st.warning(f"💎 글로벌 **희소성**의 가치: {ment}")

    else:
        st.error("데이터프레임에 오류가 있거나 선택한 MBTI 유형에 대한 열이 없습니다.")

# --- 코드 실행 방법 안내 ---
st.sidebar.markdown("---")
st.sidebar.caption("👆 MBTI 유형을 선택하여 분석을 시작하세요.")
