import streamlit as st

from data import P, REPLIES, T
from ui import LOGO_URI, md


def render(lang, mode):
    L = T[lang]
    p = P[mode]
    pl = p[lang]
    key = "chat_" + mode

    # الترويسة
    h = '<div class="chat-header">'
    h += '<div class="chat-p">'
    h += '<div class="chat-pi" style="background:'
    h += p["grad"] + '">' + pl["icon"] + '</div>'
    h += '<span>' + pl["name"] + '</span></div>'
    h += '<a href="?" class="back-link">'
    h += '← ' + L["back"] + '</a></div>'
    st.markdown(h, unsafe_allow_html=True)

    # الرسائل
    icon = '<div class="mai"><img src="'
    icon += LOGO_URI + '"/></div>'
    parts = ['<div class="mc">']

    w = md(pl["welcome"])
    parts.append('<div class="ma">' + icon)
    parts.append('<div class="mba">' + w + '</div></div>')

    for m in st.session_state[key]:
        c = md(m["content"])
        if m["role"] == "assistant":
            parts.append('<div class="ma">' + icon)
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
        r = REPLIES[mode][lang]
        st.session_state[key].append(
            {"role": "assistant", "content": r}
        )
        st.rerun()
