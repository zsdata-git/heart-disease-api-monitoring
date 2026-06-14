from typing import Literal

from pydantic import BaseModel, Field


class PatientData(BaseModel):
    Age: int = Field(..., ge=0, le=120)
    Sex: Literal["M", "F"]
    ChestPainType: Literal["ATA", "NAP", "ASY", "TA"]
    RestingBP: float = Field(..., gt=0)
    Cholesterol: float = Field(..., ge=0)
    FastingBS: Literal[0, 1]
    RestingECG: Literal["Normal", "ST", "LVH"]
    MaxHR: float = Field(..., gt=0)
    ExerciseAngina: Literal["Y", "N"]
    Oldpeak: float
    ST_Slope: Literal["Up", "Flat", "Down"]
    Cholesterol_missing: Literal[0, 1]


class PredictionResponse(BaseModel):
    probability: float
    threshold: float
    prediction: int
    label: str