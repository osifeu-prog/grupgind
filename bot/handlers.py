from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from config import DEVELOPER_LINK
from tasks.tasks import process_image_task

# תפריט קבוע
KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔑 מזהה צ'אט", callback_data="get_id")],
    [InlineKeyboardButton("👤 מזהה המשתמש", callback_data="get_user_id")],
    [InlineKeyboardButton("📸 עיבוד תמונה", callback_data="process_help")],
    [InlineKeyboardButton("📩 צור קשר עם המפתח", url=DEVELOPER_LINK)],
])

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "שלום! אני BotPicProcessor 🤖\n\n"
        "• 🔑 קבלת מזהה הקבוצה\n"
        "• 👤 קבלת מזהה המשתמש\n"
        "• 📸 עיבוד תמונות\n\n"
        "בחרו באפשרות מתחת ⬇️"
    )
    await update.message.reply_text(text, reply_markup=KEYBOARD)

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "get_id":
        await query.message.reply_text(f"🔑 Chat ID: `{query.message.chat.id}`", parse_mode="Markdown")
    elif data == "get_user_id":
        await query.message.reply_text(f"👤 User ID: `{query.from_user.id}`", parse_mode="Markdown")
    else:  # process_help
        help_text = (
            "לשליחת תמונה:\n"
            "1. שלחו תמונה בפורמט Photo או File.\n"
            "2. תתקבלנה 3 גרסאות אוטומטיות."
        )
        await query.message.reply_text(help_text)

async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    dest = file.file_unique_id + ".jpg"
    await file.download_to_drive(dest)
    await update.message.reply_text("✅ מוריד ומתחיל לעבד…")

    # שליחת משימה ל־Celery
    process_image_task.delay(dest, update.effective_chat.id, update.from_user.id)

def register_handlers(app):
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.PHOTO, on_photo))
