import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="연령대별 범죄 피해자 수", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("pppppp.csv", encoding="cp949")
    return df

def main():
    st.title("연령대별 범죄 피해자 수 시각화 대시보드")
    st.write("연령대를 선택하면, 해당 연령대의 **지역/구분별 피해자 수**를 막대그래프로 보여줍니다.")

    df = load_data()

    # 연령 선택
    age_options = sorted(df["연령"].dropna().unique())
    selected_age = st.selectbox("연령대를 선택하세요", age_options)

    # 필터된 데이터
    filtered = df[df["연령"] == selected_age].copy()

    if filtered.empty:
        st.warning("선택한 연령대에 해당하는 데이터가 없습니다.")
        return

    # 구분별 피해자 수 집계
    grouped = (
        filtered.groupby("구분", as_index=False)["피해자 수"]
        .sum()
        .sort_values("피해자 수", ascending=False)
    )

    st.subheader("선택한 연령대의 구분별 피해자 수")

    st.dataframe(grouped)

    # 색상 설정
    n = len(grouped)

    # 1등 빨강, 2~11등까지 그라데이션 (최대 10개)
    gradient_count = min(10, n - 1)

    base_colors = px.colors.sequential.Blues
    gradient_colors = base_colors[-gradient_count:]  # 진→연 순으로

    colors = ["red"]  # 1등

    # 그라데이션 색 10개까지 추가
    colors.extend(gradient_colors)

    # 나머지는 회색(#D3D3D3)
    remaining = n - 1 - gradient_count
    if remaining > 0:
        colors.extend(["#D3D3D3"] * remaining)

    # Plotly 그래프
    fig = go.Figure(
        data=[
            go.Bar(
                x=grouped["구분"],
                y=grouped["피해자 수"],
                marker_color=colors,
                hovertemplate="구분: %{x}<br>피해자 수: %{y}명<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title=f"연령대: {selected_age} - 구분별 피해자 수",
        xaxis_title="구분(지역 + 범죄유형)",
        yaxis_title="피해자 수",
        xaxis_tickangle=-45,
        hovermode="x unified",
    )

    st.subheader("막대 그래프")
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
