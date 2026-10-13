import streamlit as st

from data import T


def render(lang):
    L = T[lang]

    if st.button(L["home"], key="bh"):
        st.session_state.page = "home"
        st.rerun()

    if lang == "ar":
        st.header("💬 المساعدة والدعم")
        st.caption("دليل سريع لاستخدام ASTRO")

        st.subheader("🌸 ما هو ASTRO؟")
        st.write("مساعد ذكي بأربع شخصيات.")
        st.write("يساعدك في التعلم والصحة والدعم.")

        st.subheader("🎯 الشخصيات الأربع")
        st.write("📚 **المعلم** — للتعلم والشرح.")
        st.write("🩺 **الطبيب** — نصائح صحية عامة.")
        st.write("💗 **الصديق** — دعم نفسي.")
        st.write("✨ **عام** — أي سؤال.")

        st.subheader("🚀 كيف تبدأ؟")
        st.write("1. اختر شخصية من الرئيسية.")
        st.write("2. اكتب رسالتك في الأسفل.")
        st.write("3. اضغط زر الإرسال.")

        st.subheader("🌐 تغيير اللغة")
        st.write("من الإعدادات ⚙️ اختر:")
        st.write("• العربية")
        st.write("• English")

        st.subheader("🎨 تغيير المظهر")
        st.write("من الشريط العلوي:")
        st.write("اضغط 🎨 المظهر.")
        st.write("اختر من 10 ألوان.")

        st.subheader("⚙️ خيارات AI")
        st.write("من الإعدادات:")
        st.write("• درجة الإبداع")
        st.write("• طول الردود")
        st.write("• حفظ المحادثات")

        st.subheader("💡 نصائح")
        st.write("• كن واضحاً في سؤالك.")
        st.write("• لا تشارك معلومات حساسة.")
        st.write("• تحقق من المعلومات الطبية.")

        st.subheader("📞 الدعم")
        st.write("للمساعدة:")
        st.write("راسلنا عبر GitHub.")

        st.success("استمتع باستخدام ASTRO! 🌸")

    else:
        st.header("💬 Help & Support")
        st.caption("Quick guide to use ASTRO")

        st.subheader("🌸 What is ASTRO?")
        st.write("A smart assistant with 4 personas.")
        st.write("Helps with learning, health, support.")

        st.subheader("🎯 Four Personas")
        st.write("📚 **Teacher** — for learning.")
        st.write("🩺 **Doctor** — general health tips.")
        st.write("💗 **Friend** — emotional support.")
        st.write("✨ **General** — any question.")

        st.subheader("🚀 How to start?")
        st.write("1. Pick a persona from home.")
        st.write("2. Type your message below.")
        st.write("3. Press send.")

        st.subheader("🌐 Change language")
        st.write("From Settings ⚙️ pick:")
        st.write("• العربية")
        st.write("• English")

        st.subheader("🎨 Change theme")
        st.write("From top bar:")
        st.write("Tap 🎨 Theme.")
        st.write("Pick from 10 colors.")

        st.subheader("⚙️ AI Options")
        st.write("From Settings:")
        st.write("• Creativity level")
        st.write("• Response length")
        st.write("• Save chats")

        st.subheader("💡 Tips")
        st.write("• Be clear in questions.")
        st.write("• Don't share secrets.")
        st.write("• Verify medical info.")

        st.subheader("📞 Support")
        st.write("For help:")
        st.write("Contact via GitHub.")

        st.success("Enjoy ASTRO! 🌸")
