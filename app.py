import streamlit as st

from data import KEYS, MODES, T
from page_chat import render as chat_render
from page_home import render as home_render
from page_others import ai_page, terms_page
from ui import apply_css, draw_roses

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

for k in KEYS:
    if k not in st.session_state:
        st.session_state[k] = []

um = st.query_params.get("mode")
if um in MODES:
    st.session_state.mode = um
    st.session_state.page = "chat"
elif st.session_state.page == "chat":
    st.session_state.mode = None
    st.session_state.page = "home"

L = T[st.session_state.lang]

apply_css()
draw_roses()

st.markdown(
    '<div class="settings-btn">',
    unsafe_allow_html=True,
)
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


def main():
    lang = st.session_state.lang
    page = st.session_state.page
    mode = st.session_state.mode

    if page == "terms":
        terms_page(lang)
    elif page == "ai":
        ai_page(lang)
    elif mode and mode in MODES:
        chat_render(lang, mode)
    else:
        home_render(lang)


main()
