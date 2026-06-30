# app/services/forecasting_service.py

import pandas as pd
import numpy as np


# =========================================================
# FEATURE ENGINEERING
# =========================================================

def create_features(df):

    df = df.sort_values("date").copy()

    # Previous day escalation (no NaN)
    df["Prev_Day_Esc"] = df["count"].shift(1).fillna(df["count"])

    # Rolling averages (no NaN anymore)
    df["Rolling_3_Day_Avg"] = df["count"].rolling(3, min_periods=1).mean()
    df["Rolling_7_Day_Avg"] = df["count"].rolling(7, min_periods=1).mean()
    df["Rolling_30_Day_Avg"] = df["count"].rolling(30, min_periods=1).mean()

    # Difference
    df["Esc_Diff"] = df["count"] - df["Prev_Day_Esc"]

    # Trend
    df["Esc_Trend"] = np.where(
        df["Esc_Diff"] > 0,
        "Increasing",
        np.where(df["Esc_Diff"] < 0, "Decreasing", "Stable")
    )

    # (optional safety, but now rarely needed)
    df = df.fillna(0)

    return df

# =========================================================
# RANGE GENERATION
# =========================================================
def generate_prediction_range(prediction, volatility=None):

    low = max(0, round(prediction - 2))
    high = round(prediction + 2)

    return f"{low} - {high}"

# =========================================================
# ZONE FORECAST
# =========================================================

def forecast_zone(df):

    if df.empty:
        return {
            "level": "zone",
            "prediction_range": "0 - 0"
        }

    df = create_features(df)

    latest = df.iloc[-1]

    # --------------------------
    # FEATURE-ENGINEERED SCORE
    # --------------------------

    prediction = (
        (latest["Prev_Day_Esc"] * 0.30) +
        (latest["Rolling_3_Day_Avg"] * 0.25) +
        (latest["Rolling_7_Day_Avg"] * 0.25) +
        (latest["Rolling_30_Day_Avg"] * 0.20)
    )

    # Handle NaN
    if np.isnan(prediction):
        prediction = latest["count"]

    # Volatility
    volatility = (
        df["count"]
        .tail(7)
        .std()
    )

    if np.isnan(volatility):
        volatility = 1

    prediction_range = generate_prediction_range(
        prediction,
        volatility
    )

    return {
        "level": "zone",
        "building": latest["building"],
        "floor": latest["floor"],
        "department": latest["department"],
        "zone": latest["zone"],
        "prediction_range": prediction_range

        if not np.isnan(latest["Prev_Day_Esc"])
        else 0,
        # "rolling_3_day_avg": round(
        #     latest["Rolling_3_Day_Avg"], 2
        # ),
        # "rolling_7_day_avg": round(
        #     latest["Rolling_7_Day_Avg"], 2
        # ),
        # "rolling_30_day_avg": round(
        #     latest["Rolling_30_Day_Avg"], 2
        # )
    }


# =========================================================
# DEPARTMENT FORECAST
# =========================================================
def forecast_department(df):

    if df.empty:
        return {
            "level": "department",
            "prediction_range": "0 - 0"
        }

    zone_results = {}
    zone_mid_sum = 0

    for zone in df["zone"].unique():

        zone_df = df[df["zone"] == zone]
        result = forecast_zone(zone_df)

        zone_results[zone] = result

        low, high = map(int, result["prediction_range"].split(" - "))

        # take midpoint instead of summing range ends
        zone_mid_sum += (low + high) / 2

    dept_prediction = zone_mid_sum
    low = max(0, round(dept_prediction - 2))
    high = round(dept_prediction + 2)

    return {
        "level": "department",
        "building": df["building"].iloc[0],
        "floor": df["floor"].iloc[0],
        "department": df["department"].iloc[0],
        "prediction_range": f"{low} - {high}"
    }

# =========================================================
# FLOOR FORECAST
# =========================================================

def forecast_floor(df):

    if df.empty:
        return {
            "level": "floor",
            "prediction_range": "0 - 0"
        }

    department_results = {}
    floor_mid_sum = 0

    for dept in df["department"].unique():

        dept_df = df[df["department"] == dept]
        result = forecast_department(dept_df)

        department_results[dept] = result

        low, high = map(int, result["prediction_range"].split(" - "))

        # use midpoint instead of summing extremes
        floor_mid_sum += (low + high) / 2

    floor_prediction = floor_mid_sum
    low = max(0, round(floor_prediction - 2))
    high = round(floor_prediction + 2)

    return {
        "level": "floor",
        "building": df["building"].iloc[0],
        "floor": df["floor"].iloc[0],
        "prediction_range": f"{low} - {high}"
    }

# =========================================================
# BUILDING FORECAST
# =========================================================

def forecast_building(df):

    if df.empty:
        return {
            "level": "building",
            "prediction_range": "0 - 0"
        }

    floor_results = {}
    building_mid_sum = 0

    for floor in df["floor"].unique():

        floor_df = df[df["floor"] == floor]
        result = forecast_floor(floor_df)

        floor_results[floor] = result

        low, high = map(int, result["prediction_range"].split(" - "))

        building_mid_sum += (low + high) / 2

    building_prediction = building_mid_sum
    low = max(0, round(building_prediction - 2))
    high = round(building_prediction + 2)

    return {
        "level": "building",
        "building": df["building"].iloc[0],
        "prediction_range": f"{low} - {high}",
        "floors": floor_results
    }