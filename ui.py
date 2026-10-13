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


def build_css(color_name):
    c = COLORS.get(color_name, COLORS["pink"])
    bg = c["bg"]
    prim = c["primary"]
    txt = c["text"]
    dark = c.get("dark", False)

    user_bg = prim
    user_txt = "#fff"
    asst_bg = "#333" if dark else "rgba(255,255,255,0.85)"
    asst_txt = "#f5f5f5" if dark else txt

    css = "<style>"
    css += ".stApp{background:" + bg + "!important;}"
    css += '[data-testid="stHeader"]{background:transparent;}'
    css += "#MainMenu,footer{visibility:hidden;}"
    css += ".block-container{padding-top:5rem!important;"
    css += "padding-bottom:6rem!important;"
    css += "max-width:500px!important;}"
    css += ".rose{position:fixed;z-index:0;opacity:0.5;"
    css += "pointer-events:none;}"
    css += ".rose img{width:100%;height:100%;display:block;}"
    css += ".rose-1{top:-10px;left:-10px;"
    css += "width:130px;height:130px;}"
    css += ".rose-2{top:50px;right:-20px;"
    css += "width:100px;height:100px;opacity:0.4;}"
    css += ".rose-3{bottom:30px;left:-15px;"
    css += "width:110px;height:110px;opacity:0.45;}"
    css += ".rose-4{bottom:-20px;right:-10px;"
    css += "width:140px;height:140px;opacity:0.45;}"

    css += ".top-bar{position:fixed!important;"
    css += "top:0!important;left:0!important;"
    css += "right:0!important;z-index:999!important;"
    css += "background:rgba(255,255,255,0.35);"
    css += "backdrop-filter:blur(15px);"
    css += "padding:8px 10px;"
    css += "box-shadow:0 2px 15px rgba(0,0,0,0.1);}"
    css += ".top-bar button{width:100%!important;"
    css += "background:rgba(255,255,255,0.5)!important;"
    css += "border:1.5px solid " + prim + "!important;"
    css += "color:" + prim + "!important;"
    css += "border-radius:12px!important;"
    css += "font-weight:600!important;"
    css += "font-size:0.85rem!important;}"
    css += ".top-bar button:hover{"
    css += "background:rgba(255,255,255,0.75)!important;}"

    # شريط ثابت داخل الشات
    css += ".chat-top{position:fixed!important;"
    css += "top:0!important;left:0!important;"
    css += "right:0!important;z-index:999!important;"
    css += "background:rgba(255,255,255,0.35);"
    css += "backdrop-filter:blur(15px);"
    css += "padding:8px 12px;"
    css += "box-shadow:0 2px 15px rgba(0,0,0,0.1);"
    css += "display:flex;align-items:center;"
    css += "justify-content:space-between;"
    css += "gap:10px;}"
    css += ".chat-top .back-btn{"
    css += "background:rgba(255,255,255,0.6)!important;"
    css += "border:1.5px solid " + prim + "!important;"
    css += "color:" + prim + "!important;"
    css += "border-radius:12px!important;"
    css += "font-weight:700!important;"
    css += "font-size:0.85rem!important;"
    css += "padding:6px 14px!important;"
    css += "text-decoration:none!important;"
    css += "white-space:nowrap;}"
    css += ".chat-top .title{"
    css += "display:flex;align-items:center;gap:8px;"
    css += "color:" + txt + ";font-weight:700;"
    css += "font-size:0.95rem;overflow:hidden;"
    css += "white-space:nowrap;text-overflow:ellipsis;}"
    css += ".chat-top .title .ico{"
    css += "width:32px;height:32px;border-radius:50%;"
    css += "display:flex;align-items:center;"
    css += "justify-content:center;font-size:18px;"
    css += "flex-shrink:0;}"
    css += ".chat-menu-btn button{"
    css += "border-radius:12px!important;"
    css += "width:42px!important;height:42px!important;"
    css += "min-height:42px!important;"
    css += "background:rgba(255,255,255,0.6)!important;"
    css += "color:" + prim + "!important;"
    css += "border:1.5px solid " + prim + "!important;"
    css += "font-size:20px!important;"
    css += "font-weight:900!important;"
    css += "padding:0!important;}"

    css += ".logo-wrap{display:flex!important;"
    css += "justify-content:center!important;"
    css += "margin:15px auto 5px auto!important;"
    css += "width:120px;height:120px;"
    css += "position:relative;z-index:2;}"
    css += ".logo-wrap img{width:120px!important;"
    css += "height:120px!important;display:block!important;}"
    css += ".astro-title{text-align:center;"
    css += "font-family:Georgia,serif;font-size:2.4rem;"
    css += "font-weight:900;letter-spacing:6px;"
    css += "background:linear-gradient(180deg,#fff4c2,"
    css += "#ffd966,#d4a017,#b8860b,#fff4c2);"
    css += "-webkit-background-clip:text;"
    css += "-webkit-text-fill-color:transparent;"
    css += "position:relative;z-index:2;}"
    css += ".astro-sub{text-align:center;color:" + txt + ";"
    css += "font-size:0.95rem;margin:15px 0 20px 0;"
    css += "padding:0 15px;position:relative;z-index:2;}"

    css += ".bubbles-grid{display:grid;"
    css += "grid-template-columns:1fr 1fr;gap:18px;"
    css += "max-width:380px;margin:0 auto;padding:0 15px;"
    css += "position:relative;z-index:2;}"
    css += ".bubble{display:flex;justify-content:center;"
    css += "align-items:center;aspect-ratio:1/1;"
    css += "border-radius:50%;"
    css += "background:rgba(255,255,255,0.35);"
    css += "border:1.5px solid rgba(255,215,0,0.7);"
    css += "color:#d4a017;font-weight:800;"
    css += "font-size:0.85rem;text-align:center;"
    css += "text-decoration:none!important;"
    css += "padding:12px;line-height:1.35;"
    css += "box-shadow:0 0 20px " + prim + "55;}"

    css += ".mc{display:flex;flex-direction:column;"
    css += "gap:14px;padding:5px;"
    css += "position:relative;z-index:2;}"
    css += ".ma{display:flex;gap:10px;"
    css += "align-items:flex-start;}"
    css += ".mai{width:38px;height:38px;"
    css += "border-radius:50%;display:flex;"
    css += "align-items:center;justify-content:center;"
    css += "flex-shrink:0;border:2px solid #d4a017;}"
    css += ".mai img{width:28px;height:28px;}"
    css += ".mba{background:" + asst_bg + ";"
    css += "border-radius:18px;padding:12px 16px;"
    css += "color:" + asst_txt + ";"
    css += "font-size:0.95rem;line-height:1.6;"
    css += "max-width:78%;}"
    css += ".mu{display:flex;justify-content:flex-end;}"
    css += ".mbu{background:" + user_bg + ";"
    css += "border-radius:18px;padding:12px 16px;"
    css += "color:" + user_txt + ";"
    css += "font-size:0.95rem;max-width:78%;}"

    css += '[data-testid="stChatInput"] textarea{'
    css += "background:rgba(255,255,255,0.7)!important;"
    css += "border:1.5px solid " + prim + "88!important;"
    css += "border-radius:25px!important;"
    css += "color:" + txt + "!important;}"
    css += '[data-testid="stChatInput"] button{'
    css += "background:" + prim + "!important;"
    css += "border-radius:50%!important;}"
    css += '[data-testid="stBottom"]{'
    css += "background:transparent!important;}'

    css += "@media(max-width:400px){"
    css += ".astro-title{font-size:2rem;letter-spacing:4px;}"
    css += ".bubbles-grid{gap:14px;padding:0 10px;"
    css += "max-width:340px;}"
    css += ".bubble{font-size:0.75rem;}"
    css += ".logo-wrap{width:100px;height:100px;}"
    css += ".logo-wrap img{width:100px!important;"
    css += "height:100px!important;}}"
    css += "</style>"
    return css


def apply_css(color_name):
    st.markdown(build_css(color_name), unsafe_allow_html=True)


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
