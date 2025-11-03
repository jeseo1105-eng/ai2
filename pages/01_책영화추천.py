import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 취향 추천기 💫", page_icon="💫")

# 제목
st.title("🌈 MBTI로 알아보는 너의 취향 추천기 🎬📚")
st.write("안녕! 😄 네 MBTI를 고르면, 너한테 딱 맞는 **책 2권📖**이랑 **영화 2편🎥**을 추천해줄게!")

# MBTI 리스트
mbti_list = [
    "INTJ", "INTP", "INFJ", "INFP",
    "ISTJ", "ISTP", "ISFJ", "ISFP",
    "ENTJ", "ENTP", "ENFJ", "ENFP",
    "ESTJ", "ESTP", "ESFJ", "ESFP"
]

# 선택 박스
mbti = st.selectbox("👇 너의 MBTI를 선택해줘!", [""] + mbti_list)

# 추천 데이터
recommendations = {
    "INTJ": {
        "books": ["『1984』 - 조지 오웰", "『데미안』 - 헤르만 헤세"],
        "movies": ["🎥 인터스텔라", "🎥 인셉션"]
    },
    "INTP": {
        "books": ["『이기적 유전자』 - 리처드 도킨스", "『호모 데우스』 - 유발 하라리"],
        "movies": ["🎬 매트릭스", "🎬 테넷"]
    },
    "INFJ": {
        "books": ["『연금술사』 - 파울로 코엘료", "『달과 6펜스』 - 서머싯 몸"],
        "movies": ["🎞 어바웃 타임", "🎞 인사이드 아웃"]
    },
    "INFP": {
        "books": ["『어린 왕자』 - 생텍쥐페리", "『월든』 - 헨리 데이비드 소로"],
        "movies": ["🎬 주토피아", "🎬 월-E"]
    },
    "ISTJ": {
        "books": ["『성공하는 사람들의 7가지 습관』 - 스티븐 코비", "『원씽』 - 게리 켈러"],
        "movies": ["🎥 캐치 미 이프 유 캔", "🎥 머니볼"]
    },
    "ISTP": {
        "books": ["『셜록 홈즈』 - 아서 코난 도일", "『파이 이야기』 - 얀 마텔"],
        "movies": ["🎬 매드맥스: 분노의 도로", "🎬 미션 임파서블"]
    },
    "ISFJ": {
        "books": ["『작은 아씨들』 - 루이자 올컷", "『하늘과 바람과 별과 시』 - 윤동주"],
        "movies": ["🎞 인사이드 아웃", "🎞 초속 5cm"]
    },
    "ISFP": {
        "books": ["『나미야 잡화점의 기적』 - 히가시노 게이고", "『오늘은 이만 좀 쉴게요』 - 손힘찬"],
        "movies": ["🎬 코코", "🎬 비긴 어게인"]
    },
    "ENTJ": {
        "books": ["『손자병법』 - 손무", "『리더의 용기』 - 브레네 브라운"],
        "movies": ["🎥 아이언맨", "🎥 킹스맨"]
    },
    "ENTP": {
        "books": ["『생각의 탄생』 - 루트번스타인", "『넛지』 - 리처드 세일러"],
        "movies": ["🎞 소셜 네트워크", "🎞 나우 유 씨 미"]
    },
    "ENFJ": {
        "books": ["『미움받을 용기』 - 기시미 이치로", "『나는 나로 살기로 했다』 - 김수현"],
        "movies": ["🎬 인턴", "🎬 원더"]
    },
    "ENFP": {
        "books": ["『오만과 편견』 - 제인 오스틴", "『이기적 유전자』 - 리처드 도킨스"],
        "movies": ["🎞 라라랜드", "🎞 인사이드 아웃"]
    },
    "ESTJ": {
        "books": ["『성공하는 사람들의 7가지 습관』 - 스티븐 코비", "『원씽』 - 게리 켈러"],
        "movies": ["🎥 캐치 미 이프 유 캔", "🎥 머니볼"]
    },
    "ESTP": {
        "books": ["『부의 인문학』 - 브라운스톤", "『아웃라이어』 - 말콤 글래드웰"],
        "movies": ["🎬 분노의 질주", "🎬 탑건: 매버릭"]
    },
    "ESFJ": {
        "books": ["『작은 아씨들』 - 루이자 올컷", "『어떻게 살아야 할까』 - 유시민"],
        "movies": ["🎞 인턴", "🎞 겨울왕국"]
    },
    "ESFP": {
        "books": ["『트와일라잇』 - 스테프니 메이어", "『나미야 잡화점의 기적』 - 히가시노 게이고"],
        "movies": ["🎬 위대한 쇼맨", "🎬 맘마미아!"]
    },
}

# 결과 출력
if mbti:
    st.subheader(f"✨ {mbti}에게 어울리는 취향 추천 ✨")
    rec = recommendations.get(mbti)
    if rec:
        st.write("📚 **책 추천**")
        for book in rec["books"]:
            st.write(f"- {book}")
        st.write("\n🎬 **영화 추천**")
        for movie in rec["movies"]:
            st.write(f"- {movie}")
        st.success("이 중 하나는 네 취향 저격일지도?! 💘")
    else:
        st.warning("앗! 아직 그 MBTI는 준비 중이야 🛠")
else:
    st.info("먼저 위에서 네 MBTI를 선택해줘 😄")

st.write("---")
st.caption("💡 made with love by ChatGPT x Streamlit 💫")
