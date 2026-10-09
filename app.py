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

# حالة اللغة والوضع
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "mode" not in st.session_state:
    st.session_state.mode = None

# الترجمات
T = {
    "ar": {
        "title": "أسترو",
        "welcome": "اختر من تريد أن يكون أسترو معك اليوم",
        "teacher": "أسترو المعلم",
        "doctor": "أسترو الطبيب",
        "friend": "أسترو الصديق\nوالداعم النفسي",
        "general": "عام",
        "settings": "الإعدادات",
        "language": "اللغة",
        "terms": "الشروط وسياسة الخصوصية",
        "ai_options": "خيارات الذكاء الاصطناعي",
        "google": "ربط حساب Google",
    },
    "en": {
        "title": "ASTRO",
        "welcome": "Choose who Astro should be for you today",
        "teacher": "Astro the Teacher",
        "doctor": "Astro the Doctor",
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
/* خلفية وردية */
.stApp {
    background: linear-gradient(135deg, #ffe0ec 0%, #ffc2d8 50%, #ffb3cc 100%) !important;
}
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 1rem; max-width: 900px; }

/* ورقة الشجر المموهة في المنتصف */
.leaf-bg {
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 90vw; max-width: 700px;
    z-index: 0;
    opacity: 0.45;
    filter: blur(25px);
    pointer-events: none;
}

/* العنوان الرئيسي */
.astro-title {
    text-align: center;
    color: #6b1f4a;
    font-size: 3.2rem;
    font-weight: 800;
    margin-top: 10px;
    text-shadow: 0 2px 12px rgba(255,255,255,0.6);
    position: relative; z-index: 2;
}
.astro-sub {
    text-align: center;
    color: #8a3d63;
    font-size: 1.05rem;
    margin-bottom: 35px;
    position: relative; z-index: 2;
}

/* الفقاعات الزجاجية (الأزرار) */
div.stButton > button {
    border-radius: 50% !important;
    width: 200px !important;
    height: 200px !important;
    min-height: 200px !important;
    background: rgba(255, 255, 255, 0.28) !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border: 1.5px solid rgba(255, 255, 255, 0.6) !important;
    color: #6b1f4a !important;
    font-weight: 700 !important;
    font-size: 1.02rem !important;
    padding: 20px !important;
    display: block !important;
    margin: 15px auto !important;
    box-shadow: 0 8px 32px rgba(180, 60, 120, 0.25) !important;
    white-space: pre-line !important;
    line-height: 1.4 !important;
    transition: all 0.3s ease !important;
    position: relative; z-index: 2;
}
div.stButton > button:hover {
    transform: scale(1.06);
    background: rgba(255, 255, 255, 0.45) !important;
    box-shadow: 0 12px 40px rgba(180, 60, 120, 0.4) !important;
}
div.stButton > button:focus { outline: none !important; }

/* زر الإعدادات (الترس) */
.settings-gear button {
    border-radius: 50% !important;
    width: 52px !important;
    height: 52px !important;
    min-height: 52px !important;
    background: linear-gradient(135deg, #a855f7, #7c3aed) !important;
    color: white !important;
    font-size: 22px !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.5) !important;
    padding: 0 !important;
    margin: 0 !important;
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
      <stop offset="100%" stop-color="#ff1493" stop-opacity="0.6"/>
    </radialGradient>
  </defs>
  <path fill="url(#g1)" d="M100,10 C50,10 20,50 20,100 C20,150 50,190 100,190 C150,190 180,150 180,100 C180,50 150,10 100,10 Z"/>
  <path fill="#ffc2d8" d="M100,40 C75,40 60,70 60,100 C60,130 75,160 100,160 C125,160 140,130 140,100 C140,70 125,40 100,40 Z"/>
  <path fill="#ff69b4" d="M100,70 C90,70 85,85 85,100 C85,115 90,130 100,130 C110,130 115,115 115,100 C115,85 110,70 100,70 Z"/>
</svg>
</div>
""", unsafe_allow_html=True)

# ============================================================
# الترويسة (العنوان + زر الإعدادات في الأعلى يمين)
# ============================================================
col_title, col_gear = st.columns([6, 1])

with col_title:
    st.markdown(
        f'<div class="astro-title">🌿 {L["title"]} 🌿</div>',
        unsafe_allow_html=True,
    )

with col_gear:
    st.markdown('<div class="settings-gear">', unsafe_allow_html=True)
    with st.popover("⚙"):
        st.markdown(f"### ⚙️ {L['settings']}")

        # اللغة
        st.markdown(f"**🌐 {L['language']}**")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("العربية", use_container_width=True):
                st.session_state.lang = "ar"
                st.rerun()
        with c2:
            if st.button("English", use_container_width=True):
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
st.markdown(
    f'<div class="astro-sub">{L["welcome"]}</div>',
    unsafe_allow_html=True,
)

# ============================================================
# الفقاعات الزجاجية الأربع
# ============================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button(L["teacher"], key="btn_teacher", use_container_width=True):
        st.session_state.mode = "teacher"

with c2:
    if st.button(L["doctor"], key="btn_doctor", use_container_width=True):
        st.session_state.mode = "doctor"

with c3:
    if st.button(L["friend"], key="btn_friend", use_container_width=True):
        st.session_state.mode = "friend"

with c4:
    if st.button(L["general"], key="btn_general", use_container_width=True):
        st.session_state.mode = "general"

# ============================================================
# عرض الوضع المختار
# ============================================================
if st.session_state.mode:
    st.divider()
    selected = L[st.session_state.mode].replace("\n", " ")
    st.success(f"✅ تم اختيار: **{selected}**")
