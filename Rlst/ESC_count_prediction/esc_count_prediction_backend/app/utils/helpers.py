import pandas as pd

def add_features(df):

    df = df.sort_values("date")

    df["lag_1"] = df["count"].shift(1)
    df["lag_7"] = df["count"].shift(7)

    df["roll_7"] = df["count"].rolling(7, min_periods=1).mean()
    df["roll_30"] = df["count"].rolling(30, min_periods=1).mean()

    df["dow"] = df["date"].dt.dayofweek

    return df