import pandas as pd
from sqlalchemy import text

from app.db.database import engine
from app.utils.calculation_utils import (
    calculate_kpis,
    get_daily_comparison
)
from app.schemas.checklist_schema import ChecklistDashboardResponse

def get_all_checklists():

    query = text("""
        SELECT DISTINCT checklist_name
        FROM checklist_wise_report
        ORDER BY checklist_name
    """)

    df = pd.read_sql(query, engine)

    return df["checklist_name"].dropna().tolist()



def get_checklist_dashboard(checklist_name: str, unit_name: str = None, department_name: str = None):

    query = """
        SELECT *
        FROM checklist_wise_report
        WHERE checklist_name = :checklist_name
    """
    
    # For live data, you can uncomment this line:
    # query += " AND report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)"

    params = {"checklist_name": checklist_name}

    if unit_name:
        query += " AND unit_name = :unit_name"
        params["unit_name"] = unit_name

    if department_name:
        query += " AND department_name = :department_name"
        params["department_name"] = department_name

    query += " ORDER BY report_date"

    df = pd.read_sql(text(query), engine, params=params)

    if df.empty:
        return {"message": "No data found"}

    df["report_date"] = pd.to_datetime(df["report_date"])

    latest_date = df["report_date"].max()

    kpis = calculate_kpis(df)

    daily_comparison = get_daily_comparison(df)

    trend_7_days = df[
        df["report_date"] >= latest_date - pd.Timedelta(days=7)
    ][["report_date", "completion_percentage"]].to_dict("records")

    trend_30_days = df[
        df["report_date"] >= latest_date - pd.Timedelta(days=30)
    ][["report_date", "completion_percentage"]].to_dict("records")

    submission_vs_target = df[
        ["report_date", "no_of_targets", "no_of_submission"]
    ].to_dict("records")

    daily_lapsed = df[
        ["report_date", "no_of_lapsed"]
    ].to_dict("records")

    best_days = df.sort_values(
        "completion_percentage",
        ascending=False
    ).head(10).to_dict("records")

    worst_days = df.sort_values(
        "completion_percentage",
        ascending=True
    ).head(10).to_dict("records")


    return {
        "checklist_name": checklist_name,
       

        "kpis": kpis,
        "daily_comparison": daily_comparison,

        "trend_7_days": trend_7_days,
        "trend_30_days": trend_30_days,

        "submission_vs_target": submission_vs_target,
        "daily_lapsed": daily_lapsed,

        "best_days": best_days,
        "worst_days": worst_days
    }