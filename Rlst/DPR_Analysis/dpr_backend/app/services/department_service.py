import pandas as pd
from sqlalchemy import text

from app.db.database import engine
from app.utils.calculation_utils import (
    calculate_kpis,
    get_daily_comparison
)
from app.schemas.department_schema import DepartmentDashboardResponse



def get_all_departments():

    query = text("""
        SELECT DISTINCT department_name
        FROM department_wise_report
        ORDER BY department_name
    """)

    df = pd.read_sql(query, engine)

    return df["department_name"].dropna().tolist()

def get_department_dashboard(department_name: str):

    query = text("""
        SELECT *
        FROM department_wise_report
        WHERE department_name = :department_name
        ORDER BY report_date
    """)

    #  query = text("""
    #     SELECT *
    #     FROM department_wise_report
    #     WHERE department_name = :department_name
    #     AND report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)                    # for live data
    #     ORDER BY report_date
    # """)

    

    df = pd.read_sql(query, engine, params={"department_name": department_name})

    if df.empty:
        return {
            "message": "No data found"
        }

    df["report_date"] = pd.to_datetime(df["report_date"])

    latest_date = df["report_date"].max()

    # KPI calculations
    kpis = calculate_kpis(df)

    # Today vs Yesterday comparison
    daily_comparison = get_daily_comparison(df)

    # 7-day trend
    trend_7_days = df[
        df["report_date"] >= latest_date - pd.Timedelta(days=7)
    ][["report_date", "completion_percentage"]].to_dict("records")

    # 30-day trend
    trend_30_days = df[
        df["report_date"] >= latest_date - pd.Timedelta(days=30)
    ][["report_date", "completion_percentage"]].to_dict("records")

    # Submission vs Target
    submission_vs_target = df[
        ["report_date", "no_of_targets", "no_of_submission"]
    ].to_dict("records")

    # Lapsed data
    daily_lapsed = df[
        ["report_date", "no_of_lapsed"]
    ].to_dict("records")

    # Best days (highest performance)
    best_days = df.sort_values(
        "completion_percentage",
        ascending=False
    ).head(10).to_dict("records")

    # Worst days (lowest performance)
    worst_days = df.sort_values(
        "completion_percentage",
        ascending=True
    ).head(10).to_dict("records")

    return {
        "department_name": department_name,
        "kpis": kpis,
        "daily_comparison": daily_comparison,
        "trend_7_days": trend_7_days,
        "trend_30_days": trend_30_days,
        "submission_vs_target": submission_vs_target,
        "daily_lapsed": daily_lapsed,
        "best_days": best_days,
        "worst_days": worst_days
    }