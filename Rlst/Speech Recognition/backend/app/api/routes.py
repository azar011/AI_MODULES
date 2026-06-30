from fastapi import APIRouter, HTTPException, UploadFile, File 
from app.tasks import translate_task
import uuid
import os
from celery.result import AsyncResult
from app.celery_app import celery

MAX_SIZE = 30 * 1024 * 1024  # 30MB


ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".webm"
}

router = APIRouter()

@router.post("/translate")
async def translate(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    # temp_path = f"uploads/{uuid.uuid4()}_{file.filename}"

    filename = os.path.basename(file.filename)
    temp_path = f"uploads/{uuid.uuid4()}_{filename}"



    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )
# -----------------------OLD--------------------------------        

    # content = await file.read()     
    

    # if len(content) > MAX_SIZE:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="File size exceeds 20MB"
    #     )

    # with open(temp_path, "wb") as buffer:
    #     buffer.write(content)


# --------------------------NEW----------------------------------
    size = 0

    try:
        with open(temp_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)

                if size > MAX_SIZE:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

                    raise HTTPException(
                        status_code=413,
                        detail="File size exceeds 30MB"
                    )

                buffer.write(chunk)

    except HTTPException:
        raise

    except Exception as e:

        if os.path.exists(temp_path):
            os.remove(temp_path)

        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )
# --------------------------------------------------------------------

    try:
        task = translate_task.delay(temp_path)

        return {
            "task_id": task.id
        }


    except Exception as e:

        if os.path.exists(temp_path):
            os.remove(temp_path)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    finally:
        await file.close()
    

@router.get("/status/{task_id}")
def status(task_id: str):

    result = AsyncResult(task_id, app=celery)

    if result.failed():
        return {
            "status": "failed",
            "error": str(result.result)
        }

    if result.successful():
        return {
            "status": "completed",
            "translated_text": result.result
        }

    return {
        "status": "processing"
    }
