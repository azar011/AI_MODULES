from fastapi import APIRouter
from app.schemas.department_schema import DepartmentDashboardResponse
from app.services.department_service import (
    get_department_dashboard,
    get_all_departments
)

router = APIRouter(prefix="/department", tags=["Department"])


@router.get("/list")
def department_list():
    return get_all_departments()


@router.get(
    "/dashboard/{department_name}",
    response_model=DepartmentDashboardResponse
)
def department_dashboard(department_name: str):
    return get_department_dashboard(department_name)