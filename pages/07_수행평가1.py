import streamlit as st

st.set_page_config(page_title="🍰 디저트 추천 챗봇", page_icon="🍮")

st.title("🍰 디저트 추천 챗봇")
st.write("MBTI, 기분, 날씨에 따라 오늘의 디저트를 추천해주는 앱입니다!")

# --- MBTI 선택 ---
mbti = st.selectbox(
    "당신의 MBTI를 선택하세요:",
    ["ISTJ","ISFJ","INFJ","INTJ","ISTP","ISFP","INFP","INTP",
     "ESTP","ESFP","ENFP","ENTP","ESTJ","ESFJ","ENFJ","ENTJ"]
)

# --- 기분 선택 ---
mood = st.radio(
    "지금 기분은 어떠세요?",
    ["기쁨 😊", "지침 😪", "스트레스 😡", "심심함 😐", "설렘 💗"]
)

# --- 날씨 선택 ---
weather = st.selectbox(
    "현재 날씨는 어떤가요?",
    ["맑음 ☀️", "흐림 ☁️", "비 🌧️", "눈 ❄️", "더움 🔥", "추움 🥶"]
)

st.write("---")

# --- MBTI 기반 디저트 추천 ---
mbti_dessert = {
    "ISTJ": "클래식 치즈케이크",
    "ISFJ": "바닐라 푸딩",
    "INFJ": "말차 롤케이크",
    "INTJ": "다크 초콜릿 타르트",
    "ISTP": "초코 브라우니",
    "ISFP": "딸기 쇼트케이크",
    "INFP": "티라미수",
    "INTP": "마카롱",

    "ESTP": "크렘브륄레",
    "ESFP": "레인보우 케이크",
    "ENFP": "바스크 치즈케이크",
    "ENTP": "애플파이",

    "ESTJ": "휘낭시에",
    "ESFJ": "딸기 타르트",
    "ENFJ": "레몬 머랭파이",
    "ENTJ": "에스프레소 아포가토"
}

# --- 기분 기반 추천 ---
mood_dessert = {
    "기쁨 😊": "마들렌 🍪",
    "지침 😪": "티라미수 ☕",
    "스트레스 😡": "다크초콜릿 💝",
    "심심함 😐": "쿠키앤크림 아이스크림 🍨",
    "설렘 💗": "딸기 밀푀유 🍓"
}

# --- 날씨 기반 추천 ---
weather_dessert = {
    "맑음 ☀️": "망고 젤라또",
    "흐림 ☁️": "가나슈 케이크",
    "비 🌧️": "포레누아(초코 체리 케이크)",
    "눈 ❄️": "핫초코 + 마시멜로",
    "더움 🔥": "아이스크림 샌드위치",
    "추움 🥶": "군고구마 라떼 디저트"
}

# --- 최종 추천 ---
st.subheader("✨ 오늘의 디저트 추천")

st.write(f"**MBTI 기반 추천:** {mbti_dessert[mbti]}")
st.write(f"**기분 기반 추천:** {mood_dessert[mood]}")
st.write(f"**날씨 기반 추천:** {weather_dessert[weather]}")

st.write("---")
st.success("🎉 오늘의 디저트가 준비됐어요! 카페 가기 전에 참고해봐요 :)")
