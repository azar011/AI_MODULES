import pandas as pd
from sqlalchemy import text

from app.db.database import engine
from app.utils.calculation_utils import (
    calculate_kpis,
    get_daily_comparison
)
from app.schemas.unit_schema import UnitDashboardResponse




def get_unit_dashboard(unit_name: str):

    query = text("""
        SELECT *
        FROM unit_wise_report
        WHERE unit_name = :unit_name
        ORDER BY report_date
    """)

    # query = text("""
    #     SELECT *
    #     FROM unit_wise_report
    #     WHERE unit_name = :unit_name
    #     AND report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)           # ffor live data
    #     ORDER BY report_date
    # """)


    df = pd.read_sql(query, engine, params={"unit_name": unit_name})

    if df.empty:
        return {
            "message": "No data found"
        }

    df["report_date"] = pd.to_datetime(df["report_date"])

    latest_date = df["report_date"].max()

    # KPIs
    kpis = calculate_kpis(df)

    # Daily comparison
    daily_comparison = get_daily_comparison(df)

    # 7 days trend
    trend_7_days = df[
        df["report_date"] >= latest_date - pd.Timedelta(days=7)
    ][["report_date", "completion_percentage"]].to_dict("records")

    # 30 days trend
    trend_30_days = df[
        df["report_date"] >= latest_date - pd.Timedelta(days=30)
    ][["report_date", "completion_percentage"]].to_dict("records")

    # submission vs target
    submission_vs_target = df[
        ["report_date", "no_of_targets", "no_of_submission"]
    ].to_dict("records")

    # lapsed
    daily_lapsed = df[
        ["report_date", "no_of_lapsed"]
    ].to_dict("records")

    # best days
    best_days = df.sort_values(
        "completion_percentage",
        ascending=False
    ).head(10).to_dict("records")

    # worst days
    worst_days = df.sort_values(
        "completion_percentage",
        ascending=True
    ).head(10).to_dict("records")

    return {
        "unit_name": unit_name,
        "kpis": kpis,
        "daily_comparison": daily_comparison,
        "trend_7_days": trend_7_days,
        "trend_30_days": trend_30_days,
        "submission_vs_target": submission_vs_target,
        "daily_lapsed": daily_lapsed,
        "best_days": best_days,
        "worst_days": worst_days
    }


def get_all_units():

    query = text("""
        SELECT DISTINCT unit_name
        FROM unit_wise_report
        ORDER BY unit_name
    """)

    df = pd.read_sql(query, engine)

    return df["unit_name"].dropna().tolist()