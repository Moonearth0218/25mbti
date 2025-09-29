import streamlit as st
import pandas as pd

# 제목
st.title("🌍 국가별 MBTI 분포 데이터 미리보기")

# CSV 불러오기 (같은 폴더에 저장되어 있다고 가정)
df = pd.read_csv("countriesMBTI_16types.csv")

# 상위 5줄만 보여주기
st.subheader("상위 5개 데이터")
st.dataframe(df.head())

