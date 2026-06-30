from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import os
from supabase import create_client

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Heart Disease Monitoring",
    page_icon="❤️",
    layout="wide",
)


BASE_DIR = Path(__file__).resolve().parents[1]
LOGS_PATH = BASE_DIR / "data" / "production" / "prediction_logs.csv"
DRIFT_REPORT_PATH = BASE_DIR / "reports" / "data_drift_report.html"


st.title("❤️ Heart Disease API Monitoring Dashboard")

st.markdown(
    """
    Ce dashboard permet de suivre les prédictions générées par l'API,
    les performances opérationnelles et les premiers signaux de dérive des données.
    """
)


@st.cache_data(ttl=60)
def load_logs(path: Path) -> pd.DataFrame:
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if supabase_url and supabase_key:
        supabase = create_client(supabase_url, supabase_key)

        response = (
            supabase.table("prediction_logs")
            .select("*")
            .order("id", desc=True)
            .limit(1000)
            .execute()
        )

        return pd.DataFrame(response.data)

    return pd.read_csv(path)


if not LOGS_PATH.exists():
    st.error("Aucun fichier de logs trouvé. Lance d'abord quelques prédictions via l'API.")
    st.stop()


df = load_logs(LOGS_PATH)

st.success(f"{len(df)} prédictions chargées depuis les logs de production.")


# =========================
# Indicateurs clés
# =========================

st.header("📊 Indicateurs clés")

nb_calls = len(df)
avg_latency = df["latency_ms"].mean()
max_latency = df["latency_ms"].max()
positive_rate = df["prediction"].mean() * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Nombre d'appels", f"{nb_calls}")
col2.metric("Latence moyenne", f"{avg_latency:.2f} ms")
col3.metric("Latence max", f"{max_latency:.2f} ms")
col4.metric("Prédictions positives", f"{positive_rate:.2f}%")


# =========================
# Graphiques principaux
# =========================

st.header("📈 Analyse des prédictions")

graph_col1, graph_col2 = st.columns(2)

with graph_col1:
    st.subheader("Distribution des classes prédites")

    fig, ax = plt.subplots(figsize=(5, 3))
    df["prediction"].value_counts().sort_index().plot(kind="bar", ax=ax)

    ax.set_title("Classes prédites")
    ax.set_xlabel("Classe")
    ax.set_ylabel("Nombre d'appels")
    ax.set_xticklabels(["0", "1"], rotation=0)

    st.pyplot(fig)

with graph_col2:
    st.subheader("Distribution des probabilités")

    fig, ax = plt.subplots(figsize=(5, 3))
    df["probability"].hist(bins=20, ax=ax)

    ax.set_title("Probabilités prédites")
    ax.set_xlabel("Probabilité")
    ax.set_ylabel("Nombre d'appels")

    st.pyplot(fig)


# =========================
# Latence
# =========================

st.header("⏱️ Suivi de la latence")

fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(df["latency_ms"], marker="o", linewidth=1)

ax.set_title("Évolution de la latence des prédictions")
ax.set_xlabel("Appel API")
ax.set_ylabel("Latence (ms)")

st.pyplot(fig)

if max_latency > 500:
    st.warning(
        f"Pic de latence détecté : {max_latency:.2f} ms. "
        "La majorité des appels reste toutefois proche de la latence moyenne."
    )
else:
    st.info("Aucun pic de latence critique détecté.")


# =========================
# Analyse drift simple
# =========================

st.header("🧭 Suivi de dérive des données")

st.markdown(
    """
    Le rapport de dérive compare les données de référence utilisées lors de la modélisation
    avec les données collectées en production via l'API.
    """
)

if DRIFT_REPORT_PATH.exists():
    st.success("Rapport Evidently disponible : `reports/data_drift_report.html`")

    with open(DRIFT_REPORT_PATH, "rb") as file:
        st.download_button(
            label="📥 Télécharger le rapport Evidently HTML",
            data=file,
            file_name="data_drift_report.html",
            mime="text/html",
        )
else:
    st.warning(
        "Le rapport Evidently n'a pas encore été généré. "
        "Lance le notebook de monitoring pour créer `reports/data_drift_report.html`."
    )


# =========================
# Logs récents
# =========================

st.header("📄 Logs de production")

st.markdown("Aperçu des derniers appels enregistrés par l'API.")

st.dataframe(
    df.tail(20).sort_index(ascending=False),
    use_container_width=True,
)


# =========================
# Notes
# =========================

st.header("📝 Commentaire de monitoring")

st.markdown(
    f"""
    Sur la période observée, l'API a traité **{nb_calls} appels** avec un taux d'erreur de
    **{error_rate:.2f}%**. La latence moyenne est de **{avg_latency:.2f} ms**, ce qui indique
    un temps de réponse satisfaisant pour un prototype de déploiement.

    Le taux de prédictions positives est de **{positive_rate:.2f}%**. Cette information permet
    de suivre l'évolution des prédictions du modèle en production et d'identifier d'éventuels
    changements de comportement.
    """
)