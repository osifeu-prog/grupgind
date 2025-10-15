import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEVELOPER_LINK = os.getenv("DEVELOPER_LINK")
SRC_DIR = Path(os.getenv("SRC_DIR", "/data/input"))
DST_ROOT = Path(os.getenv("DST_ROOT", "/data/output"))
TARGET_SIZES = [(320, 180), (640, 360), (960, 540)]
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env var חסר")
