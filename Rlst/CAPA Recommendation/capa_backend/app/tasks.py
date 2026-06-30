from app.cerely_app import celery
from app.services.capa_service import process_escalation


@celery.task
def process_capa(data):

    result = process_escalation(data)

    return result