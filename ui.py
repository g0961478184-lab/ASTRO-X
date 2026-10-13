import base64
import re

import streamlit as st

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


CSS = """
<style>
.stApp{background:linear-gradient(135deg,#ffe0ec,
#ffc2d8,#ffb3cc)!important;}
[data-testid="stHeader"]{background:transparent;}
#MainMenu,footer{visibility:hidden;}
.block-container{padding-top:0.5rem!important;
max-width:500px!important;}
.rose{position:fixed;z-index:0;opacity:0.55;
pointer-events:none;}
.rose img{width:100%;height:100%;display:block;}
.rose-1{top:-10px;left:-10px;width:130px;
height:130px;}
.rose-2{top:50px;right:-20px;width:100px;
height:100px;opacity:0.45;}
.rose-3{bottom:30px;left:-15px;width:110px;
height:110px;opacity:0.5;}
.rose-4{bottom:-20px;right:-10px;width:140px;
height:140px;opacity:0.5;}
.settings-btn{position:fixed!important;
top:70px!important;left:15px!important;
z-index:999!important;}
.settings-btn button{border-radius:50%!important;
width:46px!important;height:46px!important;
background:linear-gradient(135deg,#a855f7,
#7c3aed)!important;color:#fff!important;
font-size:20px!important;border:none!important;
padding:0!important;}
.logo-wrap{display:flex!important;
justify-content:center!important;
margin:15px auto 5px auto!important;
width:120px;height:120px;position:relative;
z-index:2;}
.logo-wrap img{width:120px!important;
height:120px!important;display:block!important;}
.astro-title{text-align:center;
font-family:Georgia,serif;font-size:2.4rem;
font-weight:900;letter-spacing:6px;
background:linear-gradient(180deg,#fff4c2,
#ffd966,#d4a017,#b8860b,#fff4c2);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
position:relative;z-index:2;}
.astro-sub{text-align:center;color:#8a3d63;
font-size:0.95rem;margin:15px 0 20px 0;
padding:0 15px;position:relative;z-index:2;}
.bubbles-grid{display:grid;
grid-template-columns:1fr 1fr;gap:18px;
max-width:380px;margin:0 auto;padding:0 15px;
position:relative;z-index:2;}
.bubble{display:flex;justify-content:center;
align-items:center;aspect-ratio:1/1;
border-radius:50%;
background:radial-gradient(circle at 30% 30%,
rgba(255,255,255,0.55),rgba(255,192,203,0.28));
border:1.5px solid rgba(255,215,0,0.75);
color:#d4a017;font-weight:800;font-size:0.85rem;
text-align:center;text-decoration:none!important;
padding:12px;line-height:1.35;
box-shadow:0 0 20px rgba(255,105,180,0.7);}
.chat-header{display:flex;align-items:center;
justify-content:space-between;
background:rgba(255,255,255,0.5);
border-radius:20px;padding:12px 18px;
margin:5px 0 15px 0;position:relative;z-index:2;}
.chat-p{display:flex;align-items:center;
gap:10px;color:#6b1f4a;font-weight:700;}
.chat-pi{width:42px;height:42px;
border-radius:50%;display:flex;
align-items:center;justify-content:center;
font-size:22px;}
.back-link{text-decoration:none!important;
color:#a855f7!important;font-size:0.9rem;
padding:6px 12px;border-radius:15px;
background:rgba(255,255,255,0.5);}
.mc{display:flex;flex-direction:column;
gap:14px;padding:5px;position:relative;
z-index:2;}
.ma{display:flex;gap:10px;
align-items:flex-start;}
.mai{width:38px;height:38px;
border-radius:50%;display:flex;
align-items:center;justify-content:center;
flex-shrink:0;border:2px solid #d4a017;}
.mai img{width:28px;height:28px;}
.mba{background:rgba(255,255,255,0.85);
border-radius:18px;padding:12px 16px;
color:#6b1f4a;font-size:0.95rem;
line-height:1.6;max-width:78%;}
.mu{display:flex;justify-content:flex-end;}
.mbu{background:linear-gradient(135deg,
#a855f7,#7c3aed);border-radius:18px;
padding:12px 16px;color:#fff;
font-size:0.95rem;max-width:78%;}
</style>
"""


def apply_css():
    st.markdown(CSS, unsafe_allow_html=True)


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
