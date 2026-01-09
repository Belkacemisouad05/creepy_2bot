import json
import random
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator

# ========= TOKEN =========
TOKEN = os.getenv("BOT_TOKEN")

# ========= ملفات =========
MEMORY_FILE = "memory.json"

# ========= حالة البوت =========
bot_active = True

# ========= تحميل الذاكرة =========
def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

memory = load_memory()

# ========= الجمل المميزة =========
SPECIAL_RESPONSES = {
    "سينسي": "صندوق أسود يقبع في ظلامه ضوء أبيض 🖤✨",
    "نصرو": "صندوق أسود يقبع في ظلامه ضوء أبيض 🖤✨",
    "نصرالدين": "صندوق أسود يقبع في ظلامه ضوء أبيض 🖤✨",
    "بن هجيرة": "صندوق أسود يقبع في ظلامه ضوء أبيض 🖤✨",

    "طابت ليلتك": "تحياتي 🌙✨",
    "good night": "تحياتي 🌙✨",
    "سلام": "وعليكم السلام يا ملكة 👑",
    "hello": "أهلا وسهلا 👑",

    "كريبي": "هاااي أنا هما 🤍 اتفضلي اسألي كوداساي ✨",
    "creepy": "هاااي أنا هما 🤍",

    "dayskidy": "في ماذا تحتاجين المساعدة يا ملكة؟ 👑",
}

SOUAD_RESPONSES = [
    "الملكة سعاد في خدمة الشعب 👑",
    "تاج الملكة لا يُمس ♟👑",
    "سعاد… اسم يسبق الهيبة ✨",
    "الملكة سعاد فوق الجميع 👑🖤"
]

ALLOWED_NAMES = ["سعاد", "souad", "شيماء", "chaimaa"]

# ========= لغات برمجة =========
PROGRAMMING_KEYWORDS = {
    "python": "لغة Python تُستعمل في الذكاء الاصطناعي، الويب، الأتمتة.",
    "java": "Java لغة قوية للتطبيقات الكبيرة.",
    "c++": "C++ لغة سريعة وقوية.",
    "javascript": "JavaScript لبرمجة الويب.",
    "html": "HTML لبناء هيكل الصفحات.",
    "css": "CSS لتصميم الصفحات."
}

# ========= المعالج =========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_active
    text = update.message.text.strip()
    text_lower = text.lower()

    # ---- تشغيل ----
    if text_lower in ["اشتغل", "شغل", "start"]:
        bot_active = True
        await update.message.reply_text("👶🤍 رجعت نخدم يا لولو")
        return

    # ---- إيقاف ----
    if text_lower in ["اخرج", "اغلق", "stop"]:
        bot_active = False
        await update.message.reply_text("😴 خرجت نرقد… نرجع كي تقولي اشتغل")
        return

    # ---- إذا مطفأ ----
    if not bot_active:
        return

    # ---- الجمل المميزة ----
    if text_lower in SPECIAL_RESPONSES:
        await update.message.reply_text(SPECIAL_RESPONSES[text_lower])
        return

    # ---- ردود لسعاد ----
    if text_lower in ["سعاد", "souad"]:
        await update.message.reply_text(random.choice(SOUAD_RESPONSES))
        return

    # ---- أسماء أخرى ----
    if text_lower.isalpha() and text_lower not in [n.lower() for n in ALLOWED_NAMES]:
        await update.message.reply_text(
            "هذا الاسم سيختفي أمام ظل جلالة الملكة سعاد 👑🖤"
        )
        return

    # ---- حفظ جملة جديدة ----
    if text_lower.endswith("احفظ هذه"):
        sentence = text.replace("احفظ هذه", "").strip()
        if sentence:
            memory[sentence] = sentence
            save_memory(memory)
            await update.message.reply_text("🧠✨ حفظتها في الذاكرة")
        else:
            await update.message.reply_text("وش نحفظ؟ عطيني الجملة")
        return

    # ---- استرجاع من الذاكرة ----
    if text in memory:
        await update.message.reply_text(memory[text])
        return

    # ---- لغات برمجة ----
    for lang in PROGRAMMING_KEYWORDS:
        if lang in text_lower:
            await update.message.reply_text(PROGRAMMING_KEYWORDS[lang])
            return

    # ---- ترجمة ----
    if text_lower.startswith("ترجم"):
        try:
            sentence = text.replace("ترجم", "").strip()
            translated = GoogleTranslator(source="auto", target="ar").translate(sentence)
            await update.message.reply_text(translated)
        except:
            await update.message.reply_text("ما قدرتش نترجم 😔")
        return
        # ---- افتراضي ----
    await update.message.reply_text(
        "ما فهمتش مليح، قولي أكثر يا ملكة 👑✨\nإذا حابة نحفظها اكتبي:\n\n" + text + " احفظ هذه"
    )

# ========= تشغيل =========
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Creepy is running...")
    app.run_polling()

if __name__ == "__main__":
    main()