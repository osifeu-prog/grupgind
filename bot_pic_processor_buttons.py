import os
from dotenv import load_dotenv
import logging
from pathlib import Path
from PIL import Image
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# טען משתני סביבה (lokal .env או PaaS)
load_dotenv()
BOT_TOKEN      = os.getenv("BOT_TOKEN")
DEVELOPER_LINK = os.getenv("DEVELOPER_LINK", "https://t.me/YourDeveloperUsername")

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN env var חסר")

# נתיבי עבודה וגדלים
SRC_DIR  = Path(r"C:\Users\Giga Store\Desktop\תמונות\S1\BOTPIC")
DST_ROOT = Path(r"C:\Users\Giga Store\Desktop\תמונות\S1\processed")
TARGET_SIZES = [(320,180), (640,360), (960,540)]

# וידוא תיקיות
SRC_DIR.mkdir(parents=True, exist_ok=True)
for w,h in TARGET_SIZES:
    (DST_ROOT / f"{w}x{h}").mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# תפריט קבוע
KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔑 מזהה צ'אט",     callback_data="get_id")],
    [InlineKeyboardButton("👤 מזהה המשתמש",    callback_data="get_user_id")],
    [InlineKeyboardButton("📸 עיבוד תמונה",    callback_data="process_help")],
    [InlineKeyboardButton("📩 צור קשר עם המפתח", url=DEVELOPER_LINK)],
])

# /start – ברכה ותפריט
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    WELCOME_TEXT = """\
שלום לכולם! אני BotPicProcessor 🤖

בזכותי תוכלו:
• 🔑 לקבל את מזהה הקבוצה  
• 👤 לראות את מזהה המשתמש שלכם  
• 📸 לעבד תמונות ל־3 גדלים אוטומטית

בחרו פעולה בתפריט למטה ⬇️
"""
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=KEYBOARD,
        parse_mode="Markdown"
    )

# ברכת כניסה לחברי קבוצה חדשים
async def on_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        text = (
            f"ברוך הבא {member.full_name}!\n\n"
            f"🔑 Chat ID של הקבוצה: `{update.effective_chat.id}`\n"
            f"👤 User ID שלך: `{member.id}`\n\n"
            "לחץ על אחד הכפתורים למטה ⬇️"
        )
        await update.message.reply_text(text, reply_markup=KEYBOARD, parse_mode="Markdown")

# טיפול בלחיצות כפתורים
async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "get_id":
        await query.message.reply_text(f"🔑 Chat ID: `{query.message.chat.id}`", parse_mode="Markdown")

    elif data == "get_user_id":
        await query.message.reply_text(f"👤 User ID: `{query.from_user.id}`", parse_mode="Markdown")

    elif data == "process_help":
        help_text = (
            "כדי לעבד תמונה:\n"
            "1. שלחו תמונה (כ־photo או כקובץ).\n"
            "2. אחזור עם 3 גרסאות: 320×180, 640×360, 960×540."
        )
        await query.message.reply_text(help_text)

# עיבוד תמונה והחזרת רשימת הפלט
def process_image(path: Path):
    img = Image.open(path)
    base = path.stem
    outputs = []
    for w,h in TARGET_SIZES:
        out_dir = DST_ROOT / f"{w}x{h}"
        out_path = out_dir / f"{base}_{w}x{h}{path.suffix}"
        img.resize((w,h), Image.LANCZOS).save(out_path)
        outputs.append((out_path, (w,h)))
        logger.info(f"Saved: {out_path}")
    path.unlink()
    return outputs

# טיפול בהעלאת תמונה
async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # הורדת הקובץ
    file = await update.message.photo[-1].get_file()
    fname = file.file_unique_id + ".jpg"
    dest = SRC_DIR / fname
    await file.download_to_drive(str(dest))
    await update.message.reply_text(f"✅ הורדתי: {fname}\n⏳ מתחיל לעבד…")

    # עיבוד ושליחה חזרה
    try:
        results = process_image(dest)
        for img_path, (w,h) in results:
            with open(img_path, "rb") as f:
                await update.message.reply_photo(
                    photo=f,
                    caption=f"📷 {w}×{h}"
                )
        await update.message.reply_text("🎉 סיימתי לעבד את כל הגדלים!")
    except Exception as e:
        logger.exception(e)
        await update.message.reply_text(f"❌ קרתה שגיאה: {e}")

# main – הפעלת הבוט
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_new_member))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.PHOTO, on_photo))
    logger.info("BotPicProcessor is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
