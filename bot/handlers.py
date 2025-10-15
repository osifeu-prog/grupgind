from celery_app import celery_app
from bot.ipfs_uploader import upload_to_ipfs
from bot.web3_client import mint_nft
import telegram
from config import BOT_TOKEN

bot = telegram.Bot(token=BOT_TOKEN)

@celery_app.task
def create_nft_task(src_path: str, chat_id: int, user_wallet: str):
    try:
        # 1. עיבוד רגיל (resize) – אפשר למחוק או להרחיב
        # 2. העלאה ל-IPFS
        token_uri = upload_to_ipfs(src_path)

        # 3. קריאה לחוזה חכם
        tx_hash = mint_nft(user_wallet, token_uri)

        # 4. משוב למשתמש
        msg = (
            f"NFT נוצר בהצלחה!\n\n"
            f"Token URI: {token_uri}\n"
            f"Transaction Hash: {tx_hash}"
        )
        bot.send_message(chat_id=chat_id, text=msg)
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"❌ שגיאה ביצירת ה־NFT: {e}")
