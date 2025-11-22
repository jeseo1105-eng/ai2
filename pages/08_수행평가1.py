import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="연령대별 범죄 피해자 수", layout="wide")

@st.cache_data
def load_data():
    # 공공데이터포털에서 받은 CSV가 보통 cp949/euc-kr 인코딩이라서 이렇게 읽어줌
    df = pd.read_csv("pppppp.csv", encoding="cp949")
    return df

def main():
    st.title("연령대별 범죄 피해자 수 시각화 대시보드")
    st.write("연령대를 선택하면, 해당 연령대의 **지역/구분별 피해자 수**를 막대그래프로 보여줍니다.")

    df = load_data()

    # 기본 정보 간단 표시
    st.subheader("데이터 미리보기")
    st.dataframe(df.head())

    # 연령대 선택 위젯
    st.subheader("1. 연령대 선택")
    age_options = sorted(df["연령"].dropna().unique())
    selected_age = st.selectbox("연령대를 선택하세요", age_options)

    # 선택한 연령대로 필터링
    filtered = df[df["연령"] == selected_age].copy()

    if filtered.empty:
        st.warning("선택한 연령대에 해당하는 데이터가 없습니다.")
        return

    # 구분(지역+범죄유형)별 피해자 수 합산
    grouped = (
        filtered.groupby("구분", as_index=False)["피해자 수"]
        .sum()
        .sort_values("피해자 수", ascending=False)
    )

    st.subheader("2. 선택한 연령대의 구분별 피해자 수")
    st.dataframe(grouped)

    # 색 지정: 1등은 빨간색, 나머지는 그라데이션 느낌
    n = len(grouped)
    if n == 0:
        st.warning("그래프로 표시할 데이터가 없습니다.")
        return

    # plotly의 연속 색상 팔레트 사용 (예: Blues)
    base_colors = px.colors.sequential.Blues

    # 필요한 개수만큼 색을 뽑아오기 (1등은 빨강, 나머지 n-1개)
    if n - 1 <= len(base_colors):
        other_colors = base_colors[-(n - 1):]  # 뒤에서부터 사용해서 진→연 느낌
    else:
        # 데이터가 더 많으면 색 반복
        other_colors = [base_colors[i % len(base_colors)] for i in range(n - 1)]

    colors = ["red"] + other_colors  # 1등: 빨간색

    # Plotly 막대 그래프 생성
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

    st.subheader("3. 막대 그래프")
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
