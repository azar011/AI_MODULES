from fastapi import APIRouter
from app.services.data_service import fetch_data
from app.services.forecasting_service import (
    forecast_zone,
    forecast_department,
    forecast_floor,
    forecast_building
)

router = APIRouter()


# =========================================================
# PREDICTION API
# =========================================================

@router.get("/predict")
def predict(
    level: str,
    building: str = None,
    floor: str = None,
    department: str = None,
    zone: str = None
):

    df = fetch_data()

    if df.empty:
        return {
            "status": "error",
            "message": "No data found"
        }

    # =====================================================
    # FILTERING
    # =====================================================

    if building:
        df = df[df["building"] == building]

    if floor:
        df = df[df["floor"] == floor]

    if department:
        df = df[df["department"] == department]

    if zone:
        df = df[df["zone"] == zone]

    # =====================================================
    # NO ROWS AFTER FILTER
    # =====================================================

    if df.empty:
        return {
            "status": "error",
            "message": "No matching records found"
        }

    # =====================================================
    # LEVEL FORECASTING
    # =====================================================

    if level == "zone":

        result = forecast_zone(df)

    elif level == "department":

        result = forecast_department(df)

    elif level == "floor":

        result = forecast_floor(df)

    elif level == "building":

        result = forecast_building(df)

    else:

        return {
            "status": "error",
            "message": "Invalid level"
        }

    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return {
        "status": "success",
        "level": level,
        "result": result,
        "rows_used": len(df)
    }


# =========================================================
# GET BUILDINGS
# =========================================================

@router.get("/buildings")
def get_buildings():

    df = fetch_data()

    if df.empty:
        return []

    buildings = sorted(
        df["building"]
        .dropna()
        .unique()
        .tolist()
    )

    return buildings


# =========================================================
# GET FLOORS
# =========================================================

@router.get("/floors")
def get_floors(building: str):

    df = fetch_data()

    if df.empty:
        return []

    df = df[df["building"] == building]

    floors = sorted(
        df["floor"]
        .dropna()
        .unique()
        .tolist()
    )

    return floors


# =========================================================
# GET DEPARTMENTS
# =========================================================

@router.get("/departments")
def get_departments(
    building: str,
    floor: str
):

    df = fetch_data()

    if df.empty:
        return []

    df = df[
        (df["building"] == building)
        &
        (df["floor"] == floor)
    ]

    departments = sorted(
        df["department"]
        .dropna()
        .unique()
        .tolist()
    )

    return departments


# =========================================================
# GET ZONES
# =========================================================

@router.get("/zones")
def get_zones(
    building: str,
    floor: str,
    department: str
):

    df = fetch_data()

    if df.empty:
        return []

    df = df[
        (df["building"] == building)
        &
        (df["floor"] == floor)
        &
        (df["department"] == department)
    ]

    zones = sorted(
        df["zone"]
        .dropna()
        .unique()
        .tolist()
    )

    return zones