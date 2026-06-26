from datetime import datetime, timezone
from pathlib import Path
import os
import json

import pandas as pd
from supabase import create_client, Client


BASE_DIR = Path(__file__).resolve().parents[1]
PRODUCTION_DIR = BASE_DIR / "data" / "production"
LOG_PATH = PRODUCTION_DIR / "prediction_logs.csv"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = "prediction_logs"


def get_supabase_client() -> Client | None:
    """Retourne un client Supabase si les variables d'environnement existent."""
    if SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None


def create_log(
    endpoint: str,
    input_data: dict,
    probability: float,
    threshold: float,
    prediction: int,
    label: str,
    latency_ms: float,
    status_code: int = 200,
    error: str | None = None,
) -> dict:
    """Construit une ligne de log standardisée."""

    return {
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


def save_to_csv(log_row: dict) -> None:
    """Sauvegarde le log dans un CSV local."""

    PRODUCTION_DIR.mkdir(parents=True, exist_ok=True)

    log_df = pd.DataFrame([log_row])

    if LOG_PATH.exists():
        log_df.to_csv(LOG_PATH, mode="a", header=False, index=False)
    else:
        log_df.to_csv(LOG_PATH, index=False)


def save_to_supabase(log_row: dict) -> None:
    """Sauvegarde le log dans Supabase."""

    supabase = get_supabase_client()

    if supabase is None:
        raise RuntimeError("Supabase client is not configured.")

    db_row = {
        "timestamp": log_row.get("timestamp"),
        "endpoint": log_row.get("endpoint"),
        "probability": log_row.get("probability"),
        "threshold": log_row.get("threshold"),
        "prediction": log_row.get("prediction"),
        "label": log_row.get("label"),
        "latency_ms": log_row.get("latency_ms"),
        "status_code": log_row.get("status_code"),
        "error": log_row.get("error"),
        "Age": log_row.get("Age"),
        "Sex": log_row.get("Sex"),
        "ChestPainType": log_row.get("ChestPainType"),
        "RestingBP": log_row.get("RestingBP"),
        "Cholesterol": log_row.get("Cholesterol"),
        "FastingBS": log_row.get("FastingBS"),
        "RestingECG": log_row.get("RestingECG"),
        "MaxHR": log_row.get("MaxHR"),
        "ExerciseAngina": log_row.get("ExerciseAngina"),
        "Oldpeak": log_row.get("Oldpeak"),
        "ST_Slope": log_row.get("ST_Slope"),
        "Cholesterol_missing": log_row.get("Cholesterol_missing"),
    }

    supabase.table(TABLE_NAME).insert(db_row).execute()



def save_log(log_row: dict) -> None:
    """
    Sauvegarde le log.
    Si Supabase échoue, on bascule en CSV local pour éviter de casser l'API.
    """
    supabase = get_supabase_client()

    if supabase is not None:
        try:
            save_to_supabase(log_row)
            return
        except Exception as e:
            print(f"Erreur Supabase, fallback CSV : {e}")

    save_to_csv(log_row)    


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
) -> None:
    """Fonction principale appelée par l'API après chaque prédiction."""

    log_row = create_log(
        endpoint=endpoint,
        input_data=input_data,
        probability=probability,
        threshold=threshold,
        prediction=prediction,
        label=label,
        latency_ms=latency_ms,
        status_code=status_code,
        error=error,
    )

    save_log(log_row)


def read_logs(limit: int = 100) -> pd.DataFrame:
    """
    Lit les logs.
    - Depuis Supabase si configuré.
    - Sinon depuis le CSV local.
    """

    supabase = get_supabase_client()

    if supabase is not None:
        response = (
            supabase.table(TABLE_NAME)
            .select("*")
            .order("id", desc=True)
            .limit(limit)
            .execute()
        )
        return pd.DataFrame(response.data)

    if not LOG_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(LOG_PATH).tail(limit)


def logs_to_json(df: pd.DataFrame) -> list[dict]:
    """Convertit un DataFrame en JSON compatible FastAPI."""

    if df.empty:
        return []

    return json.loads(df.to_json(orient="records", date_format="iso"))