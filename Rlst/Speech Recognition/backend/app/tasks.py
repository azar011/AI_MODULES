from app.celery_app import celery
from app.services.speech_service import translate_audio
import os

@celery.task
def translate_task(audio_path):

    try:
        return translate_audio(audio_path)

    except Exception as e:

        print("TASK ERROR:", repr(e))

        raise

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
