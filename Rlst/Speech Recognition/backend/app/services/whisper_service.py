from faster_whisper import WhisperModel
from dotenv import load_dotenv
import torch
import re
import os

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")          #  small , medium , large-v3 

if not MODEL_NAME:
    raise ValueError("MODEL_NAME environment variable is missing")


print("Loading Whisper model...")

device = "cuda" if torch.cuda.is_available() else "cpu"

compute_type = "float16" if device == "cuda" else "int8"

model = WhisperModel(
    MODEL_NAME,
    device=device,
    compute_type=compute_type,
)

print("Whisper model loaded successfully!")
print(f"Loaded Whisper Model: {MODEL_NAME}")


def translate_audio(audio_path: str):

    segments, info = model.transcribe(
        audio_path,
        # language="ta",
        task="translate",
        beam_size=1,
        vad_filter=True
    )

    text = " ".join(segment.text for segment in segments)
    
    blocked_phrases = [
        "thank you for watching",
        "thank you for watching the video",
        "please subscribe to the channel",
        "thanks for watching",
        "see you in the next video"
    ]


    for phrase in blocked_phrases:
        text = re.sub(
            re.escape(phrase),
            "",
            text,
            flags=re.IGNORECASE
        )

    return text






