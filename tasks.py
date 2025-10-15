from celery_app import celery_app
from bot.image_processor import process_image_file
import telegram
from config import BOT_TOKEN

bot = telegram.Bot(token=BOT_TOKEN)

@celery_app.task
def process_image_task(src_path: str, chat_id: int, user_id: int):
    try:
        results = process_image_file(src_path)
        for path, (w, h) in results:
            with open(path, "rb") as img:
                bot.send_photo(chat_id=chat_id, photo=img, caption=f"📷 {w}×{h}")
        bot.send_message(chat_id=chat_id, text="🎉 סיימתי לעבד את כל הגדלים!")
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"❌ קרתה שגיאה: {e}")
