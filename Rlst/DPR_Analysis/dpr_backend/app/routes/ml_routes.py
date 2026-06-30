from fastapi import APIRouter, HTTPException
from app.services.ml_service import predict_trend

router = APIRouter(prefix="/predict", tags=["ML Predictions"])

@router.get("/{entity_type}/{entity_name}")
def get_prediction(entity_type: str, entity_name: str, days: int = 7):
    if entity_type not in ["unit", "department", "checklist"]:
        raise HTTPException(status_code=400, detail="Invalid entity type. Must be unit, department, or checklist")
    
    result = predict_trend(entity_type, entity_name, days)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return result
