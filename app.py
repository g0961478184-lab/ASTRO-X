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

# قراءة الوضع من الرابط
if "mode" in st.query_params:
    st.session_state.mode = st.query_params["mode"]

if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "mode" not in st.session_state:
    st.session_state.mode = None

# الترجمات
T = {
    "ar": {
        "welcome": "اختر من تريد أن يكون أسترو معك اليوم",
        "teacher": "أسترو<br>المعلم",
        "doctor": "أسترو<br>الطبيب",
        "friend": "أسترو الصديق<br>والداعم النفسي",
        "general": "عام",
        "settings": "الإعدادات",
        "language": "اللغة",
        "terms": "الشروط وسياسة الخصوصية",
        "ai_options": "خيارات الذكاء الاصطناعي",
        "google": "ربط حساب Google",
    },
    "en": {
        "welcome": "Choose who Astro should be for you today",
        "teacher": "Astro<br>the Teacher",
        "doctor": "Astro<br>the Doctor",
        "friend": "Astro the Friend<br>& Supporter",
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
# CSS
# ============================================================
st.markdown("""
<style>
/* ===== الخلفية ===== */
.stApp {
    background: linear-gradient(135deg, #ffe0ec 0%, #ffc2d8 50%, #ffb3cc 100%) !important;
}
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
    max-width: 500px !important;
}

/* ===== ورقة الشجر ===== */
.leaf-bg {
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 80vw; max-width: 400px;
    z-index: 0;
    opacity: 0.5;
    filter: blur(20px);
    pointer-events: none;
}

/* ===== زر الإعدادات العائم ===== */
.settings-btn {
    position: fixed !important;
    top: 70px !important;
    left: 15px !important;
    z-index: 999 !important;
}
.settings-btn button {
    border-radius: 50% !important;
    width: 46px !important;
    height: 46px !important;
    min-height: 46px !important;
    background: linear-gradient(135deg, #a855f7, #7c3aed) !important;
    color: white !important;
    font-size: 20px !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.6) !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* ===== اسم ASTRO الذهبي ===== */
.astro-title {
    text-align: center;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 2.6rem;
    font-weight: 900;
    letter-spacing: 6px;
    margin: 15px 0 0 0;
    background: linear-gradient(180deg, #fff4c2 0%, #ffd966 25%, #d4a017 55%, #b8860b 75%, #fff4c2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow:
        0 0 10px rgba(255, 215, 0, 0.6),
        0 0 20px rgba(255, 215, 0, 0.4);
    position: relative; z-index: 2;
}
.astro-title::after {
    content: "✦ ─── ✦ ─── ✦";
    display: block;
    font-size: 0.65rem;
    color: #d4a017;
    letter-spacing: 4px;
    margin-top: 4px;
    -webkit-text-fill-color: #d4a017;
    text-shadow: 0 0 8px rgba(255, 215, 0, 0.7);
}

.astro-sub {
    text-align: center;
    color: #8a3d63;
    font-size: 0.95rem;
    margin: 15px 0 20px 0;
    position: relative; z-index: 2;
    padding: 0 15px;
}

/* ===== شبكة الفقاعات (2×2) - ثابتة أفقياً ===== */
.bubbles-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    max-width: 380px;
    margin: 0 auto;
    padding: 0 15px;
    position: relative; z-index: 2;
}

/* ===== الفقاعة ===== */
.bubble {
    display: flex;
    justify-content: center;
    align-items: center;
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.55), rgba(255,192,203,0.28));
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1.5px solid rgba(255, 215, 0, 0.75);
    color: #d4a017;
    font-weight: 800;
    font-size: 0.85rem;
    text-align: center;
    text-decoration: none !important;
    text-shadow:
        0 0 6px rgba(255, 215, 0, 0.9),
        0 0 12px rgba(255, 215, 0, 0.6);
    box-shadow:
        0 0 20px rgba(255, 105, 180, 0.7),
        0 0 40px rgba(255, 20, 147, 0.5),
        inset 0 0 20px rgba(255, 255, 255, 0.3);
    animation: pulse-glow 2.5s ease-in-out infinite;
    padding: 12px;
    line-height: 1.35;
    transition: transform 0.3s ease;
    box-sizing: border-box;
}
.bubble:hover {
    transform: scale(1.06);
    color: #b8860b !important;
}

@keyframes pulse-glow {
    0%, 100% {
        box-shadow:
            0 0 20px rgba(255, 105, 180, 0.7),
            0 0 40px rgba(255, 20, 147, 0.5),
            inset 0 0 20px rgba(255, 255, 255, 0.3);
    }
    50% {
        box-shadow:
            0 0 30px rgba(255, 105, 180, 0.9),
            0 0 55px rgba(255, 20, 147, 0.7),
            inset 0 0 25px rgba(255, 255, 255, 0.4);
    }
}

/* ===== تصغير على الشاشات الصغيرة ===== */
@media (max-width: 400px) {
    .astro-title { font-size: 2.2rem; letter-spacing: 4px; }
    .bubbles-grid { gap: 14px; padding: 0 10px; max-width: 340px; }
    .bubble { font-size: 0.75rem; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# ورقة الشجر
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
</svg>
</div>
""", unsafe_allow_html=True)

# ============================================================
# زر الإعدادات العائم
# ============================================================
st.markdown('<div class="settings-btn">', unsafe_allow_html=True)
with st.popover("⚙"):
    st.markdown(f"### ⚙️ {L['settings']}")

    st.markdown(f"**🌐 {L['language']}**")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("العربية", use_container_width=True, key="ar_btn"):
            st.session_state.lang = "ar"
            st.query_params.clear()
            st.rerun()
    with c2:
        if st.button("English", use_container_width=True, key="en_btn"):
            st.session_state.lang = "en"
            st.query_params.clear()
            st.rerun()

    st.divider()
    st.button(f"📜 {L['terms']}", use_container_width=True)
    st.button(f"🤖 {L['ai_options']}", use_container_width=True)

    st.divider()
    st.button(f"🔗 {L['google']}", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# العنوان
# ============================================================
st.markdown('<div class="astro-title">ASTRO</div>', unsafe_allow_html=True)
st.markdown(f'<div class="astro-sub">{L["welcome"]}</div>', unsafe_allow_html=True)

# ============================================================
# شبكة الفقاعات - HTML Grid
# ============================================================
st.markdown(f"""
<div class="bubbles-grid">
    <a href="?mode=teacher" class="bubble" target="_self">{L["teacher"]}</a>
    <a href="?mode=doctor" class="bubble" target="_self">{L["doctor"]}</a>
    <a href="?mode=friend" class="bubble" target="_self">{L["friend"]}</a>
    <a href="?mode=general" class="bubble" target="_self">{L["general"]}</a>
</div>
""", unsafe_allow_html=True)

# ============================================================
# عرض الوضع المختار
# ============================================================
if st.session_state.mode:
    st.markdown("<br>", unsafe_allow_html=True)
    selected = L[st.session_state.mode].replace("<br>", " ")
    st.success(f"✅ تم اختيار: **{selected}**")
