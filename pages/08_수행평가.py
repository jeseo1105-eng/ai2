import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("인구 데이터 시각화")

# File upload
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="cp949")

    # Sidebar selections
    st.sidebar.header("필터 선택")
    selected_sido = st.sidebar.selectbox("시도명", sorted(df["시도명"].dropna().unique()))
    filtered_sido = df[df["시도명"] == selected_sido]

    selected_sigungu = st.sidebar.selectbox(
        "시군구명", sorted(filtered_sido["시군구명"].dropna().unique())
    )
    filtered = filtered_sido[filtered_sido["시군구명"] == selected_sigungu]

    # Aggregate male/female counts
    male_sum = filtered["남자"].sum()
    female_sum = filtered["여자"].sum()

    plot_df = pd.DataFrame({
        "성별": ["남자", "여자"],
        "인구수": [male_sum, female_sum]
    })

    # Plotly bar chart
    fig = px.bar(
        plot_df,
        x="성별",
        y="인구수",
        color="성별",
        color_discrete_map={"남자": "blue", "여자": "pink"},
        title=f"{selected_sido} {selected_sigungu} 남녀 인구 수"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("좌측에 CSV 파일을 업로드하세요.")

# Requirements for deployment
# Requirements for deployment outside streamlit app
st.subheader("requirements.txt")
st.code("""
streamlit
pandas
plotly
""", language="text")

st.subheader("requirements.txt 예시")
st.code("""
streamlit
pandas
plotly
""", language="text")
