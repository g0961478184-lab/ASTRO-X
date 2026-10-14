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


def render(lang, mode, color):
    L = T[lang]
    p = P[mode]
    pl = p[lang]
    key = "sessions_" + mode

    session = get_current(mode, lang)
    msgs = session["msgs"]

    # ===== الشريط الثابت =====
    with st.container(key="chat_top"):
        c_title, c_back, c_menu = st.columns(
            [3, 1, 1]
        )

        with c_title:
            t = '<div class="chat-title-row">'
            t += '<span class="ico" style="background:'
            t += p["grad"] + '">'
            t += pl["icon"] + '</span>'
            t += '<span class="nm">'
            t += pl["name"] + '</span></div>'
            st.markdown(t, unsafe_allow_html=True)

        with c_back:
            if st.button(
                "←",
                key="back_btn",
                use_container_width=True,
            ):
                st.query_params.clear()
                st.session_state.page = "home"
                st.session_state.mode = None
                st.rerun()

        with c_menu:
            with st.popover(
                "☰",
                use_container_width=True,
            ):
                st.markdown("### " + L["history"])

                if st.button(
                    "➕ " + L["new_chat"],
                    use_container_width=True,
                    key="new_c",
                ):
                    new_session(mode, lang)
                    st.rerun()

                st.divider()

                sessions = st.session_state.get(key, [])
                if len(sessions) <= 1:
                    st.caption(L["no_history"])
                else:
                    ordered = sorted(
                        sessions,
                        key=lambda x: x["updated"],
                        reverse=True,
                    )
                    for s in ordered:
                        is_cur = s["id"] == session["id"]
                        cc = st.columns([4, 1])
                        with cc[0]:
                            lbl = "✅ " if is_cur else ""
                            lbl += s["title"][:18]
                            if st.button(
                                lbl,
                                key="o_" + s["id"],
                                use_container_width=True,
                            ):
                                k2 = "current_" + mode
                                st.session_state[k2] = s["id"]
                                st.rerun()
                        with cc[1]:
                            if st.button(
                                "🗑️",
                                key="d_" + s["id"],
                            ):
                                lst = st.session_state[key]
                                new_l = [
                                    x for x in lst
                                    if x["id"] != s["id"]
                                ]
                                st.session_state[key] = new_l
                                if s["id"] == session["id"]:
                                    k2 = "current_" + mode
                                    st.session_state.pop(k2, None)
                                st.rerun()

    # ===== مساحة أسفل الشريط الثابت =====
    st.markdown("<div style='height:60px;'></div>",
                unsafe_allow_html=True)

    # ===== الرسائل =====
    icon = '<div class="mai"><img src="'
    icon += LOGO_URI + '"/></div>'
    parts = ['<div class="mc">']

    for m in msgs:
        c = md(m["content"])
        if m["role"] == "assistant":
            parts.append('<div class="ma">')
            parts.append(icon)
            parts.append('<div class="mba">')
            parts.append(c)
            parts.append('</div></div>')
        else:
            parts.append('<div class="mu">')
            parts.append('<div class="mbu">')
            parts.append(c)
            parts.append('</div></div>')
    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)

    # ===== الإدخال =====
    ui = st.chat_input(L["type_msg"])
    if ui:
        msgs.append({"role": "user", "content": ui})
        r = REPLIES[mode][lang]
        msgs.append({"role": "assistant", "content": r})
        session["updated"] = (
            datetime.datetime.now().isoformat()
        )
        st.rerun()

# END
