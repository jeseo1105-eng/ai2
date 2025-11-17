# app.py
# Streamlit Cloud에서 바로 돌아가도록 작성한 앱입니다.
# - subway.csv 파일이 앱 루트에 있으면 자동으로 사용합니다.
# - 없으면 파일 업로드(사용자 제공)로 대체됩니다.
# - 2025-10-01 ~ 2025-10-31 사이의 날짜(하루)와 노선 선택 후 TOP10 막대그래프 출력.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from datetime import date, datetime

st.set_page_config(page_title="지하철 승하차 TOP10 (2025-10)", layout="wide")

st.title("📊 지하철 승차+하차 합계 TOP 10 — 2025년 10월")
st.write("날짜와 호선을 선택하면 해당 조건에서 승차+하차 합계가 큰 역 10개를 막대그래프로 보여줍니다.")

# --- 데이터 로드 함수 ---
@st.cache_data
def load_csv(path=None, uploaded_file=None):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception:
            # 인코딩 이슈 대비
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding="cp949")
        return df
    if path is not None and os.path.exists(path):
        try:
            df = pd.read_csv(path)
        except Exception:
            df = pd.read_csv(path, encoding="cp949")
        return df
    return None

# 기본 파일 경로 (Streamlit Cloud에 파일을 같이 올려둘 경우)
DEFAULT_PATH = "subway.csv"

uploaded = st.file_uploader("CSV 파일 업로드 (없으면 프로젝트 루트의 subway.csv 사용)", type=["csv"])

df = load_csv(path=DEFAULT_PATH, uploaded_file=uploaded)

if df is None:
    st.warning("데이터가 없습니다. 왼쪽 위에서 CSV 파일을 업로드하거나 프로젝트 루트에 subway.csv 파일을 올려주세요.")
    st.stop()

# 컬럼명 표준화 (예상 컬럼명을 영어로 바꾸지는 않고 기존 한글 컬럼 사용)
# 사용일자 컬럼이 int(YYYYMMDD) 혹은 문자열이면 날짜형으로 변환
if '사용일자' not in df.columns:
    st.error("CSV에 '사용일자' 컬럼이 필요합니다.")
    st.stop()

# 사용일자 처리: 숫자/문자열 모두 처리해서 datetime으로 변환
def parse_yyyymmdd(x):
    try:
        x = str(int(x))
    except Exception:
        x = str(x)
    # 보통 '20251001' 포맷
    try:
        return datetime.strptime(x, "%Y%m%d").date()
    except Exception:
        # 혹시 YYYY-MM-DD 형태면 처리
        try:
            return datetime.strptime(x, "%Y-%m-%d").date()
        except Exception:
            return None

df['사용일자_dt'] = df['사용일자'].apply(parse_yyyymmdd)
df = df.dropna(subset=['사용일자_dt'])

# 날짜 범위를 2025-10-01 ~ 2025-10-31로 제한 (UI에서 선택 가능하게)
min_date = date(2025, 10, 1)
max_date = date(2025, 10, 31)

# 날짜 위젯 (단일 날짜)
selected_date = st.date_input("1) 날짜 선택 (2025년 10월 중 하루)", value=min_date, min_value=min_date, max_value=max_date)

# 노선 선택: 데이터에 있는 노선 목록으로
line_options = sorted(df['노선명'].astype(str).unique())
selected_line = st.selectbox("2) 호선 선택", ["전체 (All)"] + line_options, index=0)

# 필터링
filtered = df[df['사용일자_dt'] == selected_date]
if selected_line != "전체 (All)":
    filtered = filtered[filtered['노선명'].astype(str) == selected_line]

if filtered.empty:
    st.info("선택된 날짜/호선에 해당하는 데이터가 없습니다. CSV 파일 내용을 확인하거나 다른 날짜/호선을 선택하세요.")
    st.stop()

# 승차 + 하차 합계 컬럼 생성 (컬럼 이름이 다를 경우 예외처리)
for col in ['승차총승객수', '하차총승객수']:
    if col not in filtered.columns:
        st.error(f"CSV에 '{col}' 컬럼이 필요합니다.")
        st.stop()

filtered['합계'] = filtered['승차총승객수'].astype(int) + filtered['하차총승객수'].astype(int)

# 역별 합계 집계 (동일 역이 중복될 수 있으니 groupby)
agg = (
    filtered
    .groupby(['노선명', '역명'], as_index=False)
    .agg({'승차총승객수': 'sum', '하차총승객수': 'sum', '합계': 'sum'})
    .sort_values('합계', ascending=False)
)

top10 = agg.head(10).reset_index(drop=True)

# 색상 만들기: 첫 번째는 빨간색, 나머지 9개는 파란색 그라데이션(짙음 -> 연함)
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*[int(max(0,min(255,round(v)))) for v in rgb])

def gradient_colors(start_hex, end_hex, n):
    s = np.array(hex_to_rgb(start_hex))
    e = np.array(hex_to_rgb(end_hex))
    colors = []
    for i in range(n):
        t = i / max(1, n-1)
        rgb = (1 - t) * s + t * e
        colors.append(rgb_to_hex(tuple(rgb)))
    return colors

# 설정: 첫 빨간, 나머지 블루 그라데이션
first_color = "#ff0000"
blue_start = "#0d47a1"   # 진한 파랑
blue_end   = "#cfe3ff"   # 연한 파랑
n_rest = max(0, len(top10) - 1)
blue_shades = gradient_colors(blue_start, blue_end, n_rest) if n_rest > 0 else []
colors = [first_color] + blue_shades

# Plotly 막대그래프
fig = go.Figure()

fig.add_trace(go.Bar(
    x=top10['역명'],
    y=top10['합계'],
    marker_color=colors,
    text=top10['합계'],
    textposition='auto',
    hovertemplate=
        "<b>%{x}</b><br>" +
        "노선: %{customdata[0]}<br>" +
        "승차: %{customdata[1]}<br>" +
        "하차: %{customdata[2]}<br>" +
        "합계: %{y}<extra></extra>",
    customdata=np.stack([top10['노선명'], top10['승차총승객수'], top10['하차총승객수']], axis=-1)
))

# 레이아웃 미세조정
fig.update_layout(
    title=f"{selected_date.strftime('%Y-%m-%d')} — {selected_line} — 승차+하차 합계 TOP 10",
    xaxis_title="역명",
    yaxis_title="승차+하차 합계",
    template="plotly_white",
    bargap=0.2,
    margin=dict(l=40, r=20, t=80, b=120),
    xaxis_tickangle=-45,
    height=600,
)

st.plotly_chart(fig, use_container_width=True)

# 하단에 표로 데이터도 출력
with st.expander("데이터 테이블 보기 (TOP 10)"):
    st.dataframe(top10.style.format({"승차총승객수": "{:,}", "하차총승객수": "{:,}", "합계": "{:,}"}))

st.markdown("---")
st.caption("※ 색상: 1위는 빨강, 나머지는 파란색에서 연해지는 그라데이션입니다.")
