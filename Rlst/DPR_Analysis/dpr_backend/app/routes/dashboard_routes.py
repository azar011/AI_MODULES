from fastapi import APIRouter
from app.services.dashboard_service import get_main_dashboard

router = APIRouter(prefix="/dashboard", tags=["Main Dashboard"])


@router.get("/main")
def main_dashboard():
    return get_main_dashboard()