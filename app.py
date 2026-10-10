import base64
import datetime
import re
import uuid

import streamlit as st

st.set_page_config(page_title="ASTRO", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "current_id" not in st.session_state:
    st.session_state.current_id = {}
if "page" not in st.session_state:
    st.session_state.page = "home"

url_mode = st.query_params.get("mode")
if url_mode in ["teacher", "doctor", "friend", "general"]:
    st.session_state.mode = url_mode
    st.session_state.page = "chat"
elif st.session_state.page == "chat":
    st.session_state.page = "home"
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
        "back": "رجوع",
        "type_msg": "اكتب رسالتك...",
        "new_chat": "دردشة جديدة",
        "history": "السجل",
        "no_history": "لا يوجد سجل بعد",
        "back_home": "← الرئيسية",
        "voice": "🎤 رسالة صوتية",
        "attach": "📎 إرفاق",
        "camera": "📷 الكاميرا",
        "files": "📄 الملفات",
        "send": "📤 إرسال",
        "clear_all": "🗑️ مسح جميع الدردشات",
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
        "new_chat": "New chat",
        "history": "History",
        "no_history": "No history yet",
        "back_home": "← Home",
        "voice": "🎤 Voice message",
        "attach": "📎 Attach",
        "camera": "📷 Camera",
        "files": "📄 Files",
        "send": "📤 Send",
        "clear_all": "🗑️ Clear all chats",
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
    "teacher": {"ar": "سؤال رائع! 📚\n\nدعني أشرح لك بطريقة مبسطة:\n\n1. **الأساسيات**.\n2. **التطبيق**.\n\nهل تريد تفصيلاً؟", "en": "Great question! 📚\n\nLet me explain:\n\n1. **Basics**.\n2. **Application**."},
    "doctor": {"ar": "شكراً لمشاركتك 🩺\n\nنصائح عامة:\n\n• اشرب ماءً كافياً.\n• خذ قسطاً من الراحة.\n\n⚠️ **تنبيه**: معلومات عامة فقط.", "en": "Thanks 🩺\n\nGeneral tips:\n\n• Drink water.\n• Get rest.\n\n⚠️ **Note**: General info only."},
    "friend": {"ar": "أفهم ما تشعر به 💗\n\nشكراً لثقتك. أنت أقوى مما تظن. 🌸", "en": "I understand 💗\n\nThank you. You're stronger than you think. 🌸"},
    "general": {"ar": "شكراً على سؤالك ✨\n\nسؤال مثير. هل نتوسع؟", "en": "Thanks ✨\n\nInteresting question. Want to explore?"},
}

LOGO_SVG = '<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="r" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ff69b4"/><stop offset="50%" stop-color="#c026d3"/><stop offset="100%" stop-color="#a855f7"/></linearGradient><radialGradient id="s" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#fffbe6"/><stop offset="30%" stop-color="#ffe680"/><stop offset="60%" stop-color="#ffd966"/><stop offset="100%" stop-color="#b8860b"/></radialGradient></defs><circle cx="100" cy="100" r="78" fill="none" stroke="url(#r)" stroke-width="9"/><circle cx="100" cy="100" r="78" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="2.5"/><path d="M100,45 Q108,88 155,100 Q108,112 100,155 Q92,112 45,100 Q92,88 100,45 Z" fill="url(#s)" stroke="#d4a017" stroke-width="1.2" stroke-linejoin="round"/><circle cx="100" cy="100" r="4" fill="#ffffff"/></svg>'

ROSE_SVG = '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="rp1" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ffb6d5"/><stop offset="60%" stop-color="#ff69b4"/><stop offset="100%" stop-color="#c71585"/></radialGradient><radialGradient id="rp2" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ffd9e6"/><stop offset="70%" stop-color="#ff8fc0"/><stop offset="100%" stop-color="#e75480"/></radialGradient><radialGradient id="rp3" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#fff0f5"/><stop offset="100%" stop-color="#ffb6d5"/></radialGradient></defs><ellipse cx="50" cy="50" rx="42" ry="38" fill="url(#rp1)" opacity="0.9"/><path d="M50,20 Q35,30 30,50 Q28,65 40,78 Q50,85 60,78 Q72,65 70,50 Q65,30 50,20 Z" fill="url(#rp2)"/><path d="M50,32 Q42,38 40,50 Q39,60 46,68 Q50,72 54,68 Q61,60 60,50 Q58,38 50,32 Z" fill="url(#rp3)"/></svg>'

LOGO_DATA_URI = "data:image/svg+xml;base64," + base64.b64encode(LOGO_SVG.encode("utf-8")).decode("utf-8")
ROSE_DATA_URI = "data:image/svg+xml;base64," + base64.b64encode(ROSE_SVG.encode("utf-8")).decode("utf-8")


