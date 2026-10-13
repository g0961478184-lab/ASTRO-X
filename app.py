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

# ===== الحالة =====
if "page" not in st.session_state:
    st.session_state.page = "home"
if "mode" not in st.session_state:
    st.session_state.mode = None
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "ai_settings" not in st.session_state:
    st.session_state.ai_settings = {
        "creativity": 0.7,
        "length": "medium",
        "save_history": True,
    }

KEYS = [
    "chat_teacher",
    "chat_doctor",
    "chat_friend",
    "chat_general",
]

for k in KEYS:
    if k not in st.session_state:
        st.session_state[k] = []

# ===== الرابط =====
MODES = ["teacher", "doctor", "friend", "general"]
um = st.query_params.get("mode")
if um in MODES:
    st.session_state.mode = um
    st.session_state.page = "chat"
elif st.session_state.page == "chat":
    st.session_state.mode = None
    st.session_state.page = "home"

# ===== الترجمات =====
T = {
    "ar": {
        "welcome": "اختر من تريد أن يكون أسترو معك",
        "teacher": "أسترو<br>المعلم",
        "doctor": "أسترو<br>الطبيب",
        "friend": "أسترو الصديق<br>والداعم النفسي",
        "general": "عام",
        "settings": "الإعدادات",
        "language": "اللغة",
        "terms": "الشروط والخصوصية",
        "ai_opts": "خيارات الذكاء الاصطناعي",
        "google": "ربط Google",
        "back": "رجوع",
        "type_msg": "اكتب رسالتك...",
        "home": "← الرئيسية",
        "creativity": "درجة الإبداع",
        "cr_help": "منخفض = دقيق | عالي = مبدع",
        "length": "طول الردود",
        "short": "قصيرة",
        "medium": "متوسطة",
        "long": "طويلة",
        "save": "حفظ المحادثات",
        "clear": "🗑️ مسح كل المحادثات",
        "cleared": "تم المسح ✅",
    },
    "en": {
        "welcome": "Choose who Astro should be today",
        "teacher": "Astro<br>the Teacher",
        "doctor": "Astro<br>the Doctor",
        "friend": "Astro the Friend<br>& Supporter",
        "general": "General",
        "settings": "Settings",
        "language": "Language",
        "terms": "Terms & Privacy",
        "ai_opts": "AI Options",
        "google": "Connect Google",
        "back": "Back",
        "type_msg": "Type your message...",
        "home": "← Home",
        "creativity": "Creativity",
        "cr_help": "Low = precise | High = creative",
        "length": "Response length",
        "short": "Short",
        "medium": "Medium",
        "long": "Long",
        "save": "Save chats",
        "clear": "🗑️ Clear all chats",
        "cleared": "All cleared ✅",
    },
}
L = T[st.session_state.lang]

# ===== الشخصيات =====
P = {
    "teacher": {
        "ar": {
            "name": "أسترو المعلم",
            "icon": "📚",
            "welcome": "مرحباً! أنا أسترو المعلم 📚",
        },
        "en": {
            "name": "Astro the Teacher",
            "icon": "📚",
            "welcome": "Hello! I'm Astro the Teacher 📚",
        },
        "grad": "linear-gradient(135deg,#60a5fa,#3b82f6)",
    },
    "doctor": {
        "ar": {
            "name": "أسترو الطبيب",
            "icon": "🩺",
            "welcome": "مرحباً! أنا أسترو الطبيب 🩺",
        },
        "en": {
            "name": "Astro the Doctor",
            "icon": "🩺",
            "welcome": "Hello! I'm Astro the Doctor 🩺",
        },
        "grad": "linear-gradient(135deg,#5eead4,#14b8a6)",
    },
    "friend": {
        "ar": {
            "name": "أسترو الصديق",
            "icon": "💗",
            "welcome": "أهلاً بك يا صديقي 💗",
        },
        "en": {
            "name": "Astro the Friend",
            "icon": "💗",
            "welcome": "Hey there 💗",
        },
        "grad": "linear-gradient(135deg,#f9a8d4,#ec4899)",
    },
    "general": {
        "ar": {
            "name": "أسترو",
            "icon": "✨",
            "welcome": "مرحباً! أنا أسترو ✨",
        },
        "en": {
            "name": "Astro",
            "icon": "✨",
            "welcome": "Hello! I'm Astro ✨",
        },
        "grad": "linear-gradient(135deg,#d8b4fe,#a855f7)",
    },
}

