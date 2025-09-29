import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="MBTI 상위 10개 국가", page_icon="🧭", layout="centered")
st.title("🧭 MBTI 유형별 상위 10개 국가")

# 데이터 불러오기 (같은 폴더에 CSV가 있다고 가정)
CSV_PATH = "countriesMBTI_16types.csv"
df = pd.read_csv(CSV_PATH)

# MBTI 컬럼 목록 (CSV 컬럼명과 동일하게)
MBTI_TYPES = [
    "INFJ", "ISFJ", "INTP", "ISFP", "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP", "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

# 사이드바에서 MBTI 선택
with st.sidebar:
    st.header("옵션")
    mbti = st.selectbox("MBTI 유형 선택", MBTI_TYPES, index=0)
    st.caption("선택한 MBTI 유형의 비율이 높은 상위 10개 국가를 보여줍니다.")

# 선택한 MBTI 기준 상위 10개 국가 추출
top10 = (
    df[["Country", mbti]]
    .nlargest(10, mbti)
    .sort_values(mbti, ascending=True)  # 그래프에서 위에서 아래로 큰 값이 오도록
)

st.subheader(f"🔝 {mbti} 상위 10개 국가")
st.dataframe(top10.rename(columns={mbti: f"{mbti} 비율"}), use_container_width=True)

# Altair 막대 그래프
chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X(f"{mbti}:Q", title=f"{mbti} 비율", axis=alt.Axis(format=".1%")),
        y=alt.Y("Country:N", sort="-x", title="국가"),
        tooltip=[
            alt.Tooltip("Country:N", title="국가"),
            alt.Tooltip(f"{mbti}:Q", title=f"{mbti} 비율", format=".2%")
        ]
    )
    .properties(width=700, height=400)
)

st.altair_chart(chart, use_container_width=True)

st.markdown(
    """
    **설명**
    - 값은 각 국가의 MBTI 유형 비율(0~1)로 가정하여 %로 표시합니다.  
    - 사이드바에서 다른 MBTI 유형을 선택해 비교해 보세요.
    """
)
