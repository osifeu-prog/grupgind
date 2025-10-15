from celery import Celery
from config import CELERY_BROKER_URL

celery_app = Celery("bot_tasks", broker=CELERY_BROKER_URL)
