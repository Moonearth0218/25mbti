import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 MBTI 비율", page_icon="🌍", layout="centered")
st.title("🌍 나라를 선택하면 MBTI 분포가 보여요")
st.caption("국가별 16가지 MBTI 유형 비율(%)을 한눈에 확인하세요. 📊")

# 데이터 불러오기
@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    # MBTI 컬럼만 미리 보관
    mbti_cols = [
        "INFJ","ISFJ","INTP","ISFP","ENTP","INFP","ENTJ","ISTP",
        "INTJ","ESFP","ESTJ","ENFP","ESTP","ISTJ","ENFJ","ESFJ"
    ]
    return df, mbti_cols

df, MBTI_TYPES = load_data("countriesMBTI_16types.csv")

# 사이드바: 나라 선택
with st.sidebar:
    st.header("🔎 나라 선택")
    country = st.selectbox(
        "국가를 고르세요",
        sorted(df["Country"].unique().tolist()),
        index=0
    )
    sort_desc = st.toggle("값 큰 순으로 정렬", value=True)
    st.caption("Tip: 정렬을 바꿔보며 유형 분포를 비교해 보세요 😉")

# 선택한 나라의 MBTI 비율 추출
row = df.loc[df["Country"] == country].iloc[0]
data = pd.DataFrame({
    "MBTI": MBTI_TYPES,
    "Ratio": [row[c] for c in MBTI_TYPES]
})

# 정렬
data = data.sort_values("Ratio", ascending=not sort_desc).reset_index(drop=True)

# 표 (퍼센트로 보기 좋게)
st.subheader(f"🗺️ {country}의 MBTI 비율 (표)")
st.dataframe(
    data.assign(비율=(data["Ratio"]*100).round(2)).drop(columns=["Ratio"]).rename(columns={"MBTI":"유형"}),
    use_container_width=True
)

# Plotly 막대그래프
st.subheader(f"📈 {country}의 MBTI 분포 (막대 그래프)")
# 예쁜 파스텔 팔레트
palette = px.colors.qualitative.Set3  # 깔끔·파스텔톤
fig = px.bar(
    data,
    x="MBTI",
    y="Ratio",
    color="MBTI",
    color_discrete_sequence=palette,
    hover_data={"Ratio":":.2%","MBTI":True},
    text=data["Ratio"].map(lambda x: f"{x*100:.1f}%")
)
fig.update_traces(textposition="outside", cliponaxis=False)
fig.update_layout(
    yaxis_title="비율",
    xaxis_title="MBTI 유형",
    yaxis_tickformat=".0%",
    uniformtext_minsize=10,
    uniformtext_mode="show",
    margin=dict(l=20, r=20, t=40, b=20),
    legend_title="MBTI"
)
# 여유 공간(상단) 확보
ymax = max(0.25, data["Ratio"].max()*1.2)
fig.update_yaxes(range=[0, ymax])

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
    **설명**  
    - 값은 0~1 범위의 비율로 제공되어, 그래프와 표에서는 %로 변환하여 표시합니다.  
    - 🧭 색상은 유형별로 구분을 쉽게 하기 위해 파스텔 팔레트를 사용했습니다.  
    - 🔁 사이드바에서 정렬 옵션을 바꿔 보며 상·하위 유형을 빠르게 파악할 수 있어요.
    """
)
