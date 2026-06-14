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
│   ├── reference/
│   └── production/
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

## État actuel

✔ Structure du projet créée

✔ Dépôt Git initialisé

✔ Artefacts récupérés

✔ Chargement du modèle validé

✔ Environnement reproductible avec UV

✔ Base prête pour l'implémentation de l'API FastAPI

---

## Prochaines étapes

- Développement de l'API REST
- Conteneurisation Docker
- Mise en place du monitoring
- Détection du Data Drift
- Automatisation CI/CD