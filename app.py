import base64
import re

import streamlit as st

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
else:
    st.session_state.mode = None

if "lang" not in st.session_state:
    st.session_state.lang = "ar"

for m in ["teacher", "doctor", "friend", "general"]:
    if "chat_" + m not in st.session_state:
        st.session_state["chat_" + m] = []

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
        "back": "رجوع",
        "type_msg": "اكتب رسالتك...",
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
        "back": "Back",
        "type_msg": "Type your message...",
    },
}
L = T[st.session_state.lang]

PERSONAS = {
    "teacher": {
        "ar": {"name": "أسترو المعلم", "icon": "📚", "welcome": "مرحباً! أنا أسترو المعلم 📚\n\nما الموضوع الذي تريد أن نتعلمه اليوم؟"},
        "en": {"name": "Astro the Teacher", "icon": "📚", "welcome": "Hello! I'm Astro the Teacher 📚\n\nWhat would you like to learn today?"},
        "gradient": "linear-gradient(135deg, #60a5fa, #3b82f6)",
    },
    "doctor": {
        "ar": {"name": "أسترو الطبيب", "icon": "🩺", "welcome": "مرحباً! أنا أسترو الطبيب 🩺\n\nبماذا تشعر اليوم؟"},
        "en": {"name": "Astro the Doctor", "icon": "🩺", "welcome": "Hello! I'm Astro the Doctor 🩺\n\nHow do you feel today?"},
        "gradient": "linear-gradient(135deg, #5eead4, #14b8a6)",
    },
    "friend": {
        "ar": {"name": "أسترو الصديق", "icon": "💗", "welcome": "أهلاً بك يا صديقي 💗\n\nكيف حالك اليوم؟"},
        "en": {"name": "Astro the Friend", "icon": "💗", "welcome": "Hey there, my friend 💗\n\nHow are you today?"},
        "gradient": "linear-gradient(135deg, #f9a8d4, #ec4899)",
    },
    "general": {
        "ar": {"name": "أسترو", "icon": "✨", "welcome": "مرحباً! أنا أسترو ✨\n\nكيف يمكنني مساعدتك؟"},
        "en": {"name": "Astro", "icon": "✨", "welcome": "Hello! I'm Astro ✨\n\nHow can I help you?"},
        "gradient": "linear-gradient(135deg, #d8b4fe, #a855f7)",
    },
}

MOCK_REPLIES = {
    "teacher": {
        "ar": "سؤال رائع! 📚\n\nدعني أشرح:\n\n1. **الأساسيات**: نقطة مهمة.\n2. **التطبيق**: كيف تستخدمها.\n\nهل تريد تفصيلاً أكثر؟",
        "en": "Great question! 📚\n\nLet me explain:\n\n1. **Basics**: key point.\n2. **Application**: how to use it.",
    },
    "doctor": {
        "ar": "شكراً لمشاركتك 🩺\n\nنصائح عامة:\n\n• اشرب ماءً كافياً.\n• خذ قسطاً من الراحة.\n\n⚠️ **تنبيه**: معلومات عامة وليست بديلاً عن الطبيب.",
        "en": "Thanks for sharing 🩺\n\nGeneral tips:\n\n• Drink enough water.\n• Get enough rest.\n\n⚠️ **Note**: General info only.",
    },
    "friend": {
        "ar": "أفهم ما تشعر به 💗\n\nشكراً لثقتك. مشاعرك مهمة، وأنت أقوى مما تظن. 🌸",
        "en": "I understand how you feel 💗\n\nThank you for trusting me. You're stronger than you think. 🌸",
    },
    "general": {
        "ar": "شكراً على سؤالك ✨\n\nسؤال مثير للاهتمام. هل تريد أن نتوسع؟",
        "en": "Thanks for asking ✨\n\nInteresting question. Want to explore?",
    },
}

LOGO_SVG = '<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="r" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ff69b4"/><stop offset="50%" stop-color="#c026d3"/><stop offset="100%" stop-color="#a855f7"/></linearGradient><radialGradient id="s" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#fffbe6"/><stop offset="30%" stop-color="#ffe680"/><stop offset="60%" stop-color="#ffd966"/><stop offset="100%" stop-color="#b8860b"/></radialGradient></defs><circle cx="100" cy="100" r="78" fill="none" stroke="url(#r)" stroke-width="9"/><circle cx="100" cy="100" r="78" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="2.5"/><path d="M100,45 Q108,88 155,100 Q108,112 100,155 Q92,112 45,100 Q92,88 100,45 Z" fill="url(#s)" stroke="#d4a017" stroke-width="1.2" stroke-linejoin="round"/><circle cx="100" cy="100" r="4" fill="#ffffff"/></svg>'

