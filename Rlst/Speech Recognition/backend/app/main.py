from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

from dotenv import load_dotenv
import os

load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "")

allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Whisper Translation API Running"
    }

    
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
