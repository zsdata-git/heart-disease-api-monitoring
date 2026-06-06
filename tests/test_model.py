# vérification que le modèle fonctionne bien , lancement terminal : python -m tests.test_model

from app.model_loader import load_model, load_threshold

model = load_model()
threshold = load_threshold()

print(type(model))
print("Threshold:", threshold)