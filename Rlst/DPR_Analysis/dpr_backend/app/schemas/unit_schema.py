from pydantic import BaseModel
from typing import List, Dict, Any


class UnitDashboardResponse(BaseModel):
    unit_name: str
    kpis: Dict[str, Any]
    daily_comparison: Dict[str, Any]
    trend_7_days: List[Dict[str, Any]]
    trend_30_days: List[Dict[str, Any]]
    submission_vs_target: List[Dict[str, Any]]
    daily_lapsed: List[Dict[str, Any]]
    best_days: List[Dict[str, Any]]
    worst_days: List[Dict[str, Any]]