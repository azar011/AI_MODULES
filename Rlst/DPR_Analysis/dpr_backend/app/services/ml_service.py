import pandas as pd
import numpy as np
from datetime import timedelta
from sqlalchemy import text
from app.db.database import engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from app.config import RISK_THRESHOLD_HIGH, RISK_THRESHOLD_MEDIUM, HOLIDAYS

def predict_trend(entity_type: str, entity_name: str, days_to_predict: int = 7):
    # Determine table based on entity type
    if entity_type == "unit":
        query = text("""
            SELECT report_date, no_of_targets, no_of_submission, no_of_lapsed, completion_percentage 
            FROM unit_wise_report 
            WHERE unit_name = :entity_name 
            ORDER BY report_date
        """)
    elif entity_type == "department":
        query = text("""
            SELECT report_date, no_of_targets, no_of_submission, no_of_lapsed, completion_percentage 
            FROM department_wise_report 
            WHERE department_name = :entity_name 
            ORDER BY report_date
        """)
    elif entity_type == "checklist":
        query = text("""
            SELECT report_date, no_of_targets, no_of_submission, no_of_lapsed, completion_percentage 
            FROM checklist_wise_report 
            WHERE checklist_name = :entity_name 
            ORDER BY report_date
        """)
    else:
        return {"error": f"Invalid entity type: {entity_type}"}

    # Fetch data (limiting to last 180 days for scalability)
    df = pd.read_sql(query, engine, params={"entity_name": entity_name})
    
    if df.empty:
        return {"error": f"No historical data found for {entity_type}: {entity_name}"}

    # Preprocess date and columns
    df["report_date"] = pd.to_datetime(df["report_date"])
    df = df.sort_values("report_date").reset_index(drop=True)
    
    # Fill missing values
    df["no_of_targets"] = df["no_of_targets"].fillna(0).astype(int)
    df["no_of_submission"] = df["no_of_submission"].fillna(0).astype(int)
    df["no_of_lapsed"] = df["no_of_lapsed"].fillna(0).astype(int)
    df["completion_percentage"] = df["completion_percentage"].fillna(0.0)

    # Limit to last 180 records to prevent loading too much data
    df = df.tail(180).reset_index(drop=True)
    latest_date = df["report_date"].max()

    # Feature Engineering Helper
    def extract_features(data):
        feats = pd.DataFrame(index=data.index)
        feats["day_of_week"] = data["report_date"].dt.dayofweek
        feats["day_of_month"] = data["report_date"].dt.day
        feats["is_weekend"] = data["report_date"].dt.dayofweek.isin([5, 6]).astype(int)
        feats["is_month_end"] = data["report_date"].dt.is_month_end.astype(int)
        feats["is_holiday"] = data["report_date"].dt.strftime("%Y-%m-%d").isin(HOLIDAYS).astype(int)
        
        # Historical Lags
        feats["targets_lag_1"] = data["no_of_targets"].shift(1)
        feats["submissions_lag_1"] = data["no_of_submission"].shift(1)
        feats["lapsed_lag_1"] = data["no_of_lapsed"].shift(1)
        feats["completion_lag_1"] = data["completion_percentage"].shift(1)
        
        # Rolling features (7-day window)
        feats["targets_rolling_7"] = data["no_of_targets"].shift(1).rolling(window=7, min_periods=1).mean()
        feats["submissions_rolling_7"] = data["no_of_submission"].shift(1).rolling(window=7, min_periods=1).mean()
        feats["lapsed_rolling_7"] = data["no_of_lapsed"].shift(1).rolling(window=7, min_periods=1).mean()
        feats["completion_rolling_7"] = data["completion_percentage"].shift(1).rolling(window=7, min_periods=1).mean()
        
        return feats.fillna(method="bfill").fillna(0.0)

    # 1. Fallback baseline if insufficient data (< 15 rows)
    if len(df) < 15:
        predictions = []
        overall_completion_avg = df["completion_percentage"].mean()
        
        # Calculate baseline accuracy metrics on historical data
        baseline_preds = []
        for idx, row in df.iterrows():
            dow = row["report_date"].weekday()
            pred = df[df["report_date"].dt.dayofweek == dow]["completion_percentage"].mean()
            if pd.isna(pred):
                pred = overall_completion_avg
            baseline_preds.append(pred)
            
        actuals = df["completion_percentage"].tolist()
        mae_val = float(mean_absolute_error(actuals, baseline_preds))
        rmse_val = float(np.sqrt(mean_squared_error(actuals, baseline_preds)))
        try:
            r2_val = r2_score(actuals, baseline_preds)
            if np.isnan(r2_val):
                r2_val = 0.0
            r2_val = float(max(-1.0, r2_val))
        except:
            r2_val = 0.0
            
        if mae_val == 0.0:
            r2_val = 1.0

        for i in range(1, days_to_predict + 1):
            future_date = latest_date + timedelta(days=i)
            # Baseline day-of-week average
            dow = future_date.weekday()
            pred_completion = df[df["report_date"].dt.dayofweek == dow]["completion_percentage"].mean()
            if pd.isna(pred_completion):
                pred_completion = overall_completion_avg
            pred_completion = float(np.clip(pred_completion, 0.0, 100.0))
            
            predictions.append({
                "report_date": future_date.strftime("%Y-%m-%d"),
                "predicted_completion_percentage": round(pred_completion, 2),
                "is_forecast": True,
                "confidence_lower": round(max(0.0, pred_completion - 15.0), 2),
                "confidence_upper": round(min(100.0, pred_completion + 15.0), 2)
            })
        
        tomorrow_pred = predictions[0]["predicted_completion_percentage"]
        risk_level = "High" if tomorrow_pred < RISK_THRESHOLD_HIGH else ("Medium" if tomorrow_pred < RISK_THRESHOLD_MEDIUM else "Low")
        
        return {
            "predictions": predictions,
            "tomorrow_prediction": tomorrow_pred,
            "risk_level": risk_level,
            "metrics": {
                "mae": round(mae_val, 2),
                "rmse": round(rmse_val, 2),
                "r2": round(r2_val, 2)
            },
            "trend": "Stable",
            "is_anomaly": False,
            "confidence_score": 50.0,
            "model_type": "baseline_day_of_week"
        }

    # 2. Main ML Pipeline
    X_all = extract_features(df)
    
    # Train-test split (Chronological 80/20)
    split_idx = int(len(df) * 0.8)
    
    # Target variables (forecasting raw operational metrics directly to prevent recursive drift)
    # We build direct forecasting models for each step ahead (1 to 7)
    predictions = []
    tomorrow_targets_pred = 0
    tomorrow_submissions_pred = 0
    tomorrow_lapsed_pred = 0
    
    # We will track metrics for the step 1 forecast (tomorrow)
    tomorrow_metrics = {"mae": 0.0, "rmse": 0.0, "r2": 0.0}
    tomorrow_std = 5.0
    
    for step in range(1, days_to_predict + 1):
        # The target for step h is the value h-days ahead
        y_targets = df["no_of_targets"].shift(-step)
        y_submissions = df["no_of_submission"].shift(-step)
        y_lapsed = df["no_of_lapsed"].shift(-step)
        
        # Valid indexes for training (where target is not NaN)
        valid_idx = y_targets.dropna().index
        
        X_step = X_all.loc[valid_idx]
        y_t = y_targets.loc[valid_idx]
        y_s = y_submissions.loc[valid_idx]
        y_l = y_lapsed.loc[valid_idx]
        
        # Chronological split for evaluation
        X_train, X_test = X_step.iloc[:split_idx], X_step.iloc[split_idx:]
        yt_train, yt_test = y_t.iloc[:split_idx], y_t.iloc[split_idx:]
        ys_train, ys_test = y_s.iloc[:split_idx], y_s.iloc[split_idx:]
        yl_train, yl_test = y_l.iloc[:split_idx], y_l.iloc[split_idx:]
        
        # If test set is empty due to lack of samples, fall back to fitting on all
        if len(X_test) == 0:
            X_train, yt_train, ys_train, yl_train = X_step, y_t, y_s, y_l
            
        # Initialize and fit models for raw targets, submissions, lapses
        model_t = RandomForestRegressor(n_estimators=30, max_depth=4, random_state=42)
        model_s = RandomForestRegressor(n_estimators=30, max_depth=4, random_state=42)
        model_l = RandomForestRegressor(n_estimators=30, max_depth=4, random_state=42)
        
        model_t.fit(X_train, yt_train)
        model_s.fit(X_train, ys_train)
        model_l.fit(X_train, yl_train)
        
        # Calculate evaluation metrics for tomorrow (step 1)
        if step == 1 and len(X_test) > 0:
            s_preds = model_s.predict(X_test)
            t_preds = model_t.predict(X_test)
            
            # Avoid divide by zero
            t_preds_adj = np.where(t_preds == 0, 1, t_preds)
            pred_completion_test = (s_preds / t_preds_adj) * 100
            pred_completion_test = np.clip(pred_completion_test, 0.0, 100.0)
            
            # Actual completion rate on test set
            t_actual_adj = np.where(yt_test == 0, 1, yt_test)
            actual_completion_test = (ys_test / t_actual_adj) * 100
            actual_completion_test = np.clip(actual_completion_test, 0.0, 100.0)
            
            tomorrow_metrics["mae"] = float(mean_absolute_error(actual_completion_test, pred_completion_test))
            tomorrow_metrics["rmse"] = float(np.sqrt(mean_squared_error(actual_completion_test, pred_completion_test)))
            # R2 score (R2 can be highly sensitive, so clip lower bound at -1.0)
            try:
                r2 = r2_score(actual_completion_test, pred_completion_test)
                tomorrow_metrics["r2"] = float(max(-1.0, r2))
            except:
                tomorrow_metrics["r2"] = 0.0
                
        # Predict future date
        future_date = latest_date + timedelta(days=step)
        
        # Features at the latest available day (time t)
        X_latest = X_all.tail(1)
        
        pred_t = float(max(0, model_t.predict(X_latest)[0]))
        pred_s = float(max(0, model_s.predict(X_latest)[0]))
        pred_l = float(max(0, model_l.predict(X_latest)[0]))
        
        # Calculate completion rate
        if pred_t > 0:
            pred_completion = (pred_s / pred_t) * 100
        else:
            pred_completion = 0.0
        pred_completion = float(np.clip(pred_completion, 0.0, 100.0))
        
        # Prediction Confidence (variance of individual trees in the submissions forest)
        # Standard deviation of forest predictions serves as uncertainty estimate
        tree_preds = [tree.predict(X_latest)[0] for tree in model_s.estimators_]
        pred_std = float(np.std(tree_preds))
        if step == 1:
            tomorrow_targets_pred = pred_t
            tomorrow_submissions_pred = pred_s
            tomorrow_lapsed_pred = pred_l
            tomorrow_std = pred_std
            
        # Build confidence interval (capped at 0-100)
        # Using 1.96 standard deviations for a 95% confidence bounds approximation
        conf_lower = float(np.clip(pred_completion - max(5.0, 1.96 * pred_std), 0.0, 100.0))
        conf_upper = float(np.clip(pred_completion + max(5.0, 1.96 * pred_std), 0.0, 100.0))
        
        predictions.append({
            "report_date": future_date.strftime("%Y-%m-%d"),
            "predicted_completion_percentage": round(pred_completion, 2),
            "predicted_targets": int(round(pred_t)),
            "predicted_submissions": int(round(pred_s)),
            "predicted_lapsed": int(round(pred_l)),
            "confidence_lower": round(conf_lower, 2),
            "confidence_upper": round(conf_upper, 2),
            "is_forecast": True
        })

    # Tomorrow's prediction results
    tomorrow_pred = predictions[0]["predicted_completion_percentage"]
    risk_level = "High" if tomorrow_pred < RISK_THRESHOLD_HIGH else ("Medium" if tomorrow_pred < RISK_THRESHOLD_MEDIUM else "Low")
    
    # Anomaly Detection: 
    # Check if tomorrow's predicted completion rate is anomalous (defined as deviation from 30-day mean by > 2 SDs)
    historical_completion_mean = df["completion_percentage"].tail(30).mean()
    historical_completion_std = df["completion_percentage"].tail(30).std()
    # Handle division/std of zero
    if pd.isna(historical_completion_std) or historical_completion_std == 0:
        historical_completion_std = 5.0
        
    is_anomaly = bool(abs(tomorrow_pred - historical_completion_mean) > (2.0 * historical_completion_std))

    # Trend Classification (Increasing, Decreasing, Stable)
    # Fit a simple slope over the 7 days forecast
    forecast_rates = [p["predicted_completion_percentage"] for p in predictions]
    slope = np.polyfit(range(days_to_predict), forecast_rates, 1)[0]
    
    # Classification threshold of 0.5% average change per day
    if slope > 0.5:
        trend = "Increasing"
    elif slope < -0.5:
        trend = "Decreasing"
    else:
        trend = "Stable"
        
    # Overall confidence score: combines validation R2 and ensemble variance (capped at 100)
    # A standard score mapping where low variance + high R2 yields ~95%
    var_penalty = min(30, (tomorrow_std / max(1.0, tomorrow_submissions_pred)) * 50)
    r2_bonus = max(0, tomorrow_metrics["r2"] * 20)
    confidence_score = float(np.clip(85 - var_penalty + r2_bonus, 30.0, 98.0))

    return {
        "predictions": predictions,
        "tomorrow_prediction": tomorrow_pred,
        "risk_level": risk_level,
        "metrics": {
            "mae": round(tomorrow_metrics["mae"], 2),
            "rmse": round(tomorrow_metrics["rmse"], 2),
            "r2": round(tomorrow_metrics["r2"], 2)
        },
        "trend": trend,
        "is_anomaly": is_anomaly,
        "confidence_score": round(confidence_score, 1),
        "model_type": "direct_random_forest"
    }
