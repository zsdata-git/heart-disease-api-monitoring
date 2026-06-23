import pandas as pd
from fastapi import FastAPI, HTTPException
from pathlib import Path

from app.model_loader import load_model, load_threshold
from app.schemas import PatientData, PredictionResponse

import time
from app.monitoring import log_prediction

from app.monitoring import LOG_PATH
import json

app = FastAPI(
    title="Heart Disease Prediction API",
    description="API de prédiction du risque de maladie cardiaque",
    version="1.0.0",
)

model = load_model()
threshold = load_threshold()

BASE_DIR = Path(__file__).resolve().parents[1]
REFERENCE_DATA_PATH = BASE_DIR / "data" / "reference" / "patients_reference.csv"
patients_df = pd.read_csv(REFERENCE_DATA_PATH)

def make_prediction(input_df: pd.DataFrame, endpoint: str):
    start_time = time.perf_counter()

    probability = float(model.predict_proba(input_df)[0, 1])
    prediction = int(probability >= threshold)
    label = "Maladie cardiaque détectée" if prediction == 1 else "Pas de maladie cardiaque détectée"

    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

    log_prediction(
        endpoint=endpoint,
        input_data=input_df.iloc[0].to_dict(),
        probability=probability,
        threshold=threshold,
        prediction=prediction,
        label=label,
        latency_ms=latency_ms,
        status_code=200,
    )

    return PredictionResponse(
        probability=probability,
        threshold=threshold,
        prediction=prediction,
        label=label,
    )

@app.get("/")
def root():
    return {"message": "Heart Disease Prediction API is running."}


@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientData):
    input_df = pd.DataFrame([patient.model_dump()])
    return make_prediction(input_df, endpoint="/predict")

@app.get("/predict/{patient_id}", response_model=PredictionResponse)
def predict_by_patient_id(patient_id: str):
    patient_row = patients_df[patients_df["patient_id"] == patient_id]

    if patient_row.empty:
        raise HTTPException(status_code=404, detail="Patient ID not found")

    input_df = patient_row.drop(columns=["patient_id", "HeartDisease"], errors="ignore")

    return make_prediction(input_df, endpoint="/predict/{patient_id}")

@app.get("/monitoring/logs")
def get_prediction_logs(limit: int = 100):
    if not LOG_PATH.exists():
        return {"count": 0, "logs": [], "message": "No production logs found yet."}

    logs_df = pd.read_csv(LOG_PATH).tail(limit)

    logs_json = json.loads(
        logs_df.to_json(orient="records", date_format="iso")
    )

    return {
        "count": len(logs_json),
        "logs": logs_json,
    }