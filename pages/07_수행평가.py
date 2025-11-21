import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ----------------------------------------
# 데이터 불러오기
# ----------------------------------------
@st.cache_data
def load_data():
    csv_path = os.path.join("..", "people.csv")
    return pd.read_csv(csv_path, encoding="cp949")

df = load_data()

st.title("📊 시도·시군구별 남녀 인구 비교 대시보드")
st.write("시도명과 시군구명을 선택하면 남자·여자 인구를 막대 그래프로 비교할 수 있습니다.")

# ----------------------------------------
# 선택 UI
# ----------------------------------------
sido_list = sorted(df["시도명"].unique())
selected_sido = st.sidebar.selectbox("시도 선택", sido_list)

sgg_list = sorted(df[df["시도명"] == selected_sido]["시군구명"].unique())
selected_sgg = st.sidebar.selectbox("시군구 선택", sgg_list)

# ----------------------------------------
# 데이터 필터링
# ----------------------------------------
filtered = df[(df["시도명"] == selected_sido) & (df["시군구명"] == selected_sgg)]

# ----------------------------------------
# 막대그래프 데이터 구성
# ----------------------------------------
pop_data = {
    "성별": ["남자", "여자"],
    "인구수": [filtered["남자"].sum(), filtered["여자"].sum()]
}
pop_df = pd.DataFrame(pop_data)

# ----------------------------------------
# Plotly 막대그래프
# ----------------------------------------
fig = px.bar(
    pop_df,
    x="성별",
    y="인구수",
    title=f"📍 {selected_sido} {selected_sgg} 남녀 인구 비교",
    color="성별",
    color_discrete_map={"남자": "blue", "여자": "red"},
    text="인구수"
)

fig.update_layout(
    xaxis_title="성별",
    yaxis_title="인구수",
    template="simple_white"
)

# ----------------------------------------
# 출력
# ----------------------------------------
st.plotly_chart(fig, use_container_width=True)

with st.expander("📑 필터링된 원본 데이터 보기"):
    st.dataframe(filtered)
