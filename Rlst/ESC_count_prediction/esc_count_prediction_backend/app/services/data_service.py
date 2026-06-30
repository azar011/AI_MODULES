import pandas as pd
from app.db.mysql import engine

def fetch_data():
    query = "SELECT * FROM escalations_ml"
    df = pd.read_sql(query, engine)

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"])

    return df