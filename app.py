import streamlit as st

# ============================================================
# الإعدادات
# ============================================================
st.set_page_config(
    page_title="ASTRO",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    '<meta name="google" content="notranslate">',
    unsafe_allow_html=True,
)

# حالة اللغة والوضع
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "mode" not in st.session_state:
    st.session_state.mode = None

# الترجمات
T = {
    "ar": {
        "welcome": "اختر من تريد أن يكون أسترو معك اليوم",
        "teacher": "أسترو\nالمعلم",
        "doctor": "أسترو\nالطبيب",
        "friend": "أسترو الصديق\nوالداعم النفسي",
        "general": "عام",
        "settings": "الإعدادات",
        "language": "اللغة",
        "terms": "الشروط وسياسة الخصوصية",
        "ai_options": "خيارات الذكاء الاصطناعي",
        "google": "ربط حساب Google",
    },
    "en": {
        "welcome": "Choose who Astro should be for you today",
        "teacher": "Astro\nthe Teacher",
        "doctor": "Astro\nthe Doctor",
        "friend": "Astro the Friend\n& Supporter",
        "general": "General",
        "settings": "Settings",
        "language": "Language",
        "terms": "Terms & Privacy Policy",
        "ai_options": "AI Options",
        "google": "Connect Google Account",
    },
}
L = T[st.session_state.lang]

