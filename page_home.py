import streamlit as st

from data import T
from ui import LOGO_URI


def render(lang, color):
    L = T[lang]

    logo = '<div class="logo-wrap">'
    logo += '<img src="' + LOGO_URI + '"/></div>'
    st.markdown(logo, unsafe_allow_html=True)

    st.markdown(
        '<div class="astro-title">ASTRO</div>',
        unsafe_allow_html=True,
    )

    sub = '<div class="astro-sub">'
    sub += L["welcome"] + '</div>'
    st.markdown(sub, unsafe_allow_html=True)

    base = '?c=' + color + '&l=' + lang + '&mode='
    g = '<div class="bubbles-grid">'
    g += '<a href="' + base + 'teacher" class="bubble">'
    g += L["teacher"] + '</a>'
    g += '<a href="' + base + 'doctor" class="bubble">'
    g += L["doctor"] + '</a>'
    g += '<a href="' + base + 'friend" class="bubble">'
    g += L["friend"] + '</a>'
    g += '<a href="' + base + 'general" class="bubble">'
    g += L["general"] + '</a>'
    g += '</div>'
    st.markdown(g, unsafe_allow_html=True)
