import streamlit as st

from data import COLORS

TPL = (
    ".stApp{background:var(--bg)!important;}"
    '[data-testid="stHeader"]{background:transparent;}'
    "#MainMenu,footer{visibility:hidden;}"
    ".block-container{padding-top:5rem!important;"
    "padding-bottom:6rem!important;max-width:500px!important;}"
    ".rose{position:fixed;z-index:0;opacity:0.5;"
    "pointer-events:none;}"
    ".rose img{width:100%;height:100%;display:block;}"
    ".rose-1{top:-10px;left:-10px;"
    "width:130px;height:130px;}"
    ".rose-2{top:50px;right:-20px;"
    "width:100px;height:100px;opacity:0.4;}"
    ".rose-3{bottom:30px;left:-15px;"
    "width:110px;height:110px;opacity:0.45;}"
    ".rose-4{bottom:-20px;right:-10px;"
    "width:140px;height:140px;opacity:0.45;}"
)

TPL += (
    ".top-bar{position:fixed!important;top:0!important;"
    "left:0!important;right:0!important;z-index:999!important;"
    "background:rgba(255,255,255,0.35);"
    "backdrop-filter:blur(15px);padding:8px 10px;"
    "box-shadow:0 2px 15px rgba(0,0,0,0.1);}"
    ".top-bar [data-testid='stPopover'] button,"
    ".top-bar [data-testid='stPopover'] > div > button{"
    "width:100%!important;"
    "background:rgba(255,255,255,0.65)!important;"
    "border:1.5px solid var(--prim)!important;"
    "color:var(--prim)!important;"
    "border-radius:12px!important;"
    "font-weight:700!important;"
    "font-size:0.85rem!important;"
    "padding:8px 6px!important;"
    "box-shadow:none!important;}"
    ".top-bar [data-testid='stPopover'] button p,"
    ".top-bar [data-testid='stPopover'] button span,"
    ".top-bar [data-testid='stPopover'] button div{"
    "color:var(--prim)!important;"
    "font-weight:700!important;}"
    ".top-bar [data-testid='stPopover'] svg{"
    "fill:var(--prim)!important;}"
)

TPL += (
    ".top-bar [data-testid='stButton'] button{"
    "width:100%!important;"
    "background:rgba(255,255,255,0.65)!important;"
    "border:1.5px solid var(--prim)!important;"
    "color:var(--prim)!important;"
    "border-radius:12px!important;"
    "font-weight:700!important;"
    "font-size:0.85rem!important;"
    "padding:8px 6px!important;"
    "box-shadow:none!important;}"
    ".top-bar [data-testid='stButton'] button p,"
    ".top-bar [data-testid='stButton'] button span,"
    ".top-bar [data-testid='stButton'] button div{"
    "color:var(--prim)!important;}"
)

TPL += (
    ".st-key-chat_top{"
    "position:fixed!important;top:0!important;"
    "left:0!important;right:0!important;"
    "z-index:999!important;"
    "background:rgba(255,255,255,0.55)!important;"
    "backdrop-filter:blur(18px)!important;"
    "padding:10px 12px 8px 12px!important;"
    "box-shadow:0 2px 15px rgba(0,0,0,0.1)!important;"
    "max-width:500px!important;"
    "margin:0 auto!important;"
    "border-radius:0 0 18px 18px!important;}"
)

TPL += (
    ".st-key-chat_top button{"
    "border-radius:12px!important;"
    "background:rgba(255,255,255,0.75)!important;"
    "color:var(--prim)!important;"
    "border:1.5px solid var(--prim)!important;"
    "font-weight:900!important;"
    "font-size:18px!important;"
    "padding:4px 6px!important;"
    "min-height:42px!important;"
    "box-shadow:none!important;}"
    ".st-key-chat_top button p,"
    ".st-key-chat_top button span,"
    ".st-key-chat_top button div{"
    "color:var(--prim)!important;"
    "font-weight:900!important;}"
    ".st-key-chat_top button:hover{"
    "background:rgba(255,255,255,0.95)!important;}"
)

TPL += (
    ".chat-title-row{display:flex;align-items:center;"
    "gap:8px;color:var(--txt);font-weight:700;"
    "font-size:0.95rem;padding:8px 0;"
    "white-space:nowrap;overflow:hidden;"
    "text-overflow:ellipsis;}"
    ".chat-title-row .ico{width:34px;height:34px;"
    "border-radius:50%;display:flex;"
    "align-items:center;justify-content:center;"
    "font-size:18px;flex-shrink:0;}"
    ".chat-title-row .nm{overflow:hidden;"
    "text-overflow:ellipsis;}"
)

# ===== زر التسجيل الصوتي =====
TPL += (
    ".voice-box{"
    "background:rgba(255,255,255,0.85)!important;"
    "border-radius:18px!important;"
    "padding:14px!important;"
    "margin:10px 0!important;"
    "border:1.5px solid var(--prim)!important;"
    "box-shadow:0 4px 20px rgba(0,0,0,0.1)!important;}"
)

