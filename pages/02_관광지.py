# Streamlit app: Seoul Top10 (for foreign visitors) - Folium map
# Save this file as app.py in your Streamlit Cloud repo.
# Also create a separate requirements.txt (contents shown at the bottom of this file).

import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Seoul Top10 for Foreign Visitors", layout="wide")

st.title("🇰🇷 Seoul — Top 10 관광지 (외국인 인기)")
st.markdown("다음 지도는 외국인 관광객에게 특히 인기 있는 서울의 주요 관광지 Top10을 Folium으로 보여줍니다.")

# Top 10 명소 (이름, 위도, 경도, 간단 설명)
TOP10 = [
    {"name": "Gyeongbokgung Palace (경복궁)", "lat": 37.579617, "lon": 126.977041, "desc": "조선 시대의 대표 궁궐, 근정전 등"},
    {"name": "Bukchon Hanok Village (북촌한옥마을)", "lat": 37.582604, "lon": 126.983527, "desc": "전통 한옥이 모여있는 골목"},
    {"name": "Insadong (인사동)", "lat": 37.574022, "lon": 126.986072, "desc": "전통 공예품 상점과 찻집 골목"},
    {"name": "Myeongdong (명동)", "lat": 37.563757, "lon": 126.986205, "desc": "쇼핑 & 길거리 음식으로 유명한 상권"},
    {"name": "N Seoul Tower / Namsan (남산서울타워)", "lat": 37.551169, "lon": 126.988227, "desc": "서울 전망 명소"},
    {"name": "Hongdae (홍대)", "lat": 37.557187, "lon": 126.924445, "desc": "젊음의 거리, 공연과 카페 문화"},
    {"name": "Dongdaemun Design Plaza (DDP, 동대문디자인플라자)", "lat": 37.566295, "lon": 127.009386, "desc": "현대적 건축물 & 야시장"},
    {"name": "Changdeokgung Palace & Huwon (창덕궁과 후원)", "lat": 37.579477, "lon": 126.991015, "desc": "유네스코 세계유산 궁궐"},
    {"name": "Lotte World Tower / Seokchon Lake (롯데월드타워)", "lat": 37.513078, "lon": 127.102538, "desc": "고층 전망대와 쇼핑몰"},
    {"name": "COEX & Gangnam (코엑스/강남)", "lat": 37.512592, "lon": 127.058333, "desc": "대형 쇼핑몰, 아쿠아리움, 비즈니스 허브"},
]

# Sidebar controls
st.sidebar.header("지도 옵션")
map_type = st.sidebar.selectbox("지도 스타일 (tiles)", ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "CartoDB positron", "CartoDB dark_matter"], index=0)
start_zoom = st.sidebar.slider("초기 확대 레벨", min_value=10, max_value=15, value=12)
show_cluster = st.sidebar.checkbox("마커 클러스터 사용", value=True)
show_popup = st.sidebar.checkbox("팝업에 설명 보이기", value=True)

# Center map roughly in central Seoul
CENTER = (37.5665, 126.9780)

# Create folium map
m = folium.Map(location=CENTER, zoom_start=start_zoom, tiles=map_type)

if show_cluster:
    marker_cluster = MarkerCluster().add_to(m)

for place in TOP10:
    popup_html = f"<b>{place['name']}</b>"
    if show_popup:
        popup_html += f"<br/>{place['desc']}"
    popup = folium.Popup(popup_html, max_width=300)
    marker = folium.Marker(location=(place['lat'], place['lon']), popup=popup, tooltip=place['name'])
    if show_cluster:
        marker.add_to(marker_cluster)
    else:
        marker.add_to(m)

# Add a small legend / list on the right using st.columns
col1, col2 = st.columns([2,1])
with col1:
    st.subheader("지도")
    # Use st_folium to render
    st_data = st_folium(m, width="100%", height=650)

with col2:
    st.subheader("Top 10 리스트")
    for i, p in enumerate(TOP10, start=1):
        st.markdown(f"**{i}. {p['name']}**")
        st.markdown(f"- {p['desc']}")
        st.markdown(f"- 좌표: `{p['lat']}, {p['lon']}`")
        st.write("---")

st.markdown("---")
st.markdown("*팁: 각 마커를 클릭하면 팝업이 열립니다. 사이드바에서 지도 스타일과 클러스터를 조절해 보세요.*")

# Optional: allow user to focus on a place
st.sidebar.header("빠른 이동")
place_names = [p['name'] for p in TOP10]
choice = st.sidebar.selectbox("장소 선택", ["-- 없음 --"] + place_names)
if choice != "-- 없음 --":
    sel = next((p for p in TOP10 if p['name'] == choice), None)
    if sel:
        # create a small map focused on the chosen place and show it below
        focused = folium.Map(location=(sel['lat'], sel['lon']), zoom_start=16, tiles=map_type)
        folium.Marker(location=(sel['lat'], sel['lon']), popup=sel['name'], tooltip=sel['name']).add_to(focused)
        st.subheader(f"📍 {sel['name']}에 초점")
        st_folium(focused, width="100%", height=350)


# =====================
# requirements.txt (create this as a separate file in your repo named requirements.txt)
# =====================
# Contents below (not Python code) — copy into a file named `requirements.txt`:
#
# streamlit
# folium
# streamlit-folium
#
# Optional pinning for stability (example):
# streamlit==1.25.0
# folium==0.14.0
# streamlit-folium==0.14.0
#
# ---------------------
# 사용법 요약:
# 1) GitHub 저장소를 만들고 이 파일(app.py)와 requirements.txt(위의 내용을 복사)를 추가합니다.
# 2) Streamlit Cloud에 GitHub 저장소 연결 후 배포합니다.
# 3) 필요하면 TOP10 목록이나 마커 스타일을 수정하세요.
# ---------------------
