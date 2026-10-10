import base64

import streamlit as st

# ============================================================
# الإعدادات
# ============================================================
st.set_page_config(
    page_title="ASTRO",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    '<meta name="google" content="notranslate">',
    unsafe_allow_html=True,
)

if "mode" in st.query_params:
    st.session_state.mode = st.query_params["mode"]

if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "mode" not in st.session_state:
    st.session_state.mode = None

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
# شعار ASTRO (Base64)
# ============================================================
LOGO_SVG = '''<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="r" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#ff69b4"/>
<stop offset="50%" stop-color="#c026d3"/>
<stop offset="100%" stop-color="#a855f7"/>
</linearGradient>
<radialGradient id="s" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="#fffbe6"/>
<stop offset="30%" stop-color="#ffe680"/>
<stop offset="60%" stop-color="#ffd966"/>
<stop offset="100%" stop-color="#b8860b"/>
</radialGradient>
</defs>
<circle cx="100" cy="100" r="78" fill="none" stroke="url(#r)" stroke-width="9"/>
<circle cx="100" cy="100" r="78" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="2.5"/>
<path d="M100,45 Q108,88 155,100 Q108,112 100,155 Q92,112 45,100 Q92,88 100,45 Z" fill="url(#s)" stroke="#d4a017" stroke-width="1.2" stroke-linejoin="round"/>
<circle cx="100" cy="100" r="4" fill="#ffffff"/>
<path d="M148,60 Q150,66 156,68 Q150,70 148,76 Q146,70 140,68 Q146,66 148,60 Z" fill="#fffbe6" opacity="0.9"/>
<path d="M52,132 Q54,138 60,140 Q54,142 52,148 Q50,142 44,140 Q50,138 52,132 Z" fill="#fffbe6" opacity="0.85"/>
</svg>'''

