from fastapi import APIRouter
from app.schemas.unit_schema import UnitDashboardResponse
from app.services.unit_service import (
    get_unit_dashboard,
    get_all_units
)

router = APIRouter(prefix="/unit", tags=["Unit"])


@router.get("/list")
def unit_list():
    return get_all_units()


@router.get(
    "/dashboard/{unit_name}",
    response_model=UnitDashboardResponse
)
def unit_dashboard(unit_name: str):
    return get_unit_dashboard(unit_name)