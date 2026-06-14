import pandas as pd
from fastapi import FastAPI, HTTPException
from pathlib import Path

from app.model_loader import load_model, load_threshold
from app.schemas import PatientData, PredictionResponse


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

def make_prediction(input_df: pd.DataFrame):
    probability = float(model.predict_proba(input_df)[0, 1])
    prediction = int(probability >= threshold)
    label = "Maladie cardiaque détectée" if prediction == 1 else "Pas de maladie cardiaque détectée"

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
    return make_prediction(input_df)

@app.get("/predict/{patient_id}", response_model=PredictionResponse)
def predict_by_patient_id(patient_id: str):
    patient_row = patients_df[patients_df["patient_id"] == patient_id]

    if patient_row.empty:
        raise HTTPException(status_code=404, detail="Patient ID not found")

    input_df = patient_row.drop(columns=["patient_id", "HeartDisease"], errors="ignore")

    return make_prediction(input_df)