import streamlit as st

from data import T


def terms_page(lang):
    L = T[lang]

    if st.button(L["home"], key="bt"):
        st.session_state.page = "home"
        st.rerun()

    if lang == "ar":
        st.header("📜 الشروط والخصوصية")
        st.caption("آخر تحديث: 2026")
        st.subheader("1. الترحيب")
        st.write("ASTRO منصة محادثة ذكية.")
        st.write("استخدامك يعني موافقتك.")
        st.subheader("2. طبيعة الخدمة")
        st.write("✅ معلومات عامة فقط.")
        st.write("⚠️ لا تُغني عن مختص.")
        st.write("⚠️ قد تحتوي أخطاء.")
        st.write("❌ ليست نصيحة طبية.")
        st.subheader("3. التزاماتك")
        st.write("• استخدام مشروع فقط.")
        st.write("• لا تشارك بيانات حساسة.")
        st.subheader("4. الخصوصية")
        st.write("🔒 المحادثات في جلستك.")
        st.write("🗑️ تُحذف عند الإغلاق.")
        st.write("🚫 لا نتتبّعك.")
        st.write("💰 لا نبيع بياناتك.")
        st.subheader("5. المحتوى")
        st.write("من الذكاء الاصطناعي.")
        st.subheader("6. المسؤولية")
        st.write("يُقدَّم كما هو.")
        st.subheader("7. التعديلات")
        st.write("قد نُحدّث الشروط.")
        st.subheader("8. تواصل")
        st.write("عبر GitHub.")
        st.success("موافقتك تعني القبول 🌸")
    else:
        st.header("📜 Terms & Privacy")
        st.caption("Last updated: 2026")
        st.subheader("1. Welcome")
        st.write("ASTRO is a smart chat platform.")
        st.write("Using it means you agree.")
        st.subheader("2. Nature")
        st.write("✅ General info only.")
        st.write("⚠️ Not a specialist.")
        st.write("⚠️ May contain errors.")
        st.write("❌ Not medical advice.")
        st.subheader("3. You")
        st.write("• Use lawfully.")
        st.write("• Don't share secrets.")
        st.subheader("4. Privacy")
        st.write("🔒 Session-only chats.")
        st.write("🗑️ Lost on close.")
        st.write("🚫 No tracking.")
        st.write("💰 No data selling.")
        st.subheader("5. Content")
        st.write("AI-generated.")
        st.subheader("6. Liability")
        st.write("Provided as-is.")
        st.subheader("7. Changes")
        st.write("Terms may update.")
        st.subheader("8. Contact")
        st.write("Via GitHub.")
        st.success("Agreement means acceptance 🌸")


def ai_page(lang):
    L = T[lang]

    if st.button(L["home"], key="ba"):
        st.session_state.page = "home"
        st.rerun()

    st.header("🤖 " + L["ai_opts"])
    s = st.session_state.ai_settings

    st.subheader("🎨 " + L["creativity"])
    st.caption(L["cr_help"])
    v = st.slider(
        L["creativity"], 0.0, 1.0,
        s["creativity"], 0.1,
        label_visibility="collapsed",
    )
    s["creativity"] = v

    st.divider()
    st.subheader("📏 " + L["length"])
    opts = [L["short"], L["medium"], L["long"]]
    idx = {"short": 0, "medium": 1, "long": 2}
    cur = idx.get(s["length"], 1)
    ch = st.radio(
        L["length"], opts, index=cur,
        horizontal=True,
        label_visibility="collapsed",
    )
    s["length"] = ["short", "medium", "long"][opts.index(ch)]

    st.divider()
    st.subheader("💾 " + L["save"])
    s["save_history"] = st.toggle(
        L["save"], value=s["save_history"],
        label_visibility="collapsed",
    )

    st.divider()
    if st.button(L["clear"], use_container_width=True, key="clr"):
        for m in ["teacher", "doctor", "friend", "general"]:
            k = "sessions_" + m
            st.session_state[k] = []
            st.session_state["current_" + m] = None
        st.success(L["cleared"])

# END
