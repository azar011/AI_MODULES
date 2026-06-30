from fastapi import APIRouter
import uuid
import os
from celery.result import AsyncResult
from app.cerely_app import celery
from app.models.escalation_model import EscalationRequest
from app.services.embedding_service import create_embedding
from app.services.capa_service import process_escalation
from app.services.qdrant_service import add_case



router = APIRouter()


@router.get("/")
def home():

    return {
        "message": "CAPA AI API Running"
    }


from app.tasks import process_capa

@router.post("/generate-capa")
def generate_capa(request: EscalationRequest):

    task = process_capa.delay(request.dict())

    return {
        "task_id": task.id,
        "status": "PROCESSING"
    }

@router.get("/status/{task_id}")
def task_status(task_id: str):

    task = AsyncResult(task_id, app=celery)

    if task.state == "PENDING":

        return {
            "status": "PENDING"
        }

    elif task.state == "SUCCESS":

        return {
            "status": "SUCCESS",
            "result": task.result
        }

    elif task.state == "FAILURE":

        return {
            "status": "FAILURE",
            "error": str(task.result)
        }

    return {
        "status": task.state
    }

@router.post("/save-capa")
def save_capa(data: dict):

    is_modified = (

        data["corrective_action"].strip()
        !=
        data["original_corrective_action"].strip()

        or

        data["root_cause"].strip()
        !=
        data["original_root_cause"].strip()

        or

        data["preventive_action"].strip()
        !=
        data["original_preventive_action"].strip()
    )


    # Historical case accepted without changes
    if (
        data["source"] == "historical_case"
        and
        not is_modified
    ):

        return {
            "status": "already_exists",
            "message": "Historical case already exists. No new record created."
        }


    combined_text = f"""
    {data['department']}
    {data['checklist_name']}
    {data['question']}
    {data['remarks']}
    """

    embedding = create_embedding(
        combined_text
    )

    payload = {
        "department": data["department"],
        "checklist_name": data["checklist_name"],
        "question": data["question"],
        "remarks": data["remarks"],
        "corrective_action": data["corrective_action"],
        "root_cause": data["root_cause"],
        "preventive_action": data["preventive_action"]
    }

    add_case(
        embedding,
        payload
    )

    return {
        "status": "success",
        "message": "CAPA saved successfully"
    }

   