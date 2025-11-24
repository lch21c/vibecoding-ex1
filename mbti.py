import streamlit as st
import pandas as pd
import base64
import altair as alt

# --- 설정 (Config) ---
# 16가지 MBTI 유형 목록
MBTI_TYPES = [
    "INFJ", "ISFJ", "INTP", "ISFP", "ENTP", "INFP", "ENTJ", "ISTP", 
    "INTJ", "ESFP", "ESTJ", "ENFP", "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

# MBTI별 간략 설명 (예시)
MBTI_DESCRIPTIONS = {
    "INFJ": "선의의 옹호자: 조용하고 신비로우며, 영감이 가득한 이상주의자입니다. 사람들에게 좋은 영향을 주고자 하는 열망이 강합니다.",
    "ISFJ": "용감한 수호자: 성실하고 헌신적이며, 다른 사람들을 보호할 책임감을 느낍니다. 세부 사항에 강하고 실질적인 도움을 줍니다.",
    "INTP": "논리적인 사색가: 지식에 대한 끝없는 갈증을 가진 혁신적인 발명가입니다. 복잡한 문제를 분석하고 해결하는 데 능숙합니다.",
    "ISFP": "호기심 많은 예술가: 항상 새로운 것을 탐험할 준비가 되어 있는 유연하고 매력적인 예술가입니다. 현재를 즐기며 자유롭습니다.",
    "ENTP": "뜨거운 논쟁을 즐기는 변론가: 지적인 도전을 즐기며, 아이디어를 현실로 만드는 데 열정적입니다. 틀을 깨는 데 주저하지 않습니다.",
    "INFP": "열정적인 중재자: 이타심이 강하고 이상적이며, 항상 선을 행할 방법을 찾는 조용하고 개방적인 영혼입니다.",
    "ENTJ": "대담한 통솔자: 타고난 리더로, 카리스마와 자신감을 가지고 목표를 달성합니다. 장기적인 계획을 세우고 실행합니다.",
    "ISTP": "만능 재주꾼: 능숙하고 대담하며, 손으로 만드는 것을 즐기는 현실적인 실험가입니다. 기계와 도구를 잘 다룹니다.",
    "INTJ": "용의주도한 전략가: 상상력이 풍부하고 결단력이 있으며, 모든 것에 대한 계획을 세우는 전략적인 사령관입니다.",
    "ESFP": "자유로운 연예인: 즉흥적이고 활동적이며, 주변에 생기와 재미를 불어넣는 사람들입니다. 주목받는 것을 즐깁니다.",
    "ESTJ": "엄격한 관리자: 질서와 전통을 존중하며, 올바른 일을 하는 데 헌신하는 훌륭한 행정가입니다. 조직적이고 효율적입니다.",
    "ENFP": "재기 발랄한 활동가: 창의적이고 사교적이며, 항상 새로운 가능성을 찾고 삶을 하나의 큰 퍼즐로 보는 사람들입니다.",
    "ESTP": "모험을 즐기는 사업가: 영리하고 에너지가 넘치며, 위험을 감수하는 것을 두려워하지 않는 현실주의자입니다. 행동 지향적입니다.",
    "ISTJ": "청렴결백한 논리주의자: 사실에 기반을 두고 실용적이며, 책임감이 강한 성실한 논리주의자입니다. 전통을 중요시합니다.",
    "ENFJ": "정의로운 사회운동가: 타인을 이끌고 격려하는 데 능숙하며, 카리스마 있고 영감을 주는 리더입니다. 사람들의 성장을 돕습니다.",
    "ESFJ": "사교적인 외교관: 배려심이 깊고 사교적이며, 사람들을 돕고 공동체를 유지하는 데 헌신하는 인기인입니다.",
}

# 통계 기반 맞춤 멘트 함수
def generate_mbti_comment(mbti_type, avg_ratio):
    """선택된 MBTI의 국가별 평균 비율에 따라 다른 멘트를 생성합니다."""
    
    # 평균 비율을 백분율로 포맷
    avg_percent = f"**{avg_ratio*100:.2f}%**"
    
    # MBTI 그룹별 특징에 맞는 멘트
    if avg_ratio >= 0.07:  # 비교적 높은 비율 (상위 25% 내외)
        group_encouragement = f"🎉 많은 나라에서 당신의 MBTI **{mbti_type}** 유형의 비율은 평균 {avg_percent}로 **상당히 높은 편**입니다. 이는 당신의 성향이 많은 곳에서 자연스럽게 발현되며, 세상에 긍정적인 영향을 미치고 있음을 의미해요! 당신은 사회에 꼭 필요한 존재입니다."
    elif avg_ratio <= 0.04:  # 비교적 낮은 비율 (하위 25% 내외)
        group_encouragement = f"🌟 당신의 MBTI **{mbti_type}** 유형은 평균 {avg_percent}로 **매우 희소한 편**에 속합니다. 당신의 독특한 관점과 특별한 재능은 세상이 놓치고 있는 새로운 통찰을 제공할 수 있어요. 당신의 특별함이 세상을 바꿀 수 있습니다!"
    else:  # 중간 비율
        group_encouragement = f"👍 당신의 MBTI **{mbti_type}** 유형은 평균 {avg_percent}로 **적절한 균형**을 이루고 있습니다. 당신은 유연하게 다양한 사회에서 자신의 역할을 찾아낼 수 있는 능력을 가지고 있어요. 지금처럼 꾸준히 나아가세요!"
        
    return group_encouragement

# 배경 이미지 설정 함수
def set_background(image_path):
    """로컬 이미지를 사용하여 Streamlit 배경 스타일을 설정합니다."""
    try:
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        
        # Streamlit 배경 스타일 설정 (CSS)
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{data}");
                background-size: cover;
                background-attachment: fixed; /* 스크롤해도 배경 고정 */
                background-position: center;
                color: #333333; /* 텍스트 색상을 배경과 대비되도록 조정 */
            }}
            /* 메인 콘텐츠 영역에 투명한 배경을 추가하여 텍스트 가독성 높이기 */
            .main > div {{
                background-color: rgba(255, 255, 255, 0.9); /* 흰색, 90% 투명도 */
                padding: 20px;
                border-radius: 10px;
            }}
            /* 사이드바도 가독성 향상 */
            [data-testid="stSidebar"] {{
                background-color: rgba(240, 240, 240, 0.95); /* 회색, 95% 투명도 */
            }}
            h1, h2, h3, .stMarkdown, .stText {{
                color: #1e1e1e !important; 
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error(f"⚠️ **오류**: 파일 '{image_path}'를 찾을 수 없습니다. 경로를 확인해 주세요.")

# --- 데이터 로드 및 전처리 ---
@st.cache_data
def load_data(file_path):
    """CSV 파일을 로드하고 국가별 MBTI 평균 비율을 계산합니다."""
    try:
        df = pd.read_csv(file_path)
        # 국가 컬럼을 인덱스로 설정하거나, 여기서는 제거 후 비율만 사용
        data_df = df.set_index('Country').copy()
        # 전체 16개 MBTI 비율의 평균 계산
        mbti_avg_ratios = data_df.mean().sort_values(ascending=False)
        return mbti_avg_ratios
    except Exception as e:
        st.error(f"⚠️ **데이터 로드 중 오류 발생**: {e}")
        return None

# --- Streamlit 앱 메인 함수 ---
def main():
    # 5. 웹앱의 배경화면 설정
    set_background("dog.jpg") 

    st.title("🐶 MBTI 분석 및 응원 웹앱")
    st.markdown("---")

    # 데이터 로드
    mbti_avg_ratios = load_data("countriesMBTI_16types.csv")

    # 2. 사용자에게 MBTI를 선택하게 함
    selected_mbti = st.selectbox(
        "✨ **당신의 MBTI 유형을 선택해 주세요:**",
        options=[""] + MBTI_TYPES, # 첫 항목을 빈 문자열로 설정하여 초기 선택 없음을 표현
        index=0, # 첫 항목(빈 문자열)이 기본으로 선택되도록 설정
        format_func=lambda x: "--- MBTI 선택 ---" if x == "" else x
    )

    st.markdown("---")

    # 4. 처음 접속했을 때 (MBTI가 선택되지 않았을 때) 메시지 표시
    if selected_mbti == "":
        st.info("⬆️ **MBTI를 선택하시면, 당신의 유형에 대한 흥미로운 분석 결과를 보여 드립니다!**")
        return # MBTI가 선택되지 않았으므로 여기서 함수 종료

    # --- MBTI 선택 후 로직 ---
    if mbti_avg_ratios is not None:
        
        # 2. 선택된 MBTI에 대한 설명 표시
        st.header(f"🧠 {selected_mbti} 유형 설명")
        st.success(MBTI_DESCRIPTIONS.get(selected_mbti, "설명을 찾을 수 없습니다."))

        st.markdown("---")
        
        # 3. 첨부한 파일을 활용하여 통계 정보 표시 및 멘트 생성
        
        # 선택된 MBTI의 평균 비율
        selected_ratio = mbti_avg_ratios.loc[selected_mbti]
        
        st.header(f"📊 {selected_mbti} 유형의 글로벌 통계 분석")
        
        # 통계 시각화 (Altair 사용)
        chart_data = mbti_avg_ratios.reset_index()
        chart_data.columns = ['MBTI', 'Average_Ratio']
        
        # 선택된 MBTI 강조를 위한 하이라이트 컬럼 추가
        chart_data['Highlight'] = chart_data['MBTI'] == selected_mbti
        
        # Altair 막대 그래프 생성
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('MBTI:N', sort=MBTI_TYPES, title="MBTI 유형"),
            y=alt.Y('Average_Ratio:Q', title="국가별 평균 비율"),
            # 선택된 MBTI에 따라 색상 변경
            color=alt.condition(
                alt.datum.Highlight,
                alt.value('darkred'),  # 선택된 MBTI 색상
                alt.value('steelblue') # 다른 MBTI 색상
            ),
            tooltip=['MBTI', alt.Tooltip('Average_Ratio', format='.2%')]
        ).properties(
            title="16가지 MBTI 유형의 국가별 평균 비율 비교",
            width=700,
            height=300
        ).interactive() # 줌/패닝 기능 추가

        st.altair_chart(chart, use_container_width=True)

        # 분석 결과 요약
        st.subheader("💡 분석 결과 요약")
        st.metric(
            label=f"**{selected_mbti}** 유형의 국가별 평균 비율", 
            value=f"{selected_ratio*100:.2f} %", 
            delta=None # 변화량은 필요 없으므로 None
        )

        # 멘트 생성 및 표시
        st.markdown("---")
        st.header("💌 당신에게 드리는 응원의 메시지")
        st.markdown(generate_mbti_comment(selected_mbti, selected_ratio))
        
    else:
        st.error("데이터를 불러오는 데 실패하여 분석을 진행할 수 없습니다.")

# 앱 실행
if __name__ == "__main__":
    main()
