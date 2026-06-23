from datetime import datetime, timezone
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
PRODUCTION_DIR = BASE_DIR / "data" / "production"
LOG_PATH = PRODUCTION_DIR / "prediction_logs.csv"


def log_prediction(
    endpoint: str,
    input_data: dict,
    probability: float,
    threshold: float,
    prediction: int,
    label: str,
    latency_ms: float,
    status_code: int = 200,
    error: str | None = None,
):
    """Sauvegarde un log de prédiction en CSV pour l'analyse de production."""

    PRODUCTION_DIR.mkdir(parents=True, exist_ok=True)

    log_row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "endpoint": endpoint,
        "probability": probability,
        "threshold": threshold,
        "prediction": prediction,
        "label": label,
        "latency_ms": latency_ms,
        "status_code": status_code,
        "error": error,
        **input_data,
    }

    log_df = pd.DataFrame([log_row])

    if LOG_PATH.exists():
        log_df.to_csv(LOG_PATH, mode="a", header=False, index=False)
    else:
        log_df.to_csv(LOG_PATH, index=False)