def md_to_html(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text.replace("\n", "<br>")


def new_session(mode):
    sid = str(uuid.uuid4())[:8]
    p = PERSONAS[mode][st.session_state.lang]
    sess = {
        "id": sid,
        "title": p["name"],
        "messages": [{"role": "assistant", "content": p["welcome"], "attachment": None}],
        "updated": datetime.datetime.now().isoformat(),
    }
    st.session_state.sessions.setdefault(mode, []).append(sess)
    st.session_state.current_id[mode] = sid
    return sess


def get_session(mode):
    for s in st.session_state.sessions.get(mode, []):
        if s["id"] == st.session_state.current_id.get(mode):
            return s
    return new_session(mode)


def save_session(mode):
    get_session(mode)["updated"] = datetime.datetime.now().isoformat()


CSS = "<style>"
CSS += ".stApp { background: linear-gradient(135deg, #ffe0ec 0%, #ffc2d8 50%, #ffb3cc 100%) !important; }"
CSS += "[data-testid='stHeader'] { background: transparent; }"
CSS += "#MainMenu, footer { visibility: hidden; }"
CSS += ".block-container { padding-top: 0.5rem !important; padding-bottom: 1rem !important; max-width: 500px !important; }"
CSS += ".rose { position: fixed; z-index: 0; opacity: 0.55; pointer-events: none; filter: drop-shadow(0 6px 15px rgba(199, 21, 133, 0.35)); }"
CSS += ".rose img { width: 100%; height: 100%; display: block; }"
CSS += ".rose-1 { top: -10px; left: -10px; width: 130px; height: 130px; animation: float-1 6s ease-in-out infinite; }"
CSS += ".rose-2 { top: 50px; right: -20px; width: 100px; height: 100px; animation: float-2 7s ease-in-out infinite; opacity: 0.45; }"
CSS += ".rose-3 { bottom: 30px; left: -15px; width: 110px; height: 110px; animation: float-3 8s ease-in-out infinite; opacity: 0.5; }"
CSS += ".rose-4 { bottom: -20px; right: -10px; width: 140px; height: 140px; animation: float-4 6.5s ease-in-out infinite; opacity: 0.5; }"
CSS += "@keyframes float-1 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(-5px,18px) rotate(-3deg); } }"
CSS += "@keyframes float-2 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(5px,15px) rotate(3deg); } }"
CSS += "@keyframes float-3 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(-6px,-18px) rotate(-3deg); } }"
CSS += "@keyframes float-4 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(-12px,-14px) rotate(4deg); } }"
CSS += ".settings-btn { position: fixed !important; top: 70px !important; left: 15px !important; z-index: 999 !important; }"
CSS += ".settings-btn button { border-radius: 50% !important; width: 46px !important; height: 46px !important; min-height: 46px !important; background: linear-gradient(135deg, #a855f7, #7c3aed) !important; color: white !important; font-size: 20px !important; border: none !important; box-shadow: 0 4px 15px rgba(124, 58, 237, 0.6) !important; padding: 0 !important; }"
CSS += ".logo-wrap { display: flex !important; justify-content: center !important; margin: 15px auto 5px auto !important; position: relative; z-index: 2; width: 120px; height: 120px; }"
CSS += ".logo-wrap img { width: 120px !important; height: 120px !important; display: block !important; animation: float-logo 3.5s ease-in-out infinite; filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.75)) drop-shadow(0 0 35px rgba(168, 85, 247, 0.6)); }"
CSS += "@keyframes float-logo { 0%,100% { transform: translateY(0px); } 50% { transform: translateY(-8px); } }"
CSS += ".astro-title { text-align: center; font-family: Georgia, serif; font-size: 2.4rem; font-weight: 900; letter-spacing: 6px; margin: 5px 0 0 0; background: linear-gradient(180deg, #fff4c2 0%, #ffd966 25%, #d4a017 55%, #b8860b 75%, #fff4c2 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 10px rgba(255,215,0,0.6); position: relative; z-index: 2; }"
CSS += ".astro-sub { text-align: center; color: #8a3d63; font-size: 0.95rem; margin: 15px 0 20px 0; position: relative; z-index: 2; padding: 0 15px; }"
CSS += ".bubbles-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; max-width: 380px; margin: 0 auto; padding: 0 15px; position: relative; z-index: 2; }"
CSS += ".bubble { display: flex; justify-content: center; align-items: center; aspect-ratio: 1/1; border-radius: 50%; background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.55), rgba(255,192,203,0.28)); backdrop-filter: blur(12px); border: 1.5px solid rgba(255,215,0,0.75); color: #d4a017; font-weight: 800; font-size: 0.85rem; text-align: center; text-decoration: none !important; text-shadow: 0 0 6px rgba(255,215,0,0.9); box-shadow: 0 0 20px rgba(255,105,180,0.7), 0 0 40px rgba(255,20,147,0.5); animation: pulse-glow 2.5s ease-in-out infinite; padding: 12px; line-height: 1.35; }"
CSS += "@keyframes pulse-glow { 0%,100% { box-shadow: 0 0 20px rgba(255,105,180,0.7), 0 0 40px rgba(255,20,147,0.5); } 50% { box-shadow: 0 0 30px rgba(255,105,180,0.9), 0 0 55px rgba(255,20,147,0.7); } }"
CSS += ".chat-header { display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.5); backdrop-filter: blur(15px); border-radius: 20px; padding: 12px 18px; margin: 5px 0 15px 0; box-shadow: 0 4px 20px rgba(255,105,180,0.25); position: relative; z-index: 2; }"
CSS += ".chat-persona { display: flex; align-items: center; gap: 10px; color: #6b1f4a; font-weight: 700; font-size: 1rem; }"
CSS += ".chat-persona-icon { width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }"
CSS += ".back-link { text-decoration: none !important; color: #a855f7 !important; font-size: 0.9rem; font-weight: 600; padding: 6px 12px; border-radius: 15px; background: rgba(255,255,255,0.5); }"
CSS += ".messages-container { display: flex; flex-direction: column; gap: 14px; padding: 5px 5px 15px 5px; position: relative; z-index: 2; }"
CSS += ".msg-assistant { display: flex; align-items: flex-start; gap: 10px; justify-content: flex-start; }"
CSS += ".msg-astro-icon { width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; background: radial-gradient(circle at 30% 30%, #fff4c2, #ffd966); border: 2px solid #d4a017; box-shadow: 0 3px 12px rgba(255, 215, 0, 0.5); }"
CSS += ".msg-astro-icon img { width: 28px; height: 28px; display: block; }"
CSS += ".msg-bubble-assistant { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px); border-radius: 18px 18px 18px 6px; padding: 12px 16px; color: #6b1f4a; font-size: 0.95rem; line-height: 1.6; border: 1.5px solid rgba(255, 215, 0, 0.5); max-width: 78%; word-wrap: break-word; }"
CSS += ".msg-user { display: flex; justify-content: flex-end; }"
CSS += ".msg-bubble-user { background: linear-gradient(135deg, #a855f7, #7c3aed); border-radius: 18px 18px 6px 18px; padding: 12px 16px; color: #ffffff; font-size: 0.95rem; line-height: 1.6; box-shadow: 0 3px 15px rgba(168, 85, 247, 0.4); max-width: 78%; word-wrap: break-word; }"
CSS += ".msg-attachment { margin-top: 8px; border-radius: 12px; overflow: hidden; }"
CSS += ".msg-attachment img { width: 100%; max-width: 220px; border-radius: 12px; display: block; }"
CSS += ".msg-file { display: inline-block; padding: 6px 12px; background: rgba(255,255,255,0.25); border-radius: 10px; font-size: 0.85rem; }"
CSS += "[data-testid='stChatInput'] textarea { background: rgba(255, 255, 255, 0.7) !important; border: 1.5px solid rgba(255, 215, 0, 0.6) !important; border-radius: 25px !important; color: #6b1f4a !important; }"
CSS += "[data-testid='stChatInput'] button { background: linear-gradient(135deg, #a855f7, #7c3aed) !important; border-radius: 50% !important; }"
CSS += ".page-card { background: rgba(255,255,255,0.85); border-radius: 20px; padding: 20px; margin: 10px 0; border: 1.5px solid rgba(255,215,0,0.5); color: #6b1f4a; line-height: 1.8; position: relative; z-index: 2; }"
CSS += ".page-card h3 { color: #a855f7; font-size: 1rem; margin-top: 16px; }"
CSS += ".page-card p, .page-card li { font-size: 0.9rem; }"
CSS += ".page-title { text-align: center; font-family: Georgia, serif; font-size: 1.5rem; font-weight: 900; color: #8a3d63; margin: 15px 0; position: relative; z-index: 2; }"
CSS += "@media (max-width: 400px) { .astro-title { font-size: 2rem; letter-spacing: 4px; } .bubbles-grid { gap: 14px; padding: 0 10px; max-width: 340px; } .bubble { font-size: 0.75rem; } .logo-wrap { width: 100px; height: 100px; } .logo-wrap img { width: 100px !important; height: 100px !important; } }"
CSS += "</style>"

st.markdown(CSS, unsafe_allow_html=True)

st.markdown(
    '<div class="rose rose-1"><img src="' + ROSE_DATA_URI + '" /></div>'
    + '<div class="rose rose-2"><img src="' + ROSE_DATA_URI + '" /></div>'
    + '<div class="rose rose-3"><img src="' + ROSE_DATA_URI + '" /></div>'
    + '<div class="rose rose-4"><img src="' + ROSE_DATA_URI + '" /></div>',
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
    if st.button("📜 " + L["terms"], use_container_width=True, key="terms_btn"):
        st.session_state.page = "terms"
        st.rerun()
    if st.button("🤖 " + L["ai_options"], use_container_width=True, key="ai_btn"):
        st.session_state.page = "ai_options"
        st.rerun()
    st.divider()
    st.button("🔗 " + L["google"], use_container_width=True, key="g_btn")
st.markdown('</div>', unsafe_allow_html=True)


def show_home():
    st.markdown('<div class="logo-wrap"><img src="' + LOGO_DATA_URI + '" /></div>', unsafe_allow_html=True)
    st.markdown('<div class="astro-title">ASTRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="astro-sub">' + L["welcome"] + '</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="bubbles-grid">'
        + '<a href="?mode=teacher" class="bubble" target="_self">' + L["teacher"] + '</a>'
        + '<a href="?mode=doctor" class="bubble" target="_self">' + L["doctor"] + '</a>'
        + '<a href="?mode=friend" class="bubble" target="_self">' + L["friend"] + '</a>'
        + '<a href="?mode=general" class="bubble" target="_self">' + L["general"] + '</a>'
        + '</div>',
        unsafe_allow_html=True,
    )


def show_terms():
    if st.button(L["back_home"], key="back_terms"):
        st.session_state.page = "home"
        st.rerun()

    is_ar = st.session_state.lang == "ar"

    if is_ar:
        title = "📜 الشروط وسياسة الخصوصية"
        content = "<div class='page-card'>"
        content += "<p><em>آخر تحديث: 2026</em></p>"
        content += "<h3>1. مرحباً بك في ASTRO</h3>"
        content += "<p>ASTRO منصة محادثة ذكية تقدم أربع شخصيات. باستخدامك للتطبيق، فإنك توافق على هذه الشروط.</p>"
        content += "<h3>2. طبيعة الخدمة</h3>"
        content += "<ul><li>✅ معلومات عامة وتعليمية</li><li>⚠️ لا تُغني عن استشارة مختص</li><li>⚠️ قد تحتوي على أخطاء</li><li>❌ ليست نصيحة مهنية معتمدة</li></ul>"
        content += "<h3>3. مسؤولياتك</h3>"
        content += "<ul><li>الاستخدام لأغراض مشروعة فقط.</li><li>عدم مشاركة معلومات حساسة.</li><li>عدم محاولة اختراق الخدمة.</li></ul>"
        content += "<h3>4. الخصوصية والبيانات</h3>"
        content += "<ul><li>🔒 محادثاتك تُحفظ في جلستك الحالية فقط.</li><li>🤖 قد تُرسل رسائلك إلى مزوّد الذكاء الاصطناعي.</li><li>📊 لا نتتبّع سلوكك ولا نبيع بياناتك.</li><li>🎤 التسجيلات تُعالج في جلستك فقط.</li></ul>"
        content += "<h3>5. المحتوى المُولَّد</h3>"
        content += "<p>الردود يُولّدها الذكاء الاصطناعي ولا تعبّر عن رأي المطوّرين.</p>"
        content += "<h3>6. حدود المسؤولية</h3>"
        content += "<p>يُقدَّم التطبيق كما هو. لا نتحمّل مسؤولية أي أضرار ناتجة عن استخدامه.</p>"
        content += "<h3>7. تعديلات الشروط</h3>"
        content += "<p>قد نحدّث هذه الشروط. سيتم الإشعار بالتغييرات الجوهرية.</p>"
        content += "<h3>8. تواصل</h3>"
        content += "<p>لأي استفسار، تواصل معنا عبر GitHub.</p>"
        content += "<p style='text-align:center;color:#a855f7;'><em>باستخدامك ASTRO، أنت توافق على هذه الشروط.</em></p>"
        content += "</div>"
    else:
        title = "📜 Terms & Privacy Policy"
        content = "<div class='page-card'>"
        content += "<p><em>Last updated: 2026</em></p>"
        content += "<h3>1. Welcome to ASTRO</h3>"
        content += "<p>ASTRO is a smart chat platform with four personas. By using it, you agree to these terms.</p>"
        content += "<h3>2. Nature of Service</h3>"
        content += "<ul><li>✅ General/educational info</li><li>⚠️ Doesn't replace professional advice</li><li>⚠️ May contain errors</li><li>❌ Not certified guidance</li></ul>"
        content += "<h3>3. Your Responsibilities</h3>"
        content += "<ul><li>Use for lawful purposes only.</li><li>Don't share sensitive info.</li><li>Don't attempt to hack.</li></ul>"
        content += "
