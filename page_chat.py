import datetime
import uuid

import streamlit as st

from data import P, REPLIES, T
from ui import LOGO_URI, md


def new_session(mode, lang):
    sid = str(uuid.uuid4())[:8]
    p = P[mode][lang]
    sess = {
        "id": sid,
        "title": p["name"],
        "msgs": [
            {
                "role": "assistant",
                "content": p["welcome"],
            }
        ],
        "updated": datetime.datetime.now().isoformat(),
    }
    key = "sessions_" + mode
    if key not in st.session_state:
        st.session_state[key] = []
    st.session_state[key].append(sess)
    st.session_state["current_" + mode] = sid
    return sess


def get_current(mode, lang):
    key = "sessions_" + mode
    cur_key = "current_" + mode
    if key not in st.session_state:
        st.session_state[key] = []
    sessions = st.session_state[key]
    cur = st.session_state.get(cur_key)
    for s in sessions:
        if s["id"] == cur:
            return s
    return new_session(mode, lang)


def save_ts(mode):
    s = get_current(mode, "ar")
    s["updated"] = datetime.datetime.now().isoformat()


def render(lang, mode, color):
    L = T[lang]
    p = P[mode]
    pl = p[lang]
    key = "sessions_" + mode

    # الجلسة الحالية
    session = get_current(mode, lang)
    msgs = session["msgs"]

    # ===== الشريط العلوي الثابت =====
    st.markdown(
        '<div class="chat-top">',
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns([3, 1])

    with top_left:
        back_url = "?c=" + color + "&l=" + lang
        title_html = (
            '<a href="' + back_url + '" '
            'class="back-btn" target="_self">'
            '← ' + L["back"] + '</a>'
            '<span class="title">'
            '<span class="ico" style="background:'
            + p["grad"] + '">' + pl["icon"] + '</span>'
            '<span>' + pl["name"] + '</span></span>'
        )
        st.markdown(title_html, unsafe_allow_html=True)

    with top_right:
        st.markdown(
            '<div class="chat-menu-btn">',
            unsafe_allow_html=True,
        )
        with st.popover("☰", use_container_width=True):
            st.markdown("### ☰ " + L["history"])

            if st.button(
                "➕ " + L["new_chat"],
                use_container_width=True,
                key="new_chat_btn",
            ):
                new_session(mode, lang)
                st.rerun()

            st.divider()

            sessions = st.session_state.get(key, [])
            if len(sessions) <= 1:
                st.caption(L["no_history"])
            else:
                sorted_s = sorted(
                    sessions,
                    key=lambda x: x["updated"],
                    reverse=True,
                )
                for s in sorted_s:
                    is_cur = s["id"] == session["id"]
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        lbl = ("✅ " if is_cur else "")
                        lbl += s["title"][:20]
                        if st.button(
                            lbl,
                            key="open_" + s["id"],
                            use_container_width=True,
                        ):
                            st.session_state["current_" + mode] = s["id"]
                            st.rerun()
                    with c2:
                        if st.button(
                            "🗑️",
                            key="del_" + s["id"],
                        ):
                            lst = st.session_state[key]
                            st.session_state[key] = [
                                x for x in lst if x["id"] != s["id"]
                            ]
                            if s["id"] == session["id"]:
                                st.session_state.pop(
                                    "current_" + mode, None
                                )
                            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # مسافة تحت الشريط الثابت
    st.markdown("<br><br>", unsafe_allow_html=True)

    # ===== عرض الرسائل =====
    icon = '<div class="mai"><img src="'
    icon += LOGO_URI + '"/></div>'
    parts = ['<div class="mc">']

    for m in msgs:
        c = md(m["content"])
        if m["role"] == "assistant":
            parts.append('<div class="ma">' + icon)
            parts.append('<div class="mba">' + c + '</div></div>')
        else:
            parts.append('<div class="mu">')
            parts.append('<div class="mbu">' + c + '</div></div>')
    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)

    # ===== الإدخال =====
    ui = st.chat_input(L["type_msg"])
    if ui:
        msgs.append({"role": "user", "content": ui})
        r = REPLIES[mode][lang]
        msgs.append({"role": "assistant", "content": r})
        save_ts(mode)
        st.rerun()

# END