# ===== الردود =====
REPLIES = {
    "teacher": {
        "ar": "سؤال رائع! 📚\n\n1. الأساسيات.\n2. التطبيق.",
        "en": "Great! 📚\n\n1. Basics.\n2. Application.",
    },
    "doctor": {
        "ar": "شكراً 🩺\n\n• اشرب ماءً.\n• خذ قسطاً من الراحة.",
        "en": "Thanks 🩺\n\n• Drink water.\n• Get rest.",
    },
    "friend": {
        "ar": "أفهمك 💗\n\nأنت أقوى مما تظن.",
        "en": "I understand 💗\n\nYou're stronger than you think.",
    },
    "general": {
        "ar": "شكراً ✨\n\nهل نتوسع؟",
        "en": "Thanks ✨\n\nWant to explore?",
    },
}

# ===== الشعارات =====
LOGO = (
    '<svg viewBox="0 0 200 200" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<defs>'
    '<linearGradient id="r" x1="0%" y1="0%" '
    'x2="100%" y2="100%">'
    '<stop offset="0%" stop-color="#ff69b4"/>'
    '<stop offset="50%" stop-color="#c026d3"/>'
    '<stop offset="100%" stop-color="#a855f7"/>'
    '</linearGradient>'
    '<radialGradient id="s" cx="50%" cy="50%" r="50%">'
    '<stop offset="0%" stop-color="#fffbe6"/>'
    '<stop offset="30%" stop-color="#ffe680"/>'
    '<stop offset="60%" stop-color="#ffd966"/>'
    '<stop offset="100%" stop-color="#b8860b"/>'
    '</radialGradient>'
    '</defs>'
    '<circle cx="100" cy="100" r="78" fill="none" '
    'stroke="url(#r)" stroke-width="9"/>'
    '<circle cx="100" cy="100" r="78" fill="none" '
    'stroke="rgba(255,255,255,0.6)" stroke-width="2.5"/>'
    '<path d="M100,45 Q108,88 155,100 Q108,112 100,155 '
    'Q92,112 45,100 Q92,88 100,45 Z" fill="url(#s)" '
    'stroke="#d4a017" stroke-width="1.2" '
    'stroke-linejoin="round"/>'
    '<circle cx="100" cy="100" r="4" fill="#ffffff"/>'
    '</svg>'
)

ROSE = (
    '<svg viewBox="0 0 100 100" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<defs>'
    '<radialGradient id="rp1" cx="50%" cy="50%" r="50%">'
    '<stop offset="0%" stop-color="#ffb6d5"/>'
    '<stop offset="60%" stop-color="#ff69b4"/>'
    '<stop offset="100%" stop-color="#c71585"/>'
    '</radialGradient>'
    '<radialGradient id="rp2" cx="50%" cy="50%" r="50%">'
    '<stop offset="0%" stop-color="#ffd9e6"/>'
    '<stop offset="70%" stop-color="#ff8fc0"/>'
    '<stop offset="100%" stop-color="#e75480"/>'
    '</radialGradient>'
    '<radialGradient id="rp3" cx="50%" cy="50%" r="50%">'
    '<stop offset="0%" stop-color="#fff0f5"/>'
    '<stop offset="100%" stop-color="#ffb6d5"/>'
    '</radialGradient>'
    '</defs>'
    '<ellipse cx="50" cy="50" rx="42" ry="38" '
    'fill="url(#rp1)" opacity="0.9"/>'
    '<path d="M50,20 Q35,30 30,50 Q28,65 40,78 '
    'Q50,85 60,78 Q72,65 70,50 Q65,30 50,20 Z" '
    'fill="url(#rp2)"/>'
    '<path d="M50,32 Q42,38 40,50 Q39,60 46,68 '
    'Q50,72 54,68 Q61,60 60,50 Q58,38 50,32 Z" '
    'fill="url(#rp3)"/>'
    '</svg>'
)

