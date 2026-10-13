import streamlit as st

from data import COLORS, KEYS, MODES, T
from page_chat import render as chat_render
from page_help import render as help_render
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

# ===== الحالة =====
if "page" not in st.session_state:
    st.session_state.page = "home"
if "mode" not in st.session_state:
    st.session_state.mode = None
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "color" not in st.session_state:
    st.session_state.color = "pink"
if "ai_settings" not in st.session_state:
    st.session_state.ai_settings = {
        "creativity": 0.7,
        "length": "medium",
        "save_history": True,
    }

for k in KEYS:
    if k not in st.session_state:
        st.session_state[k] = []

# ===== الرابط =====
um = st.query_params.get("mode")
if um in MODES:
    st.session_state.mode = um
    st.session_state.page = "chat"
elif st.session_state.page == "chat":
    st.session_state.mode = None
    st.session_state.page = "home"

L = T[st.session_state.lang]
CUR_COLOR = st.session_state.color

# ===== التصميم =====
apply_css(CUR_COLOR)
draw_roses()

# ===== الشريط العلوي =====
st.markdown(
    '<div class="top-bar">',
    unsafe_allow_html=True,
)

b1, b2, b3 = st.columns(3)

with b1:
    with st.popover(
        "⚙️ " + L["settings"],
        use_container_width=True,
    ):
        st.markdown("**🌐 " + L["language"] + "**")
        cc1, cc2 = st.columns(2)
        with cc1:
            if st.button(
                "العربية",
                use_container_width=True,
                key="lang_ar",
            ):
                st.session_state.lang = "ar"
                st.rerun()
        with cc2:
            if st.button(
                "English",
                use_container_width=True,
                key="lang_en",
            ):
                st.session_state.lang = "en"
                st.rerun()
        st.divider()
        if st.button(
            "📜 " + L["terms"],
            use_container_width=True,
            key="btn_terms",
        ):
            st.session_state.page = "terms"
            st.rerun()
        if st.button(
            "🤖 " + L["ai_opts"],
            use_container_width=True,
            key="btn_ai",
        ):
            st.session_state.page = "ai"
            st.rerun()
        st.divider()
        st.button(
            "🔗 " + L["google"],
            use_container_width=True,
            key="btn_google",
        )

with b2:
    if st.button(
        "💬 " + L["help"],
        use_container_width=True,
        key="btn_help",
    ):
        st.session_state.page = "help"
        st.rerun()

with b3:
    with st.popover(
        "🎨 " + L["theme"],
        use_container_width=True,
    ):
        st.markdown("**" + L["theme"] + "**")
        color_names = list(COLORS.keys())
        rows = [
            color_names[0:4],
            color_names[4:8],
            color_names[8:10],
        ]
        for row in rows:
            cols = st.columns(4)
            for i, cname in enumerate(row):
                with cols[i]:
                    cls = "swatch-" + cname
                    st.markdown(
                        '<div class="' + cls + '">',
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        " ",
                        key="c_" + cname,
                        use_container_width=True,
                    ):
                        st.session_state.color = cname
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ===== التوجيه =====
def main():
    lang = st.session_state.lang
    page = st.session_state.page
    mode = st.session_state.mode

    if page == "terms":
        terms_page(lang)
    elif page == "ai":
        ai_page(lang)
    elif page == "help":
        help_render(lang)
    elif mode and mode in MODES:
        chat_render(lang, mode)
    else:
        home_render(lang)


main()

# END
