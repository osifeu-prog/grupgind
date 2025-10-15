import logging
from telegram.ext import ApplicationBuilder
from bot.handlers import register_handlers
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(app)
    logger.info("BotPicProcessor is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
