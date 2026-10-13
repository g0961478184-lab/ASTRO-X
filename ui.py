import base64
import re

import streamlit as st

from data import COLORS

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
    '<path d="M100,45 Q108,88 155,100 Q108,112 '
    '100,155 Q92,112 45,100 Q92,88 100,45 Z" '
    'fill="url(#s)" stroke="#d4a017"/>'
    '<circle cx="100" cy="100" r="4" fill="#fff"/>'
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
    '<stop offset="100%" stop-color="#e75480"/>'
    '</radialGradient>'
    '</defs>'
    '<ellipse cx="50" cy="50" rx="42" ry="38" '
    'fill="url(#rp1)" opacity="0.9"/>'
    '<path d="M50,20 Q35,30 30,50 Q28,65 40,78 '
    'Q50,85 60,78 Q72,65 70,50 Q65,30 50,20 Z" '
    'fill="url(#rp2)"/>'
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


# القالب الثابت (يستخدم CSS Variables)
TPL = (
    ".stApp{background:var(--bg)!important;}"
    '[data-testid="stHeader"]{background:transparent;}'
    "#MainMenu,footer{visibility:hidden;}"
    ".block-container{padding-top:5rem!important;"
    "padding-bottom:6rem!important;max-width:500px!important;}"
    ".rose{position:fixed;z-index:0;opacity:0.5;"
    "pointer-events:none;}"
    ".rose img{width:100%;height:100%;display:block;}"
    ".rose-1{top:-10px;left:-10px;width:130px;height:130px;}"
    ".rose-2{top:50px;right:-20px;width:100px;"
    "height:100px;opacity:0.4;}"
    ".rose-3{bottom:30px;left:-15px;width:110px;"
    "height:110px;opacity:0.45;}"
    ".rose-4{bottom:-20px;right:-10px;width:140px;"
    "height:140px;opacity:0.45;}"
    ".top-bar{position:fixed!important;top:0!important;"
    "left:0!important;right:0!important;z-index:999!important;"
    "background:rgba(255,255,255,0.35);"
    "backdrop-filter:blur(15px);padding:8px 10px;"
    "box-shadow:0 2px 15px rgba(0,0,0,0.1);}"
    ".top-bar button{width:100%!important;"
    "background:rgba(255,255,255,0.5)!important;"
    "border:1.5px solid var(--prim)!important;"
    "color:var(--prim)!important;"
    "border-radius:12px!important;font-weight:600!important;"
    "font-size:0.85rem!important;}"
    ".chat-top{position:fixed!important;top:0!important;"
    "left:0!important;right:0!important;z-index:999!important;"
    "background:rgba(255,255,255,0.4);"
    "backdrop-filter:blur(15px);padding:10px 12px;"
    "box-shadow:0 2px 15px rgba(0,0,0,0.1);}"
    ".back-btn{display:inline-block;"
    "background:rgba(255,255,255,0.7);"
    "border:1.5px solid var(--prim);"
    "color:var(--prim)!important;"
    "border-radius:12px;font-weight:700;"
    "font-size:0.85rem;padding:6px 14px;"
    "text-decoration:none!important;margin-right:10px;}"
    ".chat-menu-btn button{border-radius:12px!important;"
    "width:42px!important;height:42px!important;"
    "min-height:42px!important;"
    "background:rgba(255,255,255,0.7)!important;"
    "color:var(--prim)!important;"
    "border:1.5px solid var(--prim)!important;"
    "font-size:20px!important;font-weight:900!important;"
    "padding:0!important;}"
    ".logo-wrap{display:flex!important;"
    "justify-content:center!important;"
    "margin:15px auto 5px auto!important;"
    "width:120px;height:120px;position:relative;z-index:2;}"
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
    ".bubbles-grid{display:grid;"
    "grid-template-columns:1fr 1fr;gap:18px;"
    "max-width:380px;margin:0 auto;padding:0 15px;"
    "position:relative;z-index:2;}"
    ".bubble{display:flex;justify-content:center;"
    "align-items:center;aspect-ratio:1/1;"
    "border-radius:50%;background:rgba(255,255,255,0.35);"
    "border:1.5px solid rgba(255,215,0,0.7);"
    "color:#d4a017;font-weight:800;font-size:0.85rem;"
    "text-align:center;text-decoration:none!important;"
    "padding:12px;line-height:1.35;"
    "box-shadow:0 0 20px var(--prim-sh);}"
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
    '[data-testid="stChatInput"] textarea{'
    "background:rgba(255,255,255,0.75)!important;"
    "border:1.5px solid var(--prim)!important;"
    "border-radius:25px!important;"
    "color:var(--txt)!important;}"
    '[data-testid="stChatInput"] button{'
    "background:var(--prim)!important;"
    "border-radius:50%!important;}"
    '[data-testid="stBottom"]{background:transparent!important;}'
    "@media(max-width:400px){"
    ".astro-title{font-size:2rem;letter-spacing:4px;}"
    ".bubbles-grid{gap:14px;padding:0 10px;"
    "max-width:340px;}.bubble{font-size:0.75rem;}"
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


def draw_roses():
    r = '<div class="rose rose-1">'
    r += '<img src="' + ROSE_URI + '"/></div>'
    r += '<div class="rose rose-2">'
    r += '<img src="' + ROSE_URI + '"/></div>'
    r += '<div class="rose rose-3">'
    r += '<img src="' + ROSE_URI + '"/></div>'
    r += '<div class="rose rose-4">'
    r += '<img src="' + ROSE_URI + '"/></div>'
    st.markdown(r, unsafe_allow_html=True)

# END
