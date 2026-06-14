#Test 1 : health 
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

#Test 2 : prediction valide 

def test_predict():
    payload = {
        "Age": 48,
        "Sex": "M",
        "ChestPainType": "ASY",
        "RestingBP": 130,
        "Cholesterol": 245,
        "FastingBS": 0,
        "RestingECG": "Normal",
        "MaxHR": 140,
        "ExerciseAngina": "Y",
        "Oldpeak": 1.2,
        "ST_Slope": "Flat",
        "Cholesterol_missing": 0
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "probability" in data
    assert "prediction" in data

#Test 3 : si données invalides 
def test_predict_invalid_age():
    payload = {
        "Age": -5,
        "Sex": "M",
        "ChestPainType": "ASY",
        "RestingBP": 130,
        "Cholesterol": 245,
        "FastingBS": 0,
        "RestingECG": "Normal",
        "MaxHR": 140,
        "ExerciseAngina": "Y",
        "Oldpeak": 1.2,
        "ST_Slope": "Flat",
        "Cholesterol_missing": 0
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422

#test avec id bon
def test_predict_by_patient_id():
    response = client.get("/predict/PAT-0001")

    assert response.status_code == 200

    data = response.json()
    assert "probability" in data
    assert "prediction" in data

#test avec mauvais id 
def test_predict_by_unknown_patient_id():
    response = client.get("/predict/PAT-9999")

    assert response.status_code == 404