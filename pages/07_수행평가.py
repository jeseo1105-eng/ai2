import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# 1. 데이터 정의 (파일 내용을 문자열로 직접 삽입)
CSV_DATA_STRING = """
서울도서관 분야별 장서 현황(기준 : 2022.12.31),,,,,,,,,,,,,
구분,,총류,철학,종교,"사회
과학","자연
과학","기술
과학",예술,언어,문학,역사,기타,합계
,,,,,,,,,,,,,
일반도서,," 20,083 "," 25,022 "," 11,443 "," 114,653 "," 13,392 "," 50,099 "," 23,974 "," 11,914 "," 110,631 "," 32,540 ", - ," 413,751 "
서울시 및 정부간행물,," 3,291 ", 80 , 91 ," 59,898 "," 1,293 "," 29,218 "," 6,216 ", 192 , 757 ," 6,153 ", 15 ," 107,204 "
비도서,," 2,530 ", 481 , 194 ," 1,960 ", 565 , 591 ," 11,205 ", 293 ," 3,285 "," 1,596 ", - ," 22,700 "
합계,," 25,904 "," 25,583 "," 11,728 "," 176,511 "," 15,250 "," 79,908 "," 41,395 "," 12,399 "," 114,673 "," 40,289 ", 15 ," 543,655 "
"""

# 2. 데이터 로드 및 전처리 함수 (수정된 부분)
@st.cache_data
def load_and_preprocess_data(csv_string):
    data_io = StringIO(csv_string)
    
    # 1. 파일 읽기: header=2는 여전히 유효함.
    # index_col=0를 사용하여 첫 번째 열을 인덱스로 바로 설정 시도.
    df = pd.read_csv(data_io, header=2, thousands=',', index_col=0)
    
    # 2. 불필요한 빈 열 제거 (컬럼 이름이 NaN 또는 Unnamed로 시작하는 경우)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed', na=False)]
    
    # 3. 인덱스 정리: 인덱스(행 이름)의 앞뒤 공백 제거 및 정리
    df.index = df.index.astype(str).str.strip()
    
    # 4. 열 이름 정리: 줄바꿈 문자('\n')와 공백 제거
    df.columns = df.columns.str.replace('\n', ' ').str.strip()
    
    # 5. 마지막 '합계' 열 제거 (만약 아직 남아있다면)
    df = df.drop(columns=['합계'], errors='ignore')
    
    # 6. 숫자 데이터 정리: 공백 제거, '-' 값은 0으로 변환하고 모든 데이터를 정수형으로 변환
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(' ', '').replace('-', '0')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
    # 7. '합계' 행 제거 (분석에 필요한 '일반도서', '서울시 및 정부간행물', '비도서'만 남김)
    df_filtered = df.drop('합계', errors='ignore')
    
    return df_filtered

# 3. Plotly 시각화 함수 (이전과 동일)
def create_top_n_chart(data, material_type, n=6):
    
    # 이 부분에서 오류가 발생했으나, 위 전처리 함수 수정으로 해결될 것으로 예상됨.
    series = data.loc[material_type] 
    
    series = series.drop(['기타'], errors='ignore')
    
    top_n = series.sort_values(ascending=False).head(n)
    
    df_plot = top_n.reset_index()
    df_plot.columns = ['분야', '장서 수']
    
    colors = ['#FF4B4B', '#FFA422', '#FFEE6A', '#3CB371', '#1E90FF', '#8A2BE2'] 
    
    fig = px.bar(
        df_plot,
        x='장서 수',
        y='분야',
        orientation='h',
        title=f"📚 **{material_type}** 장서 수 상위 {n}개 분야",
        color='장서 수',
        color_discrete_sequence=colors,
        height=450
    )
    
    fig.update_layout(
        xaxis_title="장서 수 (권)",
        yaxis_title="분야",
        yaxis={'categoryorder':'total ascending'},
        font=dict(size=14),
        showlegend=False,
        hovermode="y unified"
    )
    
    fig.update_traces(textposition='outside', 
                      text=df_plot['장서 수'].apply(lambda x: f'{x:,}권'),
                      marker_line_width=0)
    
    return fig

# 4. Streamlit 앱 실행 (이전과 동일)
def main():
    st.set_page_config(layout="wide", page_title="서울도서관 장서 현황 분석")
    
    st.title("서울도서관 분야별 장서 현황 분석 (2022.12.31 기준)")
    st.caption("데이터는 코드 내에 직접 포함되어 있습니다.")
    
    try:
        data = load_and_preprocess_data(CSV_DATA_STRING)
    except Exception as e:
        st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")
        return

    material_types = ['일반도서', '서울시 및 정부간행물', '비도서']
    
    st.sidebar.header("📊 자료 유형 선택
