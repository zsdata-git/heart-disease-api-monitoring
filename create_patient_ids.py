import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/reference/heart_cleaning.csv")
OUTPUT_PATH = Path("data/reference/patients_reference.csv")

df = pd.read_csv(INPUT_PATH)

df.insert(0, "patient_id", [f"PAT-{i:04d}" for i in range(1, len(df) + 1)])

df.to_csv(OUTPUT_PATH, index=False)

print(f"Fichier créé : {OUTPUT_PATH}")
print(df.head())