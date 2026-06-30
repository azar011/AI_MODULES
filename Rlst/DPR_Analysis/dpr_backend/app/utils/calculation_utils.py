import pandas as pd


def calculate_kpis(df):

    df = df.fillna(0)

    total_targets = int(df["no_of_targets"].sum())
    total_submissions = int(df["no_of_submission"].sum())
    total_lapsed = int(df["no_of_lapsed"].sum())

    completion = (total_submissions / total_targets * 100) if total_targets else 0
    lapsed = (total_lapsed / total_targets * 100) if total_targets else 0

    return {
        "total_targets": total_targets,
        "total_submissions": total_submissions,
        "completion_percentage": round(completion, 2),
        "total_lapsed": total_lapsed,
        "lapsed_percentage": round(lapsed, 2)
    }



def get_daily_comparison(df):

    df = df.fillna(0)

    latest = df["report_date"].max()

    today_df = df[df["report_date"] == latest]

    today_completion = today_df["completion_percentage"].mean()

    today_target = int(today_df["no_of_targets"].sum())
    today_submission = int(today_df["no_of_submission"].sum())
    today_lapsed = int(today_df["no_of_lapsed"].sum())

    prev_date = (
        df[df["report_date"] < latest]
        ["report_date"]
        .max()
    )

    yesterday_completion = 0

    previous_target = 0
    previous_submission = 0
    previous_lapsed = 0

    if pd.notna(prev_date):

        prev_df = df[df["report_date"] == prev_date]

        yesterday_completion = (
            prev_df["completion_percentage"]
            .mean()
        )

        previous_target = int(prev_df["no_of_targets"].sum())
        previous_submission = int(prev_df["no_of_submission"].sum())
        previous_lapsed = int(prev_df["no_of_lapsed"].sum())

    avg_7 = (
        df[df["report_date"] >= latest - pd.Timedelta(days=7)]
        ["completion_percentage"]
        .mean()
    )

    avg_30 = (
        df[df["report_date"] >= latest - pd.Timedelta(days=30)]
        ["completion_percentage"]
        .mean()
    )

    return {

        # Completion %
        "today_completion": round(today_completion, 2),

        "yesterday_completion": round(yesterday_completion, 2),

        "vs_yesterday": round(
            today_completion - yesterday_completion,
            2
        ),

        "avg_7_days": round(avg_7, 2),

        "vs_7_days": round(
            today_completion - avg_7,
            2
        ),

        "avg_30_days": round(avg_30, 2),

        "vs_30_days": round(
            today_completion - avg_30,
            2
        ),

        # Latest Day Stats
        "today_stats": {
            "target": today_target,
            "submission": today_submission,
            "lapsed": today_lapsed
        },

        # Previous Day Stats
        "previous_stats": {
            "target": previous_target,
            "submission": previous_submission,
            "lapsed": previous_lapsed
        },

        # Difference
        "difference": {
            "target": today_target - previous_target,
            "submission": today_submission - previous_submission,
            "lapsed": today_lapsed - previous_lapsed
        }
    }