TPL += (
    ".voice-row{"
    "display:flex;align-items:center;"
    "gap:10px;margin-bottom:12px;}"
    ".voice-label{"
    "color:var(--txt);font-weight:700;"
    "font-size:0.95rem;}"
)

TPL += (
    ".st-key-voice_wrap button,"
    ".st-key-voice_wrap [data-testid='stButton'] button{"
    "border-radius:14px!important;"
    "background:var(--prim)!important;"
    "color:#fff!important;"
    "border:none!important;"
    "font-weight:700!important;"
    "font-size:0.9rem!important;"
    "padding:10px 14px!important;"
    "min-height:46px!important;"
    "width:100%!important;}"
    ".st-key-voice_wrap button p,"
    ".st-key-voice_wrap button span,"
    ".st-key-voice_wrap button div{"
    "color:#fff!important;"
    "font-weight:700!important;}"
)

TPL += (
    ".logo-wrap{display:flex!important;"
    "justify-content:center!important;"
    "margin:15px auto 5px auto!important;"
    "width:120px;height:120px;"
    "position:relative;z-index:2;}"
    ".logo-wrap img{width:120px!important;"
    "height:120px!important;display:block!important;}"
    ".astro-title{text-align:center;"
    "font-family:Georgia,serif;font-size:2.4rem;"
    "font-weight:900;letter-spacing:6px;"
    "background:linear-gradient(180deg,#fff4c2,"
    "#ffd966,#d4a017,#b8860b,#fff4c2);"
    "-webkit-background-clip:text;"
    "-webkit-text-fill-color:transparent;"
    "position:relative;z-index:2;}"
    ".astro-sub{text-align:center;color:var(--txt);"
    "font-size:0.95rem;margin:15px 0 20px 0;"
    "padding:0 15px;position:relative;z-index:2;}"
)

TPL += (
    ".bubbles-grid{display:grid;"
    "grid-template-columns:1fr 1fr;gap:18px;"
    "max-width:380px;margin:0 auto;padding:0 15px;"
    "position:relative;z-index:2;}"
    ".bubble{display:flex;justify-content:center;"
    "align-items:center;aspect-ratio:1/1;"
    "border-radius:50%;"
    "background:rgba(255,255,255,0.35);"
    "border:1.5px solid rgba(255,215,0,0.7);"
    "color:#d4a017;font-weight:800;font-size:0.85rem;"
    "text-align:center;text-decoration:none!important;"
    "padding:12px;line-height:1.35;"
    "box-shadow:0 0 20px var(--prim-sh);}"
)

TPL += (
    ".mc{display:flex;flex-direction:column;gap:14px;"
    "padding:5px;position:relative;z-index:2;}"
    ".ma{display:flex;gap:10px;align-items:flex-start;}"
    ".mai{width:38px;height:38px;border-radius:50%;"
    "display:flex;align-items:center;"
    "justify-content:center;flex-shrink:0;"
    "border:2px solid #d4a017;}"
    ".mai img{width:28px;height:28px;}"
    ".mba{background:var(--asst-bg);border-radius:18px;"
    "padding:12px 16px;color:var(--asst-txt);"
    "font-size:0.95rem;line-height:1.6;max-width:78%;}"
    ".mu{display:flex;justify-content:flex-end;}"
    ".mbu{background:var(--prim);border-radius:18px;"
    "padding:12px 16px;color:#fff;"
    "font-size:0.95rem;max-width:78%;}"
)

TPL += (
    '[data-testid="stChatInput"] textarea{'
    "background:rgba(255,255,255,0.75)!important;"
    "border:1.5px solid var(--prim)!important;"
    "border-radius:25px!important;"
    "color:var(--txt)!important;}"
    '[data-testid="stChatInput"] button{'
    "background:var(--prim)!important;"
    "border-radius:50%!important;}"
    '[data-testid="stBottom"]{'
    "background:transparent!important;}"
)

TPL += (
    "@media(max-width:400px){"
    ".astro-title{font-size:2rem;letter-spacing:4px;}"
    ".bubbles-grid{gap:14px;padding:0 10px;"
    "max-width:340px;}"
    ".bubble{font-size:0.75rem;}"
    ".logo-wrap{width:100px;height:100px;}"
    ".logo-wrap img{width:100px!important;"
    "height:100px!important;}}"
)


def build_css(color_name):
    c = COLORS.get(color_name, COLORS["pink"])
    dark = c.get("dark", False)

    asst_bg = "#333" if dark else "rgba(255,255,255,0.85)"
    asst_txt = "#f5f5f5" if dark else c["text"]

    root = ":root{"
    root += "--bg:" + c["bg"] + ";"
    root += "--prim:" + c["primary"] + ";"
    root += "--txt:" + c["text"] + ";"
    root += "--prim-sh:" + c["primary"] + "55;"
    root += "--asst-bg:" + asst_bg + ";"
    root += "--asst-txt:" + asst_txt + ";"
    root += "}"

    return "<style>" + root + TPL + "</style>"


def apply_css(color_name):
    st.markdown(
        build_css(color_name),
        unsafe_allow_html=True,
    )

# END