LOGO_URI = (
    "data:image/svg+xml;base64,"
    + base64.b64encode(LOGO.encode("utf-8")).decode("utf-8")
)
ROSE_URI = (
    "data:image/svg+xml;base64,"
    + base64.b64encode(ROSE.encode("utf-8")).decode("utf-8")
)


def md(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t.replace("\n", "<br>")


# ===== CSS =====
css = """
<style>
.stApp{background:linear-gradient(135deg,#ffe0ec 0%,
#ffc2d8 50%,#ffb3cc 100%)!important;}
[data-testid="stHeader"]{background:transparent;}
#MainMenu,footer{visibility:hidden;}
.block-container{padding-top:0.5rem!important;
padding-bottom:1rem!important;max-width:500px!important;}
.rose{position:fixed;z-index:0;opacity:0.55;
pointer-events:none;}
.rose img{width:100%;height:100%;display:block;}
.rose-1{top:-10px;left:-10px;width:130px;height:130px;
animation:fl1 6s ease-in-out infinite;}
.rose-2{top:50px;right:-20px;width:100px;height:100px;
animation:fl2 7s ease-in-out infinite;opacity:0.45;}
.rose-3{bottom:30px;left:-15px;width:110px;
height:110px;animation:fl3 8s ease-in-out infinite;
opacity:0.5;}
.rose-4{bottom:-20px;right:-10px;width:140px;
height:140px;animation:fl4 6.5s ease-in-out infinite;
opacity:0.5;}
@keyframes fl1{0%,100%{transform:translate(0,0);}
50%{transform:translate(-5px,18px) rotate(-3deg);}}
@keyframes fl2{0%,100%{transform:translate(0,0);}
50%{transform:translate(5px,15px) rotate(3deg);}}
@keyframes fl3{0%,100%{transform:translate(0,0);}
50%{transform:translate(-6px,-18px) rotate(-3deg);}}
@keyframes fl4{0%,100%{transform:translate(0,0);}
50%{transform:translate(-12px,-14px) rotate(4deg);}}
.settings-btn{position:fixed!important;top:70px!important;
left:15px!important;z-index:999!important;}
.settings-btn button{border-radius:50%!important;
width:46px!important;height:46px!important;
min-height:46px!important;
background:linear-gradient(135deg,#a855f7,#7c3aed)!important;
color:white!important;font-size:20px!important;
border:none!important;
box-shadow:0 4px 15px rgba(124,58,237,0.6)!important;
padding:0!important;}
.logo-wrap{display:flex!important;
justify-content:center!important;
margin:15px auto 5px auto!important;position:relative;
z-index:2;width:120px;height:120px;}
.logo-wrap img{width:120px!important;
height:120px!important;display:block!important;
animation:flL 3.5s ease-in-out infinite;}
@keyframes flL{0%,100%{transform:translateY(0);}
50%{transform:translateY(-8px);}}
.astro-title{text-align:center;font-family:Georgia,serif;
font-size:2.4rem;font-weight:900;letter-spacing:6px;
margin:5px 0 0 0;
background:linear-gradient(180deg,#fff4c2 0%,
#ffd966 25%,#d4a017 55%,#b8860b 75%,#fff4c2 100%);
-webkit-background-clip:text;background-clip:text;
-webkit-text-fill-color:transparent;
text-shadow:0 0 10px rgba(255,215,0,0.6);
position:relative;z-index:2;}
.astro-sub{text-align:center;color:#8a3d63;
font-size:0.95rem;margin:15px 0 20px 0;
position:relative;z-index:2;padding:0 15px;}
.bubbles-grid{display:grid;
grid-template-columns:1fr 1fr;gap:18px;
max-width:380px;margin:0 auto;padding:0 15px;
position:relative;z-index:2;}
.bubble{display:flex;justify-content:center;
align-items:center;aspect-ratio:1/1;
border-radius:50%;
background:radial-gradient(circle at 30% 30%,
rgba(255,255,255,0.55),rgba(255,192,203,0.28));
backdrop-filter:blur(12px);
border:1.5px solid rgba(255,215,0,0.75);
color:#d4a017;font-weight:800;font-size:0.85rem;
text-align:center;text-decoration:none!important;
text-shadow:0 0 6px rgba(255,215,0,0.9);
box-shadow:0 0 20px rgba(255,105,180,0.7),
0 0 40px rgba(255,20,147,0.5);
padding:12px;line-height:1.35;}
.bubble:hover{transform:scale(1.06);}
.chat-header{display:flex;align-items:center;
justify-content:space-between;
background:rgba(255,255,255,0.5);
backdrop-filter:blur(15px);border-radius:20px;
padding:12px 18px;margin:5px 0 15px 0;
box-shadow:0 4px 20px rgba(255,105,180,0.25);
position:relative;z-index:2;}
.chat-p{display:flex;align-items:center;gap:10px;
color:#6b1f4a;font-weight:700;font-size:1rem;}
.chat-pi{width:42px;height:42px;border-radius:50%;
display:flex;align-items:center;
justify-content:center;font-size:22px;}
.back-link{text-decoration:none!important;
color:#a855f7!important;font-size:0.9rem;
font-weight:600;padding:6px 12px;
border-radius:15px;background:rgba(255,255,255,0.5);}
.mc{display:flex;flex-direction:column;gap:14px;
padding:5px 5px 15px 5px;position:relative;z-index:2;}
.ma{display:flex;align-items:flex-start;gap:10px;
justify-content:flex-start;}
.mai{width:38px;height:38px;border-radius:50%;
display:flex;align-items:center;
justify-content:center;flex-shrink:0;
background:radial-gradient(circle at 30% 30%,
#fff4c2,#ffd966);border:2px solid #d4a017;}
.mai img{width:28px;height:28px;display:block;}
.mba{background:rgba(255,255,255,0.85);
backdrop-filter:blur(10px);
border-radius:18px 18px 18px 6px;
padding:12px 16px;color:#6b1f4a;font-size:0.95rem;
line-height:1.6;
border:1.5px solid rgba(255,215,0,0.5);
max-width:78%;word-wrap:break-word;}
.mu{display:flex;justify-content:flex-end;}
.mbu{background:linear-gradient(135deg,#a855f7,#7c3aed);
border-radius:18px 18px 6px 18px;
padding:12px 16px;color:#fff;font-size:0.95rem;
line-height:1.6;max-width:78%;word-wrap:break-word;}
[data-testid="stChatInput"] textarea{
background:rgba(255,255,255,0.7)!important;
border:1.5px solid rgba(255,215,0,0.6)!important;
border-radius:25px!important;color:#6b1f4a!important;}
[data-testid="stChatInput"] button{
background:linear-gradient(135deg,#a855f7,#7c3aed)!important;
border-radius:50%!important;}
@media(max-width:400px){
.astro-title{font-size:2rem;letter-spacing:4px;}
.bubbles-grid{gap:14px;padding:0 10px;max-width:340px;}
.bubble{font-size:0.75rem;}
.logo-wrap{width:100px;height:100px;}
.logo-wrap img{width:100px!important;
height:100px!important;}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ===== الورود =====
r1 = '<div class="rose rose-1"><img src="' + ROSE_URI + '"/></div>'
r2 = '<div class="rose rose-2"><img src="' + ROSE_URI + '"/></div>'
r3 = '<div class="rose rose-3"><img src="' + ROSE_URI + '"/></div>'
r4 = '<div class="rose rose-4"><img src="' + ROSE_URI + '"/></div>'
st.markdown(r1 + r2 + r3 + r4, unsafe_allow_html=True)

# ===== الإعدادات =====
st.markdown('<div class="settings-btn">', unsafe_allow_html=True)
with st.popover("⚙"):
    st.markdown("### ⚙️ " + L["settings"])
    st.markdown("**🌐 " + L["language"] + "**")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("العربية", use_container_width=True, key="ar"):
            st.session_state.lang = "ar"
            st.rerun()
    with c2:
        if st.button("English", use_container_width=True, key="en"):
            st.session_state.lang = "en"
            st.rerun()
    st.divider()
    if st.button("📜 " + L["terms"], use_container_width=True, key="t"):
        st.session_state.page = "terms"
        st.rerun()
    if st.button("🤖 " + L["ai_opts"], use_container_width=True, key="a"):
        st.session_state.page = "ai"
        st.rerun()
    st.divider()
    st.button("🔗 " + L["google"], use_container_width=True, key="g")
st.markdown('</div>', unsafe_allow_html=True)


# ===== الرئيسية =====
def home():
    a = '<div class="logo-wrap"><img src="' + LOGO_URI + '"/></div>'
    st.markdown(a, unsafe_allow_html=True)
    st.markdown('<div class="astro-title">ASTRO</div>',
                unsafe_allow_html=True)
    b = '<div class="astro-sub">' + L["welcome"] + '</div>'
    st.markdown(b, unsafe_allow_html=True)
    g = '<div class="bubbles-grid">'
    g += '<a href="?mode=teacher" class="bubble">'
    g += L["teacher"] + '</a>'
    g += '<a href="?mode=doctor" class="bubble">'
    g += L["doctor"] + '</a>'
    g += '<a href="?mode=friend" class="bubble">'
    g += L["friend"] + '</a>'
    g += '<a href="?mode=general" class="bubble">'
    g += L["general"] + '</a>'
    g += '</div>'
    st.markdown(g, unsafe_allow_html=True)


# ===== الشروط =====
def terms():
    if st.button(L["home"], key="bt"):
        st.session_state.page = "home"
        st.rerun()
    if st.session_state.lang == "ar":
        st.header("📜 الشروط والخصوصية")
        st.caption("آخر تحديث: 2026")
        st.subheader("1. الترحيب")
        st.write("ASTRO منصة محادثة ذكية.")
        st.write("استخدامك يعني موافقتك.")
        st.subheader("2. طبيعة الخدمة")
        st.write("✅ معلومات عامة فقط.")
        st.write("⚠️ لا تُغني عن مختص.")
        st.write("⚠️ قد تحتوي أخطاء.")
        st.write("❌ ليست نصيحة طبية.")
        st.subheader("3. التزاماتك")
        st.write("• استخدام مشروع فقط.")
        st.write("• لا تشارك بيانات حساسة.")
        st.subheader("4. الخصوصية")
        st.write("🔒 المحادثات في جلستك.")
        st.write("🗑️ تُحذف عند الإغلاق.")
        st.write("🚫 لا نتتبّعك.")
        st.write("💰 لا نبيع بياناتك.")
        st.subheader("5. المحتوى")
        st.write("من الذكاء الاصطناعي.")
        st.subheader("6. المسؤولية")
        st.write("يُقدَّم كما هو.")
        st.subheader("7. التعديلات")
        st.write("قد نُحدّث الشروط.")
        st.subheader("8. تواصل")
        st.write("عبر GitHub.")
        st.success("موافقتك تعني القبول 🌸")
    else:
        st.header("📜 Terms & Privacy")
        st.caption("Last updated: 2026")
        st.subheader("1. Welcome")
        st.write("ASTRO is a smart chat platform.")
        st.write("Using it means you agree.")
        st.subheader("2. Nature")
        st.write("✅ General info only.")
        st.write("⚠️ Not a specialist.")
        st.write("⚠️ May contain errors.")
        st.write("❌ Not medical advice.")
        st.subheader("3. You")
        st.write("• Use lawfully.")
        st.write("• Don't share secrets.")
        st.subheader("4. Privacy")
        st.write("🔒 Session-only chats.")
        st.write("🗑️ Lost on close.")
        st.write("🚫 No tracking.")
        st.write("💰 No data selling.")
        st.subheader("5. Content")
        st.write("AI-generated.")
        st.subheader("6. Liability")
        st.write("Provided as-is.")
        st.subheader("7. Changes")
        st.write("Terms may update.")
        st.subheader("8. Contact")
        st.write("Via GitHub.")
        st.success("Agreement means acceptance 🌸")


# ===== خيارات AI =====
def ai_opts():
    if st.button(L["home"], key="ba"):
        st.session_state.page = "home"
        st.rerun()
    st.header("🤖 " + L["ai_opts"])
    s = st.session_state.ai_settings
    st.subheader("🎨 " + L["creativity"])
    st.caption(L["cr_help"])
    v = st.slider(L["creativity"], 0.0, 1.0,
                  s["creativity"], 0.1,
                  label_visibility="collapsed")
    s["creativity"] = v
    st.divider()
    st.subheader("📏 " + L["length"])
    opts = [L["short"], L["medium"], L["long"]]
    idx = {"short": 0, "medium": 1, "long": 2}
    cur = idx.get(s["length"], 1)
    ch = st.radio(L["length"], opts, index=cur,
                  horizontal=True,
                  label_visibility="collapsed")
    s["length"] = ["short", "medium", "long"][opts.index(ch)]
    st.divider()
    st.subheader("💾 " + L["save"])
    s["save_history"] = st.toggle(
        L["save"], value=s["save_history"],
        label_visibility="collapsed"
    )
    st.divider()
    if st.button(L["clear"], use_container_width=True, key="clr"):
        for k in KEYS:
            st.session_state[k] = []
        st.success(L["cleared"])


# ===== الشات =====
def chat():
    mode = st.session_state.mode
    p = P[mode]
    pl = p[st.session_state.lang]
    key = "chat_" + mode

    # الترويسة
    h1 = '<div class="chat-header">'
    h1 += '<div class="chat-p">'
    h1 += '<div class="chat-pi" style="background:'
    h1 += p["grad"] + '">' + pl["icon"] + '</div>'
    h1 += '<span>' + pl["name"] + '</span></div>'
    h1 += '<a href="?" class="back-link">← ' + L["back"]
    h1 += '</a></div>'
    st.markdown(h1, unsafe_allow_html=True)

    # الرسائل
    ic = '<div class="mai"><img src="' + LOGO_URI + '"/></div>'
    parts = ['<div class="mc">']
    w = md(pl["welcome"])
    parts.append('<div class="ma">' + ic)
    parts.append('<div class="mba">' + w + '</div></div>')
    for m in st.session_state[key]:
        c = md(m["content"])
        if m["role"] == "assistant":
            parts.append('<div class="ma">' + ic)
            parts.append('<div class="mba">' + c + '</div></div>')
        else:
            parts.append('<div class="mu">')
            parts.append('<div class="mbu">' + c + '</div></div>')
    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)

    # الإدخال
    ui = st.chat_input(L["type_msg"])
    if ui:
        st.session_state[key].append(
            {"role": "user", "content": ui}
        )
        r = REPLIES[mode][st.session_state.lang]
        st.session_state[key].append(
            {"role": "assistant", "content": r}
        )
        st.rerun()


# ===== التوجيه =====
if st.session_state.page == "terms":
    terms()
elif st.session_state.page == "ai":
    ai_opts()
    
