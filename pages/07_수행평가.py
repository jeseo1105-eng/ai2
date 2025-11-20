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

# 2. 데이터 로드 및 전처리 함수
@st.cache_data
def load_and_preprocess_data(csv_string):
    # StringIO를 사용하여 문자열 데이터를 파일처럼 처리
    data_io = StringIO(csv_string)
    
    # CSV 파일을 읽어옵니다. (헤더가 3번째 행(index 2)부터 시작, 쉼표 처리)
    df = pd.read_csv(data_io, header=2, thousands=',')
    
    # 불필요한 첫 번째 열(Unnamed: 0)과 마지막 '합계' 열 제거
    df = df.iloc[:, 1:-1]
    
    # 첫 번째 열을 인덱스로 설정하고 이름을 '구분'으로 지정
    df = df.set_index(df.columns[0]).rename_axis('구분')
    
    # 열 이름 정리: 줄바꿈 문자('\n') 제거
    df.columns = df.columns.str.replace('\n', ' ').str.strip()
    
    # 숫자 데이터 정리: 공백 제거, '-' 값은 0으로 변환하고 모든 데이터를 정수형으로 변환
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(' ', '').replace('-', '0')
            # 'coerce'는 변환 불가능한 값을 NaN으로 만들고, fillna(0)으로 0 처리
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
    # '합계' 행 제거 (분석에 필요한 '일반도서', '서울시 및 정부간행물', '비도서'만 남김)
    df_filtered = df.drop('합계', errors='ignore')
    
    return df_filtered

# 3. Plotly 시각화 함수 (요청 사항에 맞게)
def create_top_n_chart(data, material_type, n=6):
    
    # 요청된 자료 유형의 데이터 추출
    series = data.loc[material_type]
    
    # '합계', '기타' 열은 분석 대상에서 제외
    series = series.drop(['합계', '기타'], errors='ignore')
    
    # 상위 N개 데이터 선택 (내림차순 정렬)
    top_n = series.sort_values(ascending=False).head(n)
    
    # Plotly에서 사용하기 위해 DataFrame으로 변환
    df_plot = top_n.reset_index()
    df_plot.columns = ['분야', '장서 수']
    
    # 4. 색상 설정 (1등부터 빨강, 주황, 노랑, 초록, 파랑, 보라색)
    colors = ['#FF4B4B', '#FFA422', '#FFEE6A', '#3CB371', '#1E90FF', '#8A2BE2'] 
    
    # 2. Plotly로 인터랙티브 막대 그래프 생성
    fig = px.bar(
        df_plot,
        x='장서 수',
        y='분야',
        orientation='h', # 수평 막대 그래프
        title=f"📚 **{material_type}** 장서 수 상위 {n}개 분야",
        color='장서 수',
        color_discrete_sequence=colors, # 사용자 정의 색상 적용
        height=450
    )
    
    # 레이아웃 설정
    fig.update_layout(
        xaxis_title="장서 수 (권)",
        yaxis_title="분야",
        yaxis={'categoryorder':'total ascending'}, # 장서 수에 따라 정렬 유지
        font=dict(size=14),
        showlegend=False,
        hovermode="y unified"
    )
    
    # 막대에 텍스트 레이블 추가
    fig.update_traces(textposition='outside', 
                      text=df_plot['장서 수'].apply(lambda x: f'{x:,}권'),
                      marker_line_width=0)
    
    return fig

# 5. Streamlit 앱 실행
def main():
    st.set_page_config(layout="wide", page_title="서울도서관 장서 현황 분석")
    
    st.title("서울도서관 분야별 장서 현황 분석 (2022.12.31 기준)")
    st.caption("데이터는 코드 내에 직접 포함되어 있습니다.")
    
    # 데이터 로드
    try:
        data = load_and_preprocess_data(CSV_DATA_STRING)
    except Exception as e:
        st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")
        return

    # 사용자가 선택할 수 있는 자료 유형 리스트
    material_types = ['일반도서', '서울시 및 정부간행물', '비도서']
    
    # 사이드바에서 자료 유형 선택
    st.sidebar.header("📊 자료 유형 선택")
    selected_type = st.sidebar.radio(
        "분석할 장서 유형을 선택하세요:",
        material_types
    )
    
    # 선택된 유형에 따른 시각화 실행
    if selected_type:
        st.subheader(f"선택: **{selected_type}**")
        
        # Plotly 그래프 생성 및 표시
        fig = create_top_n_chart(data, selected_type)
        st.plotly_chart(fig, use_container_width=True)

        # 전체 장서 수 요약
        total_count = data.loc[selected_type].drop(['합계', '기타'], errors='ignore').sum()
        st.metric(f"총 {selected_type} 장서 수", f"{total_count:,.0f}권")
        
        # 데이터 미리보기
        with st.expander("원본 데이터 테이블 보기"):
            st.dataframe(data.T, use_container_width=True)

if __name__ == "__main__":
    main()