ROSE_SVG = '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="rp1" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ffb6d5"/><stop offset="60%" stop-color="#ff69b4"/><stop offset="100%" stop-color="#c71585"/></radialGradient><radialGradient id="rp2" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ffd9e6"/><stop offset="70%" stop-color="#ff8fc0"/><stop offset="100%" stop-color="#e75480"/></radialGradient><radialGradient id="rp3" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#fff0f5"/><stop offset="100%" stop-color="#ffb6d5"/></radialGradient></defs><ellipse cx="50" cy="50" rx="42" ry="38" fill="url(#rp1)" opacity="0.9"/><path d="M50,20 Q35,30 30,50 Q28,65 40,78 Q50,85 60,78 Q72,65 70,50 Q65,30 50,20 Z" fill="url(#rp2)"/><path d="M50,32 Q42,38 40,50 Q39,60 46,68 Q50,72 54,68 Q61,60 60,50 Q58,38 50,32 Z" fill="url(#rp3)"/></svg>'

LOGO_DATA_URI = "data:image/svg+xml;base64," + base64.b64encode(LOGO_SVG.encode("utf-8")).decode("utf-8")
ROSE_DATA_URI = "data:image/svg+xml;base64," + base64.b64encode(ROSE_SVG.encode("utf-8")).decode("utf-8")


def md_to_html(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = text.replace("\n", "<br>")
    return text


st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #ffe0ec 0%, #ffc2d8 50%, #ffb3cc 100%) !important; }
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; padding-bottom: 1rem !important; max-width: 500px !important; }

.rose { position: fixed; z-index: 0; opacity: 0.55; pointer-events: none; filter: drop-shadow(0 6px 15px rgba(199, 21, 133, 0.35)); }
.rose img { width: 100%; height: 100%; display: block; }
.rose-1 { top: -10px; left: -10px; width: 130px; height: 130px; animation: float-1 6s ease-in-out infinite; }
.rose-2 { top: 50px; right: -20px; width: 100px; height: 100px; animation: float-2 7s ease-in-out infinite; opacity: 0.45; }
.rose-3 { bottom: 30px; left: -15px; width: 110px; height: 110px; animation: float-3 8s ease-in-out infinite; opacity: 0.5; }
.rose-4 { bottom: -20px; right: -10px; width: 140px; height: 140px; animation: float-4 6.5s ease-in-out infinite; opacity: 0.5; }
@keyframes float-1 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(-5px,18px) rotate(-3deg); } }
@keyframes float-2 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(5px,15px) rotate(3deg); } }
@keyframes float-3 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(-6px,-18px) rotate(-3deg); } }
@keyframes float-4 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(-12px,-14px) rotate(4deg); } }

.settings-btn { position: fixed !important; top: 70px !important; left: 15px !important; z-index: 999 !important; }
.settings-btn button { border-radius: 50% !important; width: 46px !important; height: 46px !important; min-height: 46px !important; background: linear-gradient(135deg, #a855f7, #7c3aed) !important; color: white !important; font-size: 20px !important; border: none !important; box-shadow: 0 4px 15px rgba(124, 58, 237, 0.6) !important; padding: 0 !important; }

.logo-wrap { display: flex !important; justify-content: center !important; margin: 15px auto 5px auto !important; position: relative; z-index: 2; width: 120px; height: 120px; }
.logo-wrap img { width: 120px !important; height: 120px !important; display: block !important; animation: float-logo 3.5s ease-in-out infinite; filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.75)) drop-shadow(0 0 35px rgba(168, 85, 247, 0.6)); }
@keyframes float-logo { 0%,100% { transform: translateY(0px); } 50% { transform: translateY(-8px); } }

