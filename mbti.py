import streamlit as st
import pandas as pd
import base64

# --- 1. 파일 로드 및 설정 ---
# 첨부된 CSV 파일 로드
try:
    df = pd.read_csv('countriesMBTI_16types.csv')
    mbti_types = df.columns[1:].tolist() # MBTI 유형 리스트 (첫 번째 'Country' 제외)
except FileNotFoundError:
    st.error("Error: 'countriesMBTI_16types.csv' 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    st.stop()
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    st.stop()

# MBTI 설명 데이터 (간단하게 주요 특징만 포함)
mbti_descriptions = {
    "ISTJ": "🚀 현실적인 관리자: 사실에 근거하여 책임감이 강하고 논리적인 행동파입니다.",
    "ISFJ": "🏠 용감한 수호자: 성실하고 온정적이며, 타인을 돕는 데 헌신적입니다.",
    "INFJ": "🔮 선의의 옹호자: 통찰력이 뛰어나고, 조용하면서도 강한 신념을 가진 이상주의자입니다.",
    "INTJ": "🧠 용의주도한 전략가: 지적인 호기심이 많고, 분석적이며 독립적인 사고를 합니다.",
    "ISTP": "🛠️ 만능 재주꾼: 논리적이고 뛰어난 문제 해결 능력을 가진 관찰자입니다.",
    "ISFP": "🎨 호기심 많은 예술가: 유연하고 적응력이 좋으며, 예술적 감각이 뛰어납니다.",
    "INFP": "💡 열정적인 중재자: 상상력이 풍부하고, 자신의 가치관을 따르는 낭만주의자입니다.",
    "INTP": "🧐 논리적인 사색가: 지식에 대한 갈망이 강하고, 복잡한 문제 해결을 즐깁니다.",
    "ESTP": "🤸 모험을 즐기는 사업가: 에너지가 넘치고, 사교적이며, 실제적인 행동을 선호합니다.",
    "ESFP": "🥳 자유로운 영혼의 연예인: 즉흥적이고 활동적이며, 주변 사람들을 즐겁게 합니다.",
    "ENFP": "🌟 재기 발랄한 활동가: 창의적이고 사교적이며, 가능성을 탐색하는 데 열정적입니다.",
    "ENTP": "🗣️ 뜨거운 논쟁을 즐기는 변론가: 똑똑하고 지적인 도전을 즐기며, 새로운 아이디어를 추구합니다.",
    "ESTJ": "🏛️ 엄격한 관리자: 체계적이고 현실적이며, 리더십을 발휘하는 조직가입니다.",
    "ESFJ": "💖 사교적인 외교관: 사람들에게 관심이 많고, 조화로운 관계를 중요시하는 협력자입니다.",
    "ENFJ": "🦸 정의로운 사회운동가: 카리스마와 열정을 가지고, 타인의 성장을 돕는 리더입니다.",
    "ENTJ": "👑 대담한 통솔자: 도전적이고 단호하며, 장기적인 계획을 수립하고 실행하는 데 능합니다.",
}

# MBTI 통계 기반 멘트 생성 함수
def generate_compliment(mbti_type):
    """선택된 MBTI 유형에 기반한 멘트를 생성합니다."""
    # 통계 평균값 계산 (국가별 분포를 기반으로 '평균적인' 특징을 도출)
    avg_proportion = df[mbti_type].mean() * 100
    
    # 멘트 템플릿
    compliments = {
        "ISTJ": f"당신은 **책임감**과 **사실**에 대한 뛰어난 집중력을 가지고 계십니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이는, 신뢰할 수 있는 관리자 유형이시군요!",
        "ISFJ": f"당신은 **따뜻한 마음**과 **헌신**으로 주변 사람들을 돕는 수호자입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 타인의 안녕을 위해 노력하는 모습이 인상적입니다.",
        "INFJ": f"당신은 **깊은 통찰력**과 **이상적인 신념**을 가진 옹호자입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 조용히 세상을 바꾸는 힘을 가지고 있습니다.",
        "INTJ": f"당신은 **논리적인 전략**과 **독립적인 사고**로 목표를 달성하는 전략가입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 미래를 설계하는 데 탁월합니다.",
        "ISTP": f"당신은 **뛰어난 문제 해결 능력**과 **호기심**을 가진 만능 재주꾼입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 직접 행동하며 배우는 것을 즐깁니다.",
        "ISFP": f"당신은 **유연한 마음**과 **예술적인 감각**을 가진 자유로운 영혼입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 현재를 즐기고 아름다움을 창조하는 데 능합니다.",
        "INFP": f"당신은 **강한 가치관**과 **풍부한 상상력**을 가진 중재자입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 진정성 있는 관계를 추구합니다.",
        "INTP": f"당신은 **지식에 대한 갈망**과 **복잡한 아이디어**를 다루는 사색가입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 세상의 원리를 탐구하는 데 몰두합니다.",
        "ESTP": f"당신은 **에너지 넘치는 행동**과 **현실적인 판단력**을 가진 사업가입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 순간의 기회를 놓치지 않습니다.",
        "ESFP": f"당신은 **사교성과 재치**로 주변을 밝게 만드는 연예인입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 삶의 즐거움을 극대화하는 방법을 알고 있습니다.",
        "ENFP": f"당신은 **끝없는 가능성**과 **열정**을 가진 활동가입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 영감을 주고받는 것을 중요하게 생각합니다.",
        "ENTP": f"당신은 **논리적인 사고**와 **지적인 도전**을 즐기는 변론가입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 새로운 관점을 제시하는 데 탁월합니다.",
        "ESTJ": f"당신은 **체계적인 조직력**과 **명확한 리더십**을 가진 관리자입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 효율적인 실행을 중시합니다.",
        "ESFJ": f"당신은 **뛰어난 사교성**과 **조화**를 추구하는 외교관입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 공동체의 안정에 기여합니다.",
        "ENFJ": f"당신은 **강한 카리스마**와 **타인의 성장**을 돕는 리더입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 영감을 주는 존재입니다.",
        "ENTJ": f"당신은 **대담한 실행력**과 **목표 지향적**인 통솔자입니다. 세계 통계에서 평균 약 **{avg_proportion:.2f}%**의 분포를 보이며, 큰 그림을 그리고 달성하는 데 능합니다.",
    }
    return compliments.get(mbti_type, "선택하신 MBTI에 대한 맞춤 멘트를 준비 중입니다.")


# --- 5. 배경화면 설정 함수 ---
def set_background_image(image_file):
    """첨부된 이미지를 배경화면으로 설정합니다."""
    try:
        with open(image_file, "rb") as f:
            img_bytes = f.read()
        encoded = base64.b64encode(img_bytes).decode()
        
        # Streamlit 기본 스타일 오버라이드를 위한 Markdown 및 CSS 사용
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded}");
                background-size: cover;
                background-attachment: fixed; /* 스크롤 시 배경 고정 */
                background-position: center;
                color: white; /* 텍스트 색상 기본값 흰색으로 설정 (가독성을 위해) */
            }}
            /* 가독성 향상을 위해 메인 콘텐츠 영역의 배경을 약간 어둡게 설정 */
            .main > div {{
                background-color: rgba(0, 0, 0, 0.5); /* 검은색 반투명 오버레이 */
                padding: 10px;
                border-radius: 10px;
            }}
            /* 제목 및 텍스트 색상 설정 */
            h1, h2, h3, h4, .stText, .stMarkdown p, .stMarkdown li {{
                color: white !important; 
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("경고: 'dog.jpg' 배경 이미지를 찾을 수 없습니다. 기본 배경이 사용됩니다.")
    except Exception as e:
        st.warning(f"경고: 배경 이미지 설정 중 오류 발생: {e}")

# 'dog.jpg' 파일을 배경으로 설정
set_background_image('dog.jpg')


# --- 2. 웹앱 메인 구성 및 사용자 입력 ---
st.title("🐾 MBTI 탐험 웹 앱 (feat. 댕댕이)")
st.caption("선택하신 MBTI 유형에 대한 정보와 통계를 제공합니다.")

# 사이드바에 MBTI 선택 드롭다운 생성
with st.sidebar:
    st.header("✨ MBTI 선택")
    selected_mbti = st.selectbox(
        "당신의 MBTI 유형은 무엇인가요?",
        options=[""] + mbti_types, # 4. 처음 접속 시 공백/선택 안 함 상태로 시작
        index=0,
        format_func=lambda x: "👇 유형을 선택하세요" if x == "" else x
    )

# --- 4. 초기 화면 메시지 ---
if selected_mbti == "":
    st.info("⬆️ **왼쪽 사이드바**에서 당신의 **MBTI 유형**을 선택해 주세요!")
    # 가독성 향상을 위해 중앙 콘텐츠에 배경색 추가
    st.markdown("<style> .stApp > div:first-child > section:nth-child(2) { background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 10px; } </style>", unsafe_allow_html=True)

else:
    # --- 2. 해당하는 MBTI에 대한 설명 보여주기 ---
    st.header(f"🌟 {selected_mbti} : {mbti_descriptions.get(selected_mbti).split(': ')[0]}")
    st.markdown(f"**주요 특징:** {mbti_descriptions.get(selected_mbti).split(': ')[1]}")
    
    st.markdown("---")
    
    # --- 3. 통계 정보 보여주기 ---
    st.subheader("🌎 전 세계 MBTI 통계 분석")
    
    # MBTI별 통계 데이터 추출
    mbti_stats = df[['Country', selected_mbti]].copy()
    mbti_stats['Proportion (%)'] = mbti_stats[selected_mbti] * 100
    mbti_stats = mbti_stats.sort_values(by='Proportion (%)', ascending=False)
    
    # 멘트 생성 및 표시
    compliment_message = generate_compliment(selected_mbti)
    st.success(f"**맞춤 멘트:** {compliment_message}")
    
    st.markdown("---")

    # 통계 요약 (평균, 최대, 최소)
    avg_prop = mbti_stats['Proportion (%)'].mean()
    max_country = mbti_stats.iloc[0]['Country']
    max_prop = mbti_stats.iloc[0]['Proportion (%)']
    min_country = mbti_stats.iloc[-1]['Country']
    min_prop = mbti_stats.iloc[-1]['Proportion (%)']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="평균 분포율", value=f"{avg_prop:.2f}%")
    with col2:
        st.metric(label="최대 분포 국가", value=f"{max_country}", delta=f"{max_prop:.2f}%")
    with col3:
        st.metric(label="최소 분포 국가", value=f"{min_country}", delta=f"{min_prop:.2f}%", delta_color="inverse")
        
    st.markdown("---")
    
    # 데이터 시각화
    st.caption(f"국가별 **{selected_mbti}** 유형 분포 (%):")
    
    # Bar Chart로 분포 시각화
    st.bar_chart(mbti_stats.set_index('Country')['Proportion (%)'].head(20)) # 상위 20개 국가만 표시 (너무 많으면 차트가 복잡해지므로)
    
    # ERROR FIX: st.dataframe의 caption 인수를 st.caption으로 분리하여 수정
    st.caption("분포율 상위 10개 국가")
    st.dataframe(
        mbti_stats[['Country', 'Proportion (%)']].rename(columns={'Proportion (%)': f'{selected_mbti} 분포율 (%)'}).head(10),
        use_container_width=True,
        hide_index=True,
        # caption="분포율 상위 10개 국가" # 에러 발생 인수를 제거
    )
