MODES = ["teacher", "doctor", "friend", "general"]

COLORS = {
    "pink": {
        "ar": "وردي", "en": "Pink", "emoji": "🌸",
        "bg": "linear-gradient(135deg,#ffe0ec,#ffc2d8,#ffb3cc)",
        "primary": "#a855f7",
        "text": "#6b1f4a",
    },
    "red": {
        "ar": "أحمر", "en": "Red", "emoji": "🔴",
        "bg": "linear-gradient(135deg,#ffe0e0,#ffb3b3,#ff8080)",
        "primary": "#dc2626",
        "text": "#7f1d1d",
    },
    "orange": {
        "ar": "برتقالي", "en": "Orange", "emoji": "🟠",
        "bg": "linear-gradient(135deg,#ffe8cc,#ffcc99,#ffb366)",
        "primary": "#ea580c",
        "text": "#7c2d12",
    },
    "yellow": {
        "ar": "أصفر", "en": "Yellow", "emoji": "🟡",
        "bg": "linear-gradient(135deg,#fff9cc,#ffed99,#ffe066)",
        "primary": "#ca8a04",
        "text": "#713f12",
    },
    "green": {
        "ar": "أخضر", "en": "Green", "emoji": "🟢",
        "bg": "linear-gradient(135deg,#d4f4dd,#a7e6b8,#7dd88f)",
        "primary": "#16a34a",
        "text": "#14532d",
    },
    "blue": {
        "ar": "أزرق", "en": "Blue", "emoji": "🔵",
        "bg": "linear-gradient(135deg,#d4e8ff,#a7cfff,#7bb6ff)",
        "primary": "#2563eb",
        "text": "#1e3a8a",
    },
    "indigo": {
        "ar": "نيلي", "en": "Indigo", "emoji": "🟣",
        "bg": "linear-gradient(135deg,#e0e7ff,#c7d2fe,#a5b4fc)",
        "primary": "#4f46e5",
        "text": "#312e81",
    },
    "purple": {
        "ar": "بنفسجي", "en": "Purple", "emoji": "🟪",
        "bg": "linear-gradient(135deg,#e9d5ff,#d8b4fe,#c084fc)",
        "primary": "#9333ea",
        "text": "#581c87",
    },
    "white": {
        "ar": "أبيض", "en": "White", "emoji": "⚪",
        "bg": "linear-gradient(135deg,#ffffff,#f5f5f5,#e5e5e5)",
        "primary": "#6b7280",
        "text": "#1f2937",
    },
    "black": {
        "ar": "أسود", "en": "Black", "emoji": "⚫",
        "bg": "linear-gradient(135deg,#2a2a2a,#1a1a1a,#000)",
        "primary": "#a855f7",
        "text": "#f5f5f5",
        "dark": True,
    },
}

T = {
    "ar": {
        "welcome": "اختر من تريد",
        "teacher": "أسترو<br>المعلم",
        "doctor": "أسترو<br>الطبيب",
        "friend": "أسترو الصديق",
        "general": "عام",
        "settings": "الإعدادات",
        "language": "اللغة",
        "terms": "الشروط",
        "ai_opts": "خيارات AI",
        "google": "ربط Google",
        "back": "رجوع",
        "type_msg": "اكتب...",
        "home": "← الرئيسية",
        "creativity": "الإبداع",
        "cr_help": "منخفض = دقيق",
        "length": "الطول",
        "short": "قصيرة",
        "medium": "متوسطة",
        "long": "طويلة",
        "save": "حفظ المحادثات",
        "clear": "مسح الكل",
        "cleared": "تم ✅",
        "help": "المساعدة",
        "theme": "المظهر",
        "new_chat": "دردشة جديدة",
        "history": "السجل",
        "no_history": "لا يوجد سجل بعد",
    },
    "en": {
        "welcome": "Choose who Astro should be",
        "teacher": "Astro<br>the Teacher",
        "doctor": "Astro<br>the Doctor",
        "friend": "Astro the Friend",
        "general": "General",
        "settings": "Settings",
        "language": "Language",
        "terms": "Terms",
        "ai_opts": "AI Options",
        "google": "Connect Google",
        "back": "Back",
        "type_msg": "Type...",
        "home": "← Home",
        "creativity": "Creativity",
        "cr_help": "Low = precise",
        "length": "Length",
        "short": "Short",
        "medium": "Medium",
        "long": "Long",
        "save": "Save chats",
        "clear": "Clear all",
        "cleared": "Done ✅",
        "help": "Help",
        "theme": "Theme",
        "new_chat": "New chat",
        "history": "History",
        "no_history": "No history yet",
    },
}

P = {
    "teacher": {
        "ar": {"name": "أسترو المعلم", "icon": "📚", "welcome": "أنا المعلم 📚"},
        "en": {"name": "Astro Teacher", "icon": "📚", "welcome": "I'm the Teacher 📚"},
        "grad": "linear-gradient(135deg,#60a5fa,#3b82f6)",
    },
    "doctor": {
        "ar": {"name": "أسترو الطبيب", "icon": "🩺", "welcome": "أنا الطبيب 🩺"},
        "en": {"name": "Astro Doctor", "icon": "🩺", "welcome": "I'm the Doctor 🩺"},
        "grad": "linear-gradient(135deg,#5eead4,#14b8a6)",
    },
    "friend": {
        "ar": {"name": "أسترو الصديق", "icon": "💗", "welcome": "أنا صديقك 💗"},
        "en": {"name": "Astro Friend", "icon": "💗", "welcome": "I'm your friend 💗"},
        "grad": "linear-gradient(135deg,#f9a8d4,#ec4899)",
    },
    "general": {
        "ar": {"name": "أسترو", "icon": "✨", "welcome": "أنا أسترو ✨"},
        "en": {"name": "Astro", "icon": "✨", "welcome": "I'm Astro ✨"},
        "grad": "linear-gradient(135deg,#d8b4fe,#a855f7)",
    },
}

REPLIES = {
    "teacher": {"ar": "سؤال رائع 📚", "en": "Great question 📚"},
    "doctor": {"ar": "شكراً 🩺", "en": "Thanks 🩺"},
    "friend": {"ar": "أفهمك 💗", "en": "I understand 💗"},
    "general": {"ar": "شكراً ✨", "en": "Thanks ✨"},
}

# END