.astro-title { text-align: center; font-family: 'Georgia', serif; font-size: 2.4rem; font-weight: 900; letter-spacing: 6px; margin: 5px 0 0 0; background: linear-gradient(180deg, #fff4c2 0%, #ffd966 25%, #d4a017 55%, #b8860b 75%, #fff4c2 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 10px rgba(255,215,0,0.6); position: relative; z-index: 2; }
.astro-title::after { content: "✦ ─── ✦ ─── ✦"; display: block; font-size: 0.65rem; color: #d4a017; letter-spacing: 4px; margin-top: 4px; -webkit-text-fill-color: #d4a017; }

.astro-sub { text-align: center; color: #8a3d63; font-size: 0.95rem; margin: 15px 0 20px 0; position: relative; z-index: 2; padding: 0 15px; }

.bubbles-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; max-width: 380px; margin: 0 auto; padding: 0 15px; position: relative; z-index: 2; }
.bubble { display: flex; justify-content: center; align-items: center; aspect-ratio: 1/1; border-radius: 50%; background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.55), rgba(255,192,203,0.28)); backdrop-filter: blur(12px); border: 1.5px solid rgba(255,215,0,0.75); color: #d4a017; font-weight: 800; font-size: 0.85rem; text-align: center; text-decoration: none !important; text-shadow: 0 0 6px rgba(255,215,0,0.9); box-shadow: 0 0 20px rgba(255,105,180,0.7), 0 0 40px rgba(255,20,147,0.5); animation: pulse-glow 2.5s ease-in-out infinite; padding: 12px; line-height: 1.35; transition: transform 0.3s ease; }
.bubble:hover { transform: scale(1.06); }
@keyframes pulse-glow { 0%,100% { box-shadow: 0 0 20px rgba(255,105,180,0.7), 0 0 40px rgba(255,20,147,0.5); } 50% { box-shadow: 0 0 30px rgba(255,105,180,0.9), 0 0 55px rgba(255,20,147,0.7); } }

.chat-header { display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.5); backdrop-filter: blur(15px); border-radius: 20px; padding: 12px 18px; margin: 5px 0 15px 0; box-shadow: 0 4px 20px rgba(255,105,180,0.25); position: relative; z-index: 2; }
.chat-persona { display: flex; align-items: center; gap: 10px; color: #6b1f4a; font-weight: 700; font-size: 1rem; }
.chat-persona-icon { width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.back-link { text-decoration: none !important; color: #a855f7 !important; font-size: 0.9rem; font-weight: 600; padding: 6px 12px; border-radius: 15px; background: rgba(255,255,255,0.5); }

.messages-container { display: flex; flex-direction: column; gap: 14px; padding: 5px 5px 15px 5px; position: relative; z-index: 2; }

.msg-assistant { display: flex; align-items: flex-start; gap: 10px; justify-content: flex-start; }
.msg-astro-icon { width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; background: radial-gradient(circle at 30% 30%, #fff4c2, #ffd966); border: 2px solid #d4a017; box-shadow: 0 3px 12px rgba(255, 215, 0, 0.5), 0 0 15px rgba(255, 105, 180, 0.3); }
.msg-astro-icon img { width: 28px; height: 28px; display: block; }
.msg-bubble-assistant { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px); border-radius: 18px 18px 18px 6px; padding: 12px 16px; color: #6b1f4a; font-size: 0.95rem; line-height: 1.6; border: 1.5px solid rgba(255, 215, 0, 0.5); box-shadow: 0 3px 12px rgba(255, 105, 180, 0.2); max-width: 78%; word-wrap: break-word; }

.msg-user { display: flex; justify-content: flex-end; }
.msg-bubble-user { background: linear-gradient(135deg, #a855f7, #7c3aed); border-radius: 18px 18px 6px 18px; padding: 12px 16px; color: #ffffff; font-size: 0.95rem; line-height: 1.6; box-shadow: 0 3px 15px rgba(168, 85, 247, 0.4); max-width: 78%; word-wrap: break-word; }

[data-testid="stChatInput"] textarea { background: rgba(255, 255, 255, 0.7) !important; border: 1.5px solid rgba(255, 215, 0, 0.6) !important; border-radius: 25px !important; color: #6b1f4a !important; font-size: 0.95rem !important; }
[data-testid="stChatInput"] textarea::placeholder { color: #a87b92 !important; }
[data-testid="stChatInput"] button { background: linear-gradient(135deg, #a855f7, #7c3aed) !important; border-radius: 50% !important; }

@media (max-width: 400px) {
    .astro-title { font-size: 2rem; letter-spacing: 4px; }
    .bubbles-grid { gap: 14px; padding: 0 10px; max-width: 340px; }
    .bubble { font-size: 0.75rem; }
    .logo-wrap { width: 100px; height: 100px; }
    .logo-wrap img { width: 100px !important; height: 100px !important; }
    .msg-bubble-assistant, .msg-bubble-user { font-size: 0.85rem; padding: 10px 14px; max-width: 82%; }
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="rose rose-1"><img src="' + ROSE_DATA_URI + '" /></div>'
    '<div class="rose rose-2"><img src="' + ROSE_DATA_URI + '" /></div>'
    '<div class="rose rose-3"><img src="' + ROSE_DATA_URI + '" /></div>'
    '<div class="rose rose-4"><img src="' + ROSE_DATA_URI + '" /></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="settings-btn">', unsafe_allow_html=True)
with st.popover("⚙"):
    st.markdown("### ⚙️ " + L["settings"])
    st.markdown("**🌐 " + L["language"] + "**")
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
    st.button("📜 " + L["terms"], use_container_width=True)
    st.button("🤖 " + L["ai_options"], use_container_width=True)
    st.divider()
    st.button("🔗 " + L["google"], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


def show_home():
    st.markdown('<div class="logo-wrap"><img src="' + LOGO_DATA_URI + '" /></div>', unsafe_allow_html=True)
    st.markdown('<div class="astro-title">ASTRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="astro-sub">' + L["welcome"] + '</div>', unsafe_allow_html=True)
    grid = (
        '<div class="bubbles-grid">'
        '<a href="?mode=teacher" class="bubble" target="_self">' + L["teacher"] + '</a>'
        '<a href="?mode=doctor" class="bubble" target="_self">' + L["doctor"] + '</a>'
        '<a href="?mode=friend" class="bubble" target="_self">' + L["friend"] + '</a>'
        '<a href="?mode=general" class="bubble" target="_self">' + L["general"] + '</a>'
        '</div>'
    )
    st.markdown(grid, unsafe_allow_html=True)


def show_chat():
    mode = st.session_state.mode
    persona = PERSONAS[mode]
    p = persona[st.session_state.lang]
    key = "chat_" + mode

    header = (
        '<div class="chat-header">'
        '<div class="chat-persona">'
        '<div class="chat-persona-icon" style="background:' + persona["gradient"] + '">'
        + p["icon"] + '</div>'
        '<span>' + p["name"] + '</span>'
        '</div>'
        '<a href="?" class="back-link" target="_self">← ' + L["back"] + '</a>'
        '</div>'
    )
    st.markdown(header, unsafe_allow_html=True)

    html_parts = ['<div class="messages-container">']

    # رسالة الترحيب - تُعرض دائماً بلغتها الحالية (لا تُخزَّن)
    welcome_html = md_to_html(p["welcome"])
    html_parts.append(
        '<div class="msg-assistant">'
        '<div class="msg-astro-icon"><img src="' + LOGO_DATA_URI + '" /></div>'
        '<div class="msg-bubble-assistant">' + welcome_html + '</div>'
        '</div>'
    )

    # بقية الرسائل
    for msg in st.session_state[key]:
        content = md_to_html(msg["content"])
        if msg["role"] == "assistant":
            html_parts.append(
                '<div class="msg-assistant">'
                '<div class="msg-astro-icon"><img src="' + LOGO_DATA_URI + '" /></div>'
                '<div class="msg-bubble-assistant">' + content + '</div>'
                '</div>'
            )
        else:
            html_parts.append(
                '<div class="msg-user">'
                '<div class="msg-bubble-user">' + content + '</div>'
                '</div>'
            )
    html_parts.append('</div>')
    st.markdown("".join(html_parts), unsafe_allow_html=True)

    user_input = st.chat_input(L["type_msg"])
    if user_input:
        st.session_state[key].append({"role": "user", "content": user_input})
        reply = MOCK_REPLIES[mode][st.session_state.lang]
        st.session_state[key].append({"role": "assistant", "content": reply})
        st.rerun()


if st.session_state.mode and st.session_state.mode in PERSONAS:
    show_chat()
else:
    show_home()
