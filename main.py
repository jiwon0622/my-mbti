import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="MBTI 단짝 포켓몬 찾기",
    page_icon="⭐",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# 디자인: 크림색 + 노란색 + 별빛
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

.stApp {
    background:
      radial-gradient(circle at 12% 8%, rgba(255,220,119,.25), transparent 22%),
      radial-gradient(circle at 90% 35%, rgba(255,196,96,.18), transparent 25%),
      linear-gradient(180deg, #fff9e9 0%, #fff2cb 100%);
    color: #59452a;
    font-family: 'Noto Sans KR', sans-serif;
}
.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, p, label, .stMarkdown {
    color: #59452a;
}
.hero {
    text-align: center;
    padding: 1.3rem 1rem 1.6rem;
    border: 2px solid #f3d98d;
    border-radius: 28px;
    background: rgba(255,255,255,.68);
    box-shadow: 0 12px 32px rgba(156,115,36,.10);
    margin-bottom: 1.4rem;
}
.hero-icon { font-size: 3.3rem; line-height: 1.3; }
.hero h1 {
    font-family: 'Jua', 'Noto Sans KR', sans-serif;
    color: #8b6222;
    font-size: clamp(2rem, 6vw, 3.2rem);
    margin: .3rem 0;
}
.hero p { font-size: 1.05rem; line-height: 1.8; color: #8b785a; margin-bottom: 0; }
.section-card {
    background: rgba(255,255,255,.75);
    border: 2px solid #f1dca6;
    border-radius: 24px;
    padding: 1.25rem 1.2rem;
    margin: 1rem 0;
    box-shadow: 0 8px 22px rgba(156,115,36,.07);
}
.section-title {
    font-family: 'Jua', 'Noto Sans KR', sans-serif;
    font-size: 1.6rem;
    text-align: center;
    color: #805b25;
    margin: .1rem 0 .5rem;
}
.section-hint { text-align:center; color:#9a8665; margin-bottom:1rem; }
div.stButton > button {
    min-height: 3.2rem;
    width: 100%;
    border-radius: 16px;
    border: 2px solid #efd58c;
    background: linear-gradient(145deg, #fffef8, #ffedb2);
    color: #76551f;
    font-weight: 900;
    font-size: 1.05rem;
    box-shadow: 0 4px 0 #e8cd81;
    transition: transform .15s ease, box-shadow .15s ease;
}
div.stButton > button:hover {
    border-color: #e5b943;
    color: #654615;
    background: #ffe49a;
    transform: translateY(-2px);
    box-shadow: 0 6px 0 #e4c46f;
}
.pill {
    display:inline-block;
    padding:.45rem .9rem;
    border-radius:999px;
    background:#fff0b9;
    border:1px solid #f0d27a;
    color:#80591b;
    font-weight:800;
    margin:.2rem;
}
.result-card {
    position: relative;
    overflow: hidden;
    text-align:center;
    background: linear-gradient(145deg, rgba(255,255,255,.96), rgba(255,247,220,.96));
    border: 2px solid #efce70;
    border-radius: 28px;
    padding: 1.5rem 1.25rem;
    box-shadow: 0 12px 35px rgba(164,117,28,.15);
}
.result-card h2 {
    font-family: 'Jua', 'Noto Sans KR', sans-serif;
    color: #80591b;
    font-size: clamp(1.8rem, 5vw, 2.5rem);
    margin: .3rem 0;
}
.result-subtitle { color:#8b785a; font-size:1.03rem; line-height:1.7; }
.info-box {
    text-align:left;
    background:#fff8e5;
    border:1px solid #f1d98f;
    border-radius:18px;
    padding:1rem 1.1rem;
    margin-top:1rem;
    color:#665239;
    line-height:1.85;
}
.info-box strong { color:#8b6222; font-size:1.05rem; }
.compat-box {
    background:#fff0f4;
    border:1px solid #f1c5d3;
    border-radius:18px;
    padding:1rem;
    margin-top:1rem;
    color:#735064;
    line-height:1.8;
}
.small-note { text-align:center; color:#9a886c; font-size:.85rem; margin-top:1.2rem; }
div[data-testid="stImage"] img {
    max-height: 240px;
    object-fit: contain;
    filter: drop-shadow(0 8px 12px rgba(153,111,39,.18));
}
@media (max-width: 600px) {
    .block-container { padding: 1rem .7rem 2rem; }
    .section-card { padding: 1rem .7rem; }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# MBTI별 단짝 포켓몬 데이터
# 이미지: PokeAPI 공개 스프라이트 저장소
# -----------------------------
POKEMON = {
    "ISTJ": {
        "ko": "꼬부기", "en": "Squirtle", "id": 7,
        "types": "물",
        "features": "침착하고 믿음직하며, 상황을 살피고 차근차근 움직여요.",
        "reason": "꼼꼼하고 책임감 있게 맡은 일을 해내는 ISTJ와 차분한 꼬부기는 닮은 점이 많아요. 서두르기보다 안정적으로 한 걸음씩 나아가는 단짝이에요.",
        "emoji": "💧",
    },
    "ISFJ": {
        "ko": "이브이", "en": "Eevee", "id": 133,
        "types": "노말",
        "features": "친근하고 적응력이 좋아 여러 모습으로 진화할 수 있어요.",
        "reason": "주변 사람을 세심하게 챙기는 ISFJ처럼 이브이는 친근하고 다정한 매력이 있어요. 서로를 편안하게 해 주는 포근한 단짝 조합이에요.",
        "emoji": "🌼",
    },
    "INFJ": {
        "ko": "가디안", "en": "Gardevoir", "id": 282,
        "types": "에스퍼 / 페어리",
        "features": "소중한 사람을 지키려는 마음이 강하고 신비로운 분위기를 지녔어요.",
        "reason": "사람의 마음을 깊이 이해하려는 INFJ와 소중한 이를 지키는 가디안은 따뜻한 신념으로 이어져요. 조용하지만 깊은 유대감을 만드는 단짝이에요.",
        "emoji": "✨",
    },
    "INTJ": {
        "ko": "뮤츠", "en": "Mewtwo", "id": 150,
        "types": "에스퍼",
        "features": "강력한 초능력과 뛰어난 지능을 지닌 포켓몬이에요.",
        "reason": "전략적으로 생각하고 복잡한 문제를 분석하는 INTJ에게 뮤츠가 잘 어울려요. 독립적으로 생각하면서 목표를 향해 나아가는 멋진 조합이에요.",
        "emoji": "🧠",
    },
    "ISTP": {
        "ko": "메타그로스", "en": "Metagross", "id": 376,
        "types": "강철 / 에스퍼",
        "features": "네 개의 뇌를 가진 듯한 계산 능력과 강력한 몸을 자랑해요.",
        "reason": "원리를 파악하고 실용적으로 문제를 해결하는 ISTP와 분석적인 메타그로스는 환상의 팀이에요. 말보다 행동과 결과로 보여 주는 점이 닮았어요.",
        "emoji": "🤖",
    },
    "ISFP": {
        "ko": "치라미", "en": "Minccino", "id": 572,
        "types": "노말",
        "features": "깔끔한 것을 좋아하고 작고 귀여운 몸으로 부지런히 움직여요.",
        "reason": "자신만의 감각과 취향을 소중히 여기는 ISFP와 섬세한 치라미는 부드러운 감성이 닮았어요. 소소한 즐거움과 아름다움을 함께 발견하는 단짝이에요.",
        "emoji": "🎨",
    },
    "INFP": {
        "ko": "뮤", "en": "Mew", "id": 151,
        "types": "에스퍼",
        "features": "신비롭고 호기심이 많으며 자유롭게 하늘을 날아다녀요.",
        "reason": "풍부한 상상력과 자신만의 가치관을 가진 INFP에게 신비로운 뮤가 잘 어울려요. 새로운 가능성을 꿈꾸고 자신만의 세계를 소중히 여기는 점이 닮았어요.",
        "emoji": "🌸",
    },
    "INTP": {
        "ko": "프리져", "en": "Articuno", "id": 144,
        "types": "얼음 / 비행",
        "features": "차갑고 신비로운 아름다움을 지닌 전설의 포켓몬이에요.",
        "reason": "궁금한 것을 깊이 파고들고 논리적으로 생각하는 INTP와 신비로운 프리져는 차분한 분위기가 닮았어요. 혼자만의 생각을 즐기면서도 특별한 존재감을 뽐내요.",
        "emoji": "❄️",
    },
    "ESTP": {
        "ko": "리자몽", "en": "Charizard", "id": 6,
        "types": "불꽃 / 비행",
        "features": "하늘을 날며 강력한 불꽃을 사용하는 대담한 포켓몬이에요.",
        "reason": "새로운 상황에 빠르게 적응하고 직접 도전하는 ESTP와 리자몽은 에너지가 넘쳐요. 망설이기보다 경험하며 배우는 모험 단짝이에요.",
        "emoji": "🔥",
    },
    "ESFP": {
        "ko": "피카츄", "en": "Pikachu", "id": 25,
        "types": "전기",
        "features": "밝고 활기차며 전기를 모아 힘차게 방출해요.",
        "reason": "사람들과 어울리고 순간을 즐기는 ESFP처럼 피카츄도 밝은 에너지로 주변을 환하게 만들어요. 함께 있으면 웃음과 활기가 끊이지 않을 것 같은 단짝이에요.",
        "emoji": "⚡",
    },
    "ENFP": {
        "ko": "파치리스", "en": "Pachirisu", "id": 417,
        "types": "전기",
        "features": "호기심이 많고 재빠르며 볼에 전기를 모을 수 있어요.",
        "reason": "새로운 가능성과 아이디어를 좋아하는 ENFP에게 통통 튀는 파치리스가 잘 어울려요. 여기저기 새로운 즐거움을 찾아다니는 활발한 단짝이에요.",
        "emoji": "🌈",
    },
    "ENTP": {
        "ko": "겟핸보숭", "en": "Ambipom", "id": 424,
        "types": "노말",
        "features": "꼬리 끝의 손으로 능숙하게 물건을 다루고 장난을 좋아해요.",
        "reason": "기발한 생각과 재치 있는 대화를 즐기는 ENTP와 장난꾸러기 겟핸보숭은 유쾌한 조합이에요. 뻔한 방식보다 새로운 방법을 찾아내는 점이 닮았어요.",
        "emoji": "💡",
    },
    "ESTJ": {
        "ko": "괴력몬", "en": "Machamp", "id": 68,
        "types": "격투",
        "features": "네 개의 팔로 강한 힘을 발휘하는 든든한 포켓몬이에요.",
        "reason": "목표를 세우고 체계적으로 일을 진행하는 ESTJ와 믿음직한 괴력몬은 추진력이 닮았어요. 해야 할 일을 확실하게 마무리하는 든든한 팀이에요.",
        "emoji": "💪",
    },
    "ESFJ": {
        "ko": "푸린", "en": "Jigglypuff", "id": 39,
        "types": "노말 / 페어리",
        "features": "노래 부르기를 좋아하고 둥글둥글한 모습이 사랑스러워요.",
        "reason": "주변 사람들과 조화를 이루고 함께하는 시간을 소중히 여기는 ESFJ와 푸린은 다정한 분위기가 닮았어요. 노래와 웃음으로 주변을 따뜻하게 만드는 단짝이에요.",
        "emoji": "🎤",
    },
    "ENFJ": {
        "ko": "루카리오", "en": "Lucario", "id": 448,
        "types": "격투 / 강철",
        "features": "파동을 감지해 주변을 살피고 정의감이 강한 포켓몬이에요.",
        "reason": "다른 사람의 성장을 응원하고 힘이 되어 주는 ENFJ와 파동으로 마음을 읽는 루카리오는 배려심이 닮았어요. 서로를 믿고 함께 성장하는 단짝이에요.",
        "emoji": "💙",
    },
    "ENTJ": {
        "ko": "망나뇽", "en": "Dragonite", "id": 149,
        "types": "드래곤 / 비행",
        "features": "큰 날개로 하늘을 날고 힘과 친절함을 함께 지녔어요.",
        "reason": "큰 목표를 세우고 팀을 이끄는 ENTJ와 강인하면서도 든든한 망나뇽은 리더십이 잘 어울려요. 넓은 시야로 목표를 향해 함께 나아가는 조합이에요.",
        "emoji": "🐉",
    },
}

# -----------------------------
# 제목과 안내
# -----------------------------
st.markdown("""
<div class="hero">
  <div class="hero-icon">⭐ 🐾 🌼</div>
  <h1>MBTI 단짝 포켓몬 찾기</h1>
  <p>내 성격과 찰떡궁합인 포켓몬은 누구일까?<br>
  MBTI를 고르고 나만의 단짝을 만나 봐!</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-card"><div class="section-title">🌟 나의 MBTI는?</div><div class="section-hint">반짝이는 버튼을 눌러 유형을 선택해 줘!</div>', unsafe_allow_html=True)

types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ",
]

# 4열 버튼 배열
for row_start in range(0, 16, 4):
    cols = st.columns(4)
    for col, mbti in zip(cols, types[row_start:row_start + 4]):
        with col:
            if st.button(f"⭐ {mbti}", key=f"mbti_{mbti}", use_container_width=True):
                st.session_state["selected_mbti"] = mbti
                st.session_state["celebrate"] = True

st.markdown("</div>", unsafe_allow_html=True)

selected = st.session_state.get("selected_mbti")

if selected:
    data = POKEMON[selected]

    # 선택 직후 축하 효과는 한 번만 실행
    if st.session_state.get("celebrate", False):
        st.balloons()
        st.snow()
        st.session_state["celebrate"] = False

    st.markdown(
        f"""
        <div class="result-card">
          <div style="font-size:1rem; color:#9b762e; font-weight:800;">
            🎉 너의 MBTI는 {selected}!
          </div>
          <div style="font-size:2rem; margin:.3rem;">{data['emoji']} ✨ 🎊</div>
          <h2>{data['ko']} ({data['en']})</h2>
          <div class="result-subtitle">너와 가장 잘 어울리는 단짝 포켓몬을 찾았어!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    image_url = (
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
        f"sprites/pokemon/{data['id']}.png"
    )

    # 포켓몬 이미지와 기본 정보
    left, right = st.columns([1, 1.2], vertical_alignment="center")
    with left:
        st.image(
            image_url,
            caption=f"{data['ko']} · {data['en']}",
            use_container_width=True,
        )
    with right:
        st.markdown(
            f"""
            <div class="info-box">
              <strong>🏷️ 타입</strong><br>
              <span class="pill">{data['types']}</span>
              <br><br>
              <strong>✨ 포켓몬 특징</strong><br>
              {data['features']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="info-box">
          <strong>💛 너와 잘 어울리는 이유</strong><br>
          {data['reason']}
        </div>
        <div class="compat-box">
          <strong>🎊 축하해! 단짝 포켓몬을 찾았어!</strong><br>
          별빛처럼 반짝이는 너만의 파트너와 즐거운 모험을 떠나 봐 ✨
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🔄 다시 고르기", key="reset", use_container_width=True):
        st.session_state.pop("selected_mbti", None)
        st.session_state["celebrate"] = False
        st.rerun()

else:
    st.markdown("""
    <div class="section-card" style="text-align:center;">
      <div style="font-size:3rem;">🥚 ✨ 🐾</div>
      <h3 style="color:#8b6222;">아직 단짝을 찾지 않았어!</h3>
      <p style="color:#8b785a; line-height:1.8;">
        위에서 MBTI 버튼 하나를 눌러 봐.<br>
        너와 잘 어울리는 포켓몬이 기다리고 있어!
      </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="small-note">
  포켓몬 이미지 출처: PokeAPI 공개 스프라이트 저장소<br>
  이 결과는 재미를 위한 성격 놀이이며, 실제 성격이나 궁합을 과학적으로 판단하지 않아.
</div>
""", unsafe_allow_html=True)
