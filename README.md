---
title: Heart Disease API Monitoring
emoji: ❤️
colorFrom: pink
colorTo: red
sdk: docker
app_port: 8000
pinned: false
---

# Heart Disease API Monitoring

## Contexte

Ce projet constitue la continuité du projet de scoring cardiovasculaire réalisé précédemment (projet 6).

Le modèle de Machine Learning développé et évalué lors du projet de classification du risque de maladie cardiaque est réutilisé comme base de travail afin de préparer son déploiement en production et son monitoring.

L'objectif est de transformer un modèle de scoring validé en un service exploitable dans un environnement réel.

---

## Objectifs du projet

- Déployer le modèle sous forme d'API REST
- Automatiser le cycle de déploiement via CI/CD
- Mettre en place le stockage des données de production
- Surveiller les performances du modèle
- Détecter d'éventuels phénomènes de Data Drift
- Garantir la traçabilité des expérimentations et des versions

---

## Structure du projet

```text
heart-disease-api-monitoring/
|
|
├── .github/ 
│ └── workflows/ 
│ └── ci.yml
|
|
├── app/
│   ├── main.py
│   ├── model_loader.py
│   ├── monitoring.py
│   └── schemas.py
│
├── models/
│   ├── best_rf_model.joblib
│   └── threshold.json
│
├── data/ 
|    ├── production/ 
│    └── reference/ 
│        ├── heart_cleaning.csv 
│        └── patients_reference.csv
│
├── tests/
│   ├── test_model.py
│   └── test_api.py
│
├── notebooks/
│
├── reports/
│
├── Dockerfile
├── create_patient_ids.py
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Étape 0 - Initialisation du projet

Création d'un nouveau dépôt dédié au projet de déploiement afin de séparer :

- le projet de modélisation
- le projet MLOps / mise en production

Choix réalisés :

- environnement Python géré avec UV
- environnement virtuel dédié
- versionnement Git dès le démarrage
- récupération uniquement des artefacts nécessaires au déploiement

Artefacts réutilisés :

- modèle entraîné : `best_rf_model.joblib`
- seuil de décision optimal : `threshold.json`

---

## Étape 1 - Contrôle de version et dépôt Git

### Initialisation

```bash
uv init
uv venv
```

Activation de l'environnement :

```bash
.venv\Scripts\activate
```

Installation du kernel Jupyter :

```bash
uv add ipykernel

python -m ipykernel install --user \
--name heart-disease-api-monitoring \
--display-name "Python (heart-disease-api-monitoring)"
```

---

### Dépendances installées

- fastapi
- uvicorn
- pandas
- scikit-learn
- joblib
- evidently
- pytest

Installation :

```bash
uv add fastapi uvicorn pandas scikit-learn joblib evidently pytest
```

---

### Vérification des artefacts

Validation du chargement :

```bash
python -m tests.test_model
```

Résultat attendu :

```text
<class 'sklearn.pipeline.Pipeline'>
Threshold: 0.477421727458697
```

---

### Versionnement

Le projet est suivi avec Git.

Fichiers exclus via `.gitignore` :

- environnement virtuel
- caches Python
- artefacts temporaires
- fichiers système

Exemple de stratégie de commits :

```text
Initial project structure
Add trained model artifacts
Add model loading utilities
Prepare API architecture
```

Une stratégie de branches pourra être utilisée par la suite :

```text
main
feature/api
feature/monitoring
feature/docker
feature/cicd
```

---

## Étape 2 - Déploiement du modèle 

---

### Lancer l'API

```bash
uvicorn app.main:app --reload
```

Documentation Swagger :

http://127.0.0.1:8000/docs


---

### Endpoints disponibles

- Vérification de l'état de l'API
GET /health

Exemple de réponse :

{
  "status": "ok",
  "model_loaded": true
}

- Prédiction à partir de données utilisateur
POST /predict

Exemple de requête :

{
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

Exemple de réponse :

{
  "probability": 0.91,
  "threshold": 0.477,
  "prediction": 1,
  "label": "Maladie cardiaque détectée"
}

- Prédiction à partir d'un identifiant patient
GET /predict/PAT-0001

Cette route récupère les données du patient depuis le fichier de référence puis exécute automatiquement la prédiction.

---

### Docker

Construire l'image
```bash
docker build -t heart-disease-api
```

Lancer le conteneur
```bash
docker run -p 8000:8000 heart-disease-api
```
Documentation Swagger :

http://localhost:8000/docs

---

### Tests

Exécuter tous les tests :
```bash
pytest
```

Résultat attendu : 5 passed

Les tests couvrent :
- chargement du modèle
- endpoint /health
- endpoint /predict
- endpoint /predict/{patient_id}
- validation des données d'entrée

---

### Pipeline CI/CD

Une pipeline GitHub Actions est exécutée automatiquement à chaque push sur la branche principale.

Étapes exécutées :

- Exécution des tests automatisés.
- Construction de l'image Docker.
- Simulation du déploiement.

Le workflow est défini dans :

.github/workflows/ci.yml

---

### Déploiement 

- GitHub

Repository :
https://github.com/zsdata-git/heart-disease-api-monitoring

- Hugging Face Space

Application déployée :
https://hayette-heart-disease-api.hf.space

Documentation interactive :
https://hayette-heart-disease-api.hf.space/docs

---

## Technologies utilisées

- Python 3.12
- FastAPI
- Uvicorn
- Scikit-Learn
- Pandas
- Pytest
- Docker
- GitHub Actions
- Hugging Face Spaces

---

## Auteur 
Projet réalisé par Hayette dans le cadre d'un projet de déploiement et monitoring d'un modèle de Machine Learning.