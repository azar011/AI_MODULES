from fastapi import APIRouter
from app.schemas.checklist_schema import ChecklistDashboardResponse
from app.services.checklist_service import (
    get_checklist_dashboard,
    get_all_checklists
)

router = APIRouter(prefix="/checklist", tags=["Checklist"])


@router.get("/list")
def checklist_list():
    return get_all_checklists()


@router.get(
    "/dashboard/{checklist_name}",
    response_model=ChecklistDashboardResponse
)
def checklist_dashboard(
    checklist_name: str,

):
    return get_checklist_dashboard(checklist_name)