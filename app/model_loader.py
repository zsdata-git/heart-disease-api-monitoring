"""
Fonctions utilitaires permettant de charger :

- le modèle entraîné
- le seuil de décision optimisé

Ces artefacts proviennent du projet de modélisation.
"""

import json
from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "models" / "best_rf_model.joblib"
THRESHOLD_PATH = BASE_DIR / "models" / "threshold.json"


def load_model():
    return joblib.load(MODEL_PATH)


def load_threshold():
    with open(THRESHOLD_PATH, "r") as f:
        return json.load(f)["threshold"]