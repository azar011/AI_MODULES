import os

# Configurable ML Risk Thresholds (Completion rates)
RISK_THRESHOLD_HIGH = float(os.getenv("ML_RISK_THRESHOLD_HIGH", 60.0))
RISK_THRESHOLD_MEDIUM = float(os.getenv("ML_RISK_THRESHOLD_MEDIUM", 85.0))

# Pre-defined Holiday dates (YYYY-MM-DD)
HOLIDAYS = {
    "2026-01-01",  # New Year's Day
    "2026-01-26",  # Republic Day (India)
    "2026-08-15",  # Independence Day (India)
    "2026-10-02",  # Gandhi Jayanti
    "2026-12-25",  # Christmas
}
