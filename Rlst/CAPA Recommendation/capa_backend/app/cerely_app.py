from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable is missing")

celery = Celery(
    "capa_backend",
    broker=REDIS_URL,
    backend=REDIS_URL
)