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

# منع الترجمة التلقائية
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
        "title": "أسترو",
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
        "title": "ASTRO",
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
/* خلفية وردية */
.stApp {
    background: linear-gradient(135deg, #ffe0ec 0%, #ffc2d8 50%, #ffb3cc 100%) !important;
}
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 800px; }

/* ورقة الشجر المموهة في المنتصف - أوضح */
.leaf-bg {
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 85vw; max-width: 500px;
    z-index: 0;
    opacity: 0.55;
    filter: blur(18px);
    pointer-events: none;
}

/* العنوان الرئيسي */
.astro-title {
    text-align: center;
    color: #6b1f4a;
    font-size: 2.6rem;
    font-weight: 800;
    margin-top: 5px;
    margin-bottom: 5px;
    text-shadow: 0 2px 12px rgba(255,255,255,0.7);
    position: relative; z-index: 2;
}
.astro-sub {
    text-align: center;
    color: #8a3d63;
    font-size: 1rem;
    margin-bottom: 25px;
    position: relative; z-index: 2;
    padding: 0 15px;
}

/* الفقاعات الزجاجية - أصغر */
div.stButton > button {
    border-radius: 50% !important;
    width: 140px !important;
    height: 140px !important;
    min-height: 140px !important;
    background: rgba(255, 255, 255, 0.35) !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border: 1.5px solid rgba(255, 255, 255, 0.75) !important;
    color: #6b1f4a !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 10px !important;
    display: block !important;
    margin: 12px auto !important;
    box-shadow: 0 8px 28px rgba(180, 60, 120, 0.25) !important;
    white-space: pre-line !important;
    line-height: 1.3 !important;
    transition: all 0.3s ease !important;
    position: relative; z-index: 2;
}
div.stButton > button:hover {
    transform: scale(1.05);
    background: rgba(255, 255, 255, 0.5) !important;
    box-shadow: 0 12px 35px rgba(180, 60, 120, 0.4) !important;
}
div.stButton > button:focus { outline: none !important; }

/* جعل الأعمدة متساوية */
[data-testid="column"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

/* زر الإعدادات */
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

/* تصغير المسافة بين الصفوف على الجوال */
@media (max-width: 768px) {
    .astro-title { font-size: 2.2rem; }
    div.stButton > button {
        width: 130px !important;
        height: 130px !important;
        min-height: 130px !important;
        font-size: 0.85rem !important;
    }
    .block-container { padding-left: 0.5rem; padding-right: 0.5rem; }
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
    st.markdown(
        f'<div class="astro-title">🌿 {L["title"]} 🌿</div>',
        unsafe_allow_html=True,
    )

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
st.markdown(
    f'<div class="astro-sub">{L["welcome"]}</div>',
    unsafe_allow_html=True,
)

# ============================================================
# الفقاعات - تخطيط 2×2
# ============================================================
row1_c1, row1_c2 = st.columns(2)
with row1_c1:
    if st.button(L["teacher"], key="btn_teacher", use_container_width=False):
        st.session_state.mode = "teacher"
with row1_c2:
    if st.button(L["doctor"], key="btn_doctor", use_container_width=False):
        st.session_state.mode = "doctor"

row2_c1, row2_c2 = st.columns(2)
with row2_c1:
    if st.button(L["friend"], key="btn_friend", use_container_width=False):
        st.session_state.mode = "friend"
with row2_c2:
    if st.button(L["general"], key="btn_general", use_container_width=False):
        st.session_state.mode = "general"

# ============================================================
# عرض الوضع المختار
# ============================================================
if st.session_state.mode:
    st.divider()
    selected = L[st.session_state.mode].replace("\n", " ")
    st.success(f"✅ تم اختيار: **{selected}**")
