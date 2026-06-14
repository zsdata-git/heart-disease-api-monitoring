from pydantic import BaseModel, Field


class PatientData(BaseModel):
    Age: int = Field(..., ge=0, le=120)
    Sex: str
    ChestPainType: str
    RestingBP: float = Field(..., gt=0)
    Cholesterol: float = Field(..., ge=0)
    FastingBS: int = Field(..., ge=0, le=1)
    RestingECG: str
    MaxHR: float = Field(..., gt=0)
    ExerciseAngina: str
    Oldpeak: float
    ST_Slope: str
    Cholesterol_missing: int = Field(..., ge=0, le=1)


class PredictionResponse(BaseModel):
    probability: float
    threshold: float
    prediction: int
    label: str