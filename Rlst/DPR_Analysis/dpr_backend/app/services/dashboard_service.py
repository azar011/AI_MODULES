import pandas as pd
from sqlalchemy import text
from app.db.database import engine


def calculate_completion(df):

    if df.empty:
        return df

    df["lapsed"] = (
        df["targets"] -
        df["submissions"]
    )

    df["completion"] = df.apply(
        lambda row: round(
            (row["submissions"] / row["targets"]) * 100,
            2
        ) if row["targets"] > 0 else 0,
        axis=1
    )

    return df


def get_main_dashboard():

    # =========================
    # UNIT DASHBOARD
    # =========================
    unit_query = text("""
        SELECT
            unit_name,
            SUM(no_of_targets) AS targets,
            SUM(no_of_submission) AS submissions
        FROM unit_wise_report
        # WHERE report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY unit_name
    """)

    today_units_query = text("""
        SELECT
            unit_name,
            SUM(no_of_targets) AS targets,
            SUM(no_of_submission) AS submissions
        FROM unit_wise_report
        WHERE report_date = (
            SELECT MAX(report_date)
            FROM unit_wise_report
        )
        GROUP BY unit_name
    """)

    # =========================
    # DEPARTMENT DASHBOARD
    # =========================
    dept_query = text("""
        SELECT
            department_name,
            SUM(no_of_targets) AS targets,
            SUM(no_of_submission) AS submissions
        FROM department_wise_report
        # WHERE report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY department_name
    """)
    today_departments_query = text("""
        SELECT
            department_name,
            SUM(no_of_targets) AS targets,
            SUM(no_of_submission) AS submissions
        FROM department_wise_report
        WHERE report_date = (
            SELECT MAX(report_date)
            FROM department_wise_report
        )
        GROUP BY department_name
    """)

    # =========================
    # CHECKLIST DASHBOARD
    # =========================
    checklist_query = text("""
        SELECT
            checklist_name,
            SUM(no_of_targets) AS targets,
            SUM(no_of_submission) AS submissions
        FROM checklist_wise_report
        # WHERE report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY checklist_name
    """)
    
    today_checklists_query = text("""
        SELECT
            checklist_name,
            SUM(no_of_targets) AS targets,
            SUM(no_of_submission) AS submissions
        FROM checklist_wise_report
        WHERE report_date = (
            SELECT MAX(report_date)
            FROM checklist_wise_report
        )
        GROUP BY checklist_name
    """)

    try:

        unit_df = pd.read_sql(unit_query, engine)
        dept_df = pd.read_sql(dept_query, engine)
        checklist_df = pd.read_sql(checklist_query, engine)
        today_units_df = pd.read_sql(
            today_units_query,
            engine
        )

        today_departments_df = pd.read_sql(
            today_departments_query,
            engine
        )

        today_checklists_df = pd.read_sql(
            today_checklists_query,
            engine
        )

        # Calculate actual completion %
        unit_df = calculate_completion(unit_df)
        dept_df = calculate_completion(dept_df)
        checklist_df = calculate_completion(checklist_df)

        today_units_df = calculate_completion(
            today_units_df
        )

        today_departments_df = calculate_completion(
            today_departments_df
        )

        today_checklists_df = calculate_completion(
            today_checklists_df
        )

        today_targets = int(today_units_df["targets"].sum()) if not today_units_df.empty else 0
        today_submissions = int(today_units_df["submissions"].sum()) if not today_units_df.empty else 0
        today_lapsed = int(today_units_df["lapsed"].sum()) if not today_units_df.empty else 0
        today_completion = round((today_submissions / today_targets) * 100, 2) if today_targets > 0 else 0.0

        with engine.connect() as conn:
            latest_date_result = conn.execute(text("SELECT MAX(report_date) FROM unit_wise_report")).scalar()
            latest_date_str = str(latest_date_result) if latest_date_result else None

        today_summary = {
            "targets": today_targets,
            "submissions": today_submissions,
            "lapsed": today_lapsed,
            "completion": today_completion,
            "latest_date": latest_date_str
        }

        return {

            "today_summary": today_summary,

            "today_units":
                today_units_df.to_dict(
                    orient="records"
                ),

            "today_departments":
                today_departments_df.to_dict(
                    orient="records"
                ),

            "today_checklists":
                today_checklists_df.to_dict(
                    orient="records"
                ),

            "units":
                unit_df.to_dict(
                    orient="records"
                ),

            "departments":
                dept_df.to_dict(
                    orient="records"
                ),

            "checklists":
                checklist_df.to_dict(
                    orient="records"
                )

        }

    except Exception as e:
        raise Exception(f"Dashboard Error: {str(e)}")