# ============================================================
# التنسيقات (CSS)
# ============================================================
st.markdown("""
<style>
/* ===== الخلفية الوردية ===== */
.stApp {
    background: linear-gradient(135deg, #ffe0ec 0%, #ffc2d8 50%, #ffb3cc 100%) !important;
}
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 800px; }

/* ===== ورقة الشجر المموهة ===== */
.leaf-bg {
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 85vw; max-width: 500px;
    z-index: 0;
    opacity: 0.5;
    filter: blur(20px);
    pointer-events: none;
}

/* ===== اسم ASTRO الذهبي المزخرف ===== */
.astro-title {
    text-align: center;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 3.2rem;
    font-weight: 900;
    letter-spacing: 8px;
    margin: 10px 0 5px 0;
    background: linear-gradient(180deg, #fff4c2 0%, #ffd966 25%, #d4a017 55%, #b8860b 75%, #fff4c2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 
        0 0 10px rgba(255, 215, 0, 0.6),
        0 0 20px rgba(255, 215, 0, 0.4),
        0 0 30px rgba(255, 215, 0, 0.2);
    position: relative; z-index: 2;
}
.astro-title::after {
    content: "✦ ─── ✦ ─── ✦";
    display: block;
    font-size: 0.8rem;
    color: #d4a017;
    letter-spacing: 4px;
    margin-top: 6px;
    -webkit-text-fill-color: #d4a017;
    text-shadow: 0 0 8px rgba(255, 215, 0, 0.7);
}

.astro-sub {
    text-align: center;
    color: #8a3d63;
    font-size: 1rem;
    margin-bottom: 30px;
    position: relative; z-index: 2;
    padding: 0 15px;
}

/* ===== الفقاعات الذهبية مع هالة وردية متوهجة ===== */
div.stButton > button {
    border-radius: 50% !important;
    width: 150px !important;
    height: 150px !important;
    min-height: 150px !important;
    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.5), rgba(255,192,203,0.25)) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1.5px solid rgba(255, 215, 0, 0.7) !important;
    color: #d4a017 !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    padding: 12px !important;
    display: block !important;
    margin: 25px auto !important;
    white-space: pre-line !important;
    line-height: 1.3 !important;
    text-shadow: 
        0 0 6px rgba(255, 215, 0, 0.9),
        0 0 12px rgba(255, 215, 0, 0.6),
        0 0 18px rgba(255, 100, 180, 0.4) !important;
    box-shadow: 
        0 0 20px rgba(255, 105, 180, 0.7),
        0 0 40px rgba(255, 20, 147, 0.5),
        0 0 60px rgba(255, 20, 147, 0.3),
        inset 0 0 20px rgba(255, 255, 255, 0.3) !important;
    transition: all 0.35s ease !important;
    position: relative; z-index: 2;
    animation: pulse-glow 2.5s ease-in-out infinite;
}

@keyframes pulse-glow {
    0%, 100% {
        box-shadow: 
            0 0 20px rgba(255, 105, 180, 0.7),
            0 0 40px rgba(255, 20, 147, 0.5),
            0 0 60px rgba(255, 20, 147, 0.3),
            inset 0 0 20px rgba(255, 255, 255, 0.3);
    }
    50% {
        box-shadow: 
            0 0 30px rgba(255, 105, 180, 0.9),
            0 0 55px rgba(255, 20, 147, 0.7),
            0 0 80px rgba(255, 20, 147, 0.5),
            inset 0 0 25px rgba(255, 255, 255, 0.4);
    }
}

div.stButton > button:hover {
    transform: scale(1.08);
    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.7), rgba(255,215,0,0.3)) !important;
    color: #b8860b !important;
    border-color: #ffd700 !important;
    box-shadow: 
        0 0 35px rgba(255, 215, 0, 0.9),
        0 0 70px rgba(255, 105, 180, 0.8),
        0 0 100px rgba(255, 20, 147, 0.5) !important;
}
div.stButton > button:focus { outline: none !important; }

/* ===== إجبار الأعمدة على البقاء أفقية على الجوال ===== */
[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 8px !important;
    justify-content: center !important;
}
[data-testid="column"] {
    flex: 1 1 50% !important;
    min-width: 0 !important;
    width: 50% !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

/* ===== زر الإعدادات البنفسجي ===== */
.settings-gear button {
    border-radius: 50% !important;
    width: 48px !important;
    height: 48px !important;
    min-height: 48px !important;
    background: linear-gradient(135deg, #a855f7, #7c3aed) !important;
    color: white !important;
    font-size: 20px !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.5) !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* ===== استجابة الجوال ===== */
@media (max-width: 768px) {
    .astro-title { font-size: 2.4rem; letter-spacing: 5px; }
    .astro-title::after { font-size: 0.65rem; }
    div.stButton > button {
        width: 140px !important;
        height: 140px !important;
        min-height: 140px !important;
        font-size: 0.8rem !important;
        margin: 15px auto !important;
    }
    .block-container { padding-left: 0.3rem; padding-right: 0.3rem; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# ورقة الشجر المموهة
# ============================================================
st.markdown("""
<div class="leaf-bg">
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="g1" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff69b4" stop-opacity="1"/>
      <stop offset="100%" stop-color="#ff1493" stop-opacity="0.5"/>
    </radialGradient>
  </defs>
  <path fill="url(#g1)" d="M100,10 C50,10 20,50 20,100 C20,150 50,190 100,190 C150,190 180,150 180,100 C180,50 150,10 100,10 Z"/>
  <path fill="#ffc2d8" d="M100,40 C75,40 60,70 60,100 C60,130 75,160 100,160 C125,160 140,130 140,100 C140,70 125,40 100,40 Z"/>
  <path fill="#ff69b4" d="M100,70 C90,70 85,85 85,100 C85,115 90,130 100,130 C110,130 115,115 115,100 C115,85 110,70 100,70 Z"/>
  <path fill="#ffffff" opacity="0.5" d="M60,95 L140,95 L140,105 L60,105 Z"/>
  <path fill="#ffffff" opacity="0.5" d="M95,60 L105,60 L105,140 L95,140 Z"/>
</svg>
</div>
""", unsafe_allow_html=True)

# ============================================================
# الترويسة
# ============================================================
col_title, col_gear = st.columns([5, 1])

with col_title:
    st.markdown('<div class="astro-title">ASTRO</div>', unsafe_allow_html=True)

with col_gear:
    st.markdown('<div class="settings-gear">', unsafe_allow_html=True)
    with st.popover("⚙"):
        st.markdown(f"### ⚙️ {L['settings']}")

        st.markdown(f"**🌐 {L['language']}**")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("العربية", use_container_width=True, key="ar_btn"):
                st.session_state.lang = "ar"
                st.rerun()
        with c2:
            if st.button("English", use_container_width=True, key="en_btn"):
                st.session_state.lang = "en"
                st.rerun()

        st.divider()
        st.button(f"📜 {L['terms']}", use_container_width=True)
        st.button(f"🤖 {L['ai_options']}", use_container_width=True)

        st.divider()
        st.button(f"🔗 {L['google']}", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# الرسالة الترحيبية
# ============================================================
st.markdown(f'<div class="astro-sub">{L["welcome"]}</div>', unsafe_allow_html=True)

# ============================================================
# الفقاعات - 2×2
# ============================================================
row1_c1, row1_c2 = st.columns(2)
with row1_c1:
    if st.button(L["teacher"], key="btn_teacher"):
        st.session_state.mode = "teacher"
with row1_c2:
    if st.button(L["doctor"], key="btn_doctor"):
        st.session_state.mode = "doctor"

row2_c1, row2_c2 = st.columns(2)
with row2_c1:
    if st.button(L["friend"], key="btn_friend"):
        st.session_state.mode = "friend"
with row2_c2:
    if st.button(L["general"], key="btn_general"):
        st.session_state.mode = "general"

# ============================================================
# عرض الوضع المختار
# ============================================================
if st.session_state.mode:
    st.divider()
    selected = L[st.session_state.mode].replace("\n", " ")
    st.success(f"✅ تم اختيار: **{selected}**")
