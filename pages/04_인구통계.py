import streamlit as st
import pandas as pd
import plotly.express as px

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="cp949")
    # 숫자형 변환 (쉼표 제거)
    for col in df.columns[3:]:
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)
    return df

df = load_data()

# --- Streamlit UI ---
st.set_page_config(page_title="서울 인구 연령분포", layout="wide")

st.title("👥 서울 자치구별 연령대 인구 시각화 (2025년 10월 기준)")
st.markdown("지역구를 선택하면 연령별 인구 꺾은선 그래프가 표시됩니다.")

# --- 지역 선택 ---
regions = df["행정구역"].tolist()
selected_region = st.selectbox("📍 지역을 선택하세요", regions[1:], index=0)

# --- 데이터 필터링 ---
region_data = df[df["행정구역"] == selected_region].iloc[0, 3:]
ages = [col.replace("2025년10월_거주자_", "") for col in df.columns[3:]]
values = region_data.values

plot_df = pd.DataFrame({
    "연령": ages,
    "인구수": values
})

# --- Plotly 시각화 ---
fig = px.line(
    plot_df,
    x="연령",
    y="인구수",
    markers=True,
    title=f"📊 {selected_region} 연령별 인구 분포",
    template="plotly_white"
)

fig.update_layout(
    xaxis_title="나이",
    yaxis_title="인구수",
    hovermode="x unified",
    title_font=dict(size=20),
    margin=dict(l=40, r=40, t=60, b=40)
)

st.plotly_chart(fig, use_container_width=True)

# --- 요약 통계 ---
st.subheader("📈 인구 요약")
st.metric("총인구수", f"{df.loc[df['행정구역']==selected_region, '2025년10월_거주자_총인구수'].values[0]}")