# ============================================================
# وردة (Base64 SVG)
# ============================================================
ROSE_SVG = '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
<defs>
<radialGradient id="rp1" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="#ffb6d5"/>
<stop offset="60%" stop-color="#ff69b4"/>
<stop offset="100%" stop-color="#c71585"/>
</radialGradient>
<radialGradient id="rp2" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="#ffd9e6"/>
<stop offset="70%" stop-color="#ff8fc0"/>
<stop offset="100%" stop-color="#e75480"/>
</radialGradient>
<radialGradient id="rp3" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="#fff0f5"/>
<stop offset="100%" stop-color="#ffb6d5"/>
</radialGradient>
</defs>
<ellipse cx="50" cy="50" rx="42" ry="38" fill="url(#rp1)" opacity="0.9"/>
<path d="M50,20 Q35,30 30,50 Q28,65 40,78 Q50,85 60,78 Q72,65 70,50 Q65,30 50,20 Z" fill="url(#rp2)"/>
<path d="M50,32 Q42,38 40,50 Q39,60 46,68 Q50,72 54,68 Q61,60 60,50 Q58,38 50,32 Z" fill="url(#rp3)"/>
<path d="M50,42 Q46,46 45,52 Q45,58 50,60 Q55,58 55,52 Q54,46 50,42 Z" fill="#ffffff" opacity="0.7"/>
<path d="M50,48 Q48,50 48,52 Q48,55 50,55 Q52,55 52,52 Q52,50 50,48 Z" fill="#ffe0ec"/>
</svg>'''

LOGO_B64 = base64.b64encode(LOGO_SVG.encode("utf-8")).decode("utf-8")
LOGO_DATA_URI = f"data:image/svg+xml;base64,{LOGO_B64}"

ROSE_B64 = base64.b64encode(ROSE_SVG.encode("utf-8")).decode("utf-8")
ROSE_DATA_URI = f"data:image/svg+xml;base64,{ROSE_B64}"

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
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

/* ===== ورود الخلفية ===== */
.rose {
    position: fixed;
    z-index: 0;
    opacity: 0.55;
    pointer-events: none;
    filter: drop-shadow(0 6px 15px rgba(199, 21, 133, 0.35));
}
.rose img {
    width: 100%;
    height: 100%;
    display: block;
}

/* المواقع الأربعة */
.rose-1 {
    top: -10px; left: -10px;
    width: 130px; height: 130px;
    animation: float-1 6s ease-in-out infinite;
}
.rose-2 {
    top: 50px; right: -20px;
    width: 100px; height: 100px;
    animation: float-2 7s ease-in-out infinite;
    opacity: 0.45;
}
.rose-3 {
    bottom: 30px; left: -15px;
    width: 110px; height: 110px;
    animation: float-3 8s ease-in-out infinite;
    opacity: 0.5;
}
.rose-4 {
    bottom: -20px; right: -10px;
    width: 140px; height: 140px;
    animation: float-4 6.5s ease-in-out infinite;
    opacity: 0.5;
}

/* تأثيرات الطفو المتنوعة */
@keyframes float-1 {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    25% { transform: translate(8px, 12px) rotate(4deg); }
    50% { transform: translate(-5px, 18px) rotate(-3deg); }
    75% { transform: translate(6px, 8px) rotate(2deg); }
}
@keyframes float-2 {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    33% { transform: translate(-10px, 15px) rotate(-5deg); }
    66% { transform: translate(5px, 8px) rotate(3deg); }
}
@keyframes float-3 {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    33% { transform: translate(12px, -10px) rotate(5deg); }
    66% { transform: translate(-6px, -18px) rotate(-3deg); }
}
@keyframes float-4 {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    50% { transform: translate(-12px, -14px) rotate(4deg); }
}

/* ===== زر الإعدادات ===== */
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

/* ===== الشعار ===== */
.logo-wrap {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    margin: 15px auto 5px auto !important;
    position: relative;
    z-index: 2;
    width: 120px;
    height: 120px;
}
.logo-wrap img {
    width: 120px !important;
    height: 120px !important;
    display: block !important;
    animation: float-logo 3.5s ease-in-out infinite;
    filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.75))
            drop-shadow(0 0 35px rgba(168, 85, 247, 0.6));
}
@keyframes float-logo {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

.astro-title {
    text-align: center;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 2.4rem;
    font-weight: 900;
    letter-spacing: 6px;
    margin: 5px 0 0 0;
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

.bubbles-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    max-width: 380px;
    margin: 0 auto;
    padding: 0 15px;
    position: relative; z-index: 2;
}

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

@media (max-width: 400px) {
    .rose-1 { width: 100px; height: 100px; }
    .rose-2 { width: 80px; height: 80px; }
    .rose-3 { width: 90px; height: 90px; }
    .rose-4 { width: 110px; height: 110px; }
    .logo-wrap { width: 100px; height: 100px; }
    .logo-wrap img { width: 100px !important; height: 100px !important; }
    .astro-title { font-size: 2rem; letter-spacing: 4px; }
    .bubbles-grid { gap: 14px; padding: 0 10px; max-width: 340px; }
    .bubble { font-size: 0.75rem; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# الورود الأربع في الخلفية
# ============================================================
st.markdown(f"""
<div class="rose rose-1"><img src="{ROSE_DATA_URI}" alt="rose" /></div>
<div class="rose rose-2"><img src="{ROSE_DATA_URI}" alt="rose" /></div>
<div class="rose rose-3"><img src="{ROSE_DATA_URI}" alt="rose" /></div>
<div class="rose rose-4"><img src="{ROSE_DATA_URI}" alt="rose" /></div>
""", unsafe_allow_html=True)

# ============================================================
# زر الإعدادات
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
# شعار ASTRO
# ============================================================
st.markdown(
    f'<div class="logo-wrap"><img src="{LOGO_DATA_URI}" alt="ASTRO" /></div>',
    unsafe_allow_html=True,
)

# ============================================================
# العنوان
# ============================================================
st.markdown('<div class="astro-title">ASTRO</div>', unsafe_allow_html=True)
st.markdown(f'<div class="astro-sub">{L["welcome"]}</div>', unsafe_allow_html=True)

# ============================================================
# الفقاعات
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
# عرض الوضع
# ============================================================
if st.session_state.mode:
    st.markdown("<br>", unsafe_allow_html=True)
    selected = L[st.session_state.mode].replace("<br>", " ")
    st.success(f"✅ تم اختيار: **{selected}**")
