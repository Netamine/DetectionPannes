import streamlit as st
import sys
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from components.imputation import correct_timestamp_intervals
from components import upload_file
from components.validation import validate_data
from components.imputation import impute_missing_values, REQUIRED_COLUMNS

import matplotlib

matplotlib.rcParams["font.family"] = "DejaVu Sans"


# Ajouter le répertoire parent au sys.path pour que Python trouve backend/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.utils.models_loader import load_models
# Définir le port pour Streamlit (Render définit $PORT dans l'environnement)
PORT = int(os.getenv("PORT", 8501))  # Par défaut, Streamlit tourne sur 8501

# Afficher l'info dans les logs
print(f"✅ Lancement de Streamlit sur le port {PORT}...")

# 🌟 Configuration de la page
st.set_page_config(page_title="Système de Prédiction des Pannes", layout="wide")
# 🌟 Ajout de styles CSS personnalisés
st.markdown(
    """
    <style>
        /* Style du corps de la page */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #F7F9FC;
        }
        
        /* Style des titres */
        .main-header {
            background-color: #1E1E2F;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            color: #F8F9FA;
            font-size: 24px;
            font-weight: bold;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Style des blocs d'informations */
        .info-box {
            background-color: #ffffff;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
        }
        
        /* Style des boutons */
        .stButton>button {
            background-color: #007BFF !important;
            color: white !important;
            font-size: 14px !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            border: none !important;
        }
        
        /* Style des sliders */
        .stSlider>div {
            background-color: #007BFF !important;
            border-radius: 10px !important;
        }
        
        /* Style du tableau des résultats */
        .stDataFrame {
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True
)


# 🎯 **En-tête Principal**
st.markdown(
    """
    <style>
        .main-header {
            background-color: #1E1E2F;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            color: #F8F9FA;
            font-size: 26px;
            font-weight: bold;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }
    </style>
    <div class="main-header">🔍 Système de Prédiction des Pannes avec Imputation</div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# 🏗️ **Disposition en 2 colonnes**
col1, col2 = st.columns(2)

with col1:
    # 📌 **Bloc : Instructions**
    st.markdown(
        """
        <div class="info-box">
            <h4>🛠️ Comment utiliser cette Interface ?</h4>
            <p>Cette interface permet de tester la <b>prédiction des pannes</b>.</p>
            <p>📩 Téléversez un fichier CSV contenant les mesures des capteurs.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    # 📄 **Bloc : Conditions du fichier CSV**
    st.markdown(
        """
        <div class="info-box" style="background-color: #E3F2FD;">
            <h4>📄 Conditions du fichier CSV</h4>
            <ul>
                <li>✅ Format : <b>CSV</b> avec au moins 30 minutes de données.</li>
                <li>✅ Intervalle fixe : <b>10 secondes</b> (300 observations).</li>
                <li>✅ Colonnes requises :</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.code(", ".join(REQUIRED_COLUMNS), language="text")

st.markdown("---")

# 📤 **Téléversement du fichier CSV**
st.markdown("### 📥 Importer un fichier CSV pour l'analyse")
uploaded_file = upload_file()

if uploaded_file is not None:
    try:
        with st.spinner("📂 Chargement du fichier..."):
            df = pd.read_csv(uploaded_file, sep=',')
            st.markdown("#### 📊 **Aperçu du dataset avant validation**")
            st.write(f"📌 **Nombre de lignes :** {df.shape[0]} | **Nombre de colonnes :** {df.shape[1]}")
            st.dataframe(df.head())
    except Exception:
        st.error("❌ Erreur : Impossible de lire le fichier CSV.")
        st.stop()

    # 📌 **Validation du dataset**
    with st.spinner("🔍 Validation des données..."):
        validation_result, df = validate_data(df)
        if not validation_result:
            st.stop()

    # ✅ **Imputation des données**
    with st.spinner("⚙️ Imputation des valeurs manquantes..."):
        df_imputed = impute_missing_values(df, load_models("data/models"))

    # ✅ **Correction des timestamps**
    with st.spinner("⏳ Correction des timestamps..."):
        df_corrected = correct_timestamp_intervals(df_imputed)

    # ✅ **Affichage du dataset après validation et correction**
    df_filtered = df_corrected[REQUIRED_COLUMNS]
    st.markdown("### 📊 **Aperçu du dataset après validation et imputation**")
    st.write(f"📌 **Nombre de lignes :** {df_filtered.shape[0]} | **Nombre de colonnes :** {df_filtered.shape[1]}")

# Ajout d'un conteneur avec scroll
    with st.container():
        st.markdown(
            """
            <style>
            .dataframe-container {
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 10px;
                background-color: #f9f9f9;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(df_filtered.head(10))
        st.markdown('</div>', unsafe_allow_html=True)


    # ================================================================
    #  📌 PRÉDICTION DES PANNES APRÈS VALIDATION
    # ================================================================

    # Charger les modèles UNE SEULE FOIS
    if "models" not in st.session_state:
        st.session_state.models = load_models("data/models")

    models = st.session_state.models
    sae = models["sae"]
    scaler = models["scaler"]
    threshold = models["threshold"]

    # Appliquer la normalisation
    features_scaler = scaler.feature_names_in_
    df_filtered[features_scaler] = scaler.transform(df_filtered[features_scaler])

    # Prédiction avec SAE
    with st.spinner("🤖 Exécution du modèle de prédiction..."):
        reconstructed_values = sae.predict(df_filtered[features_scaler])

    # Calcul de l'erreur de reconstruction
    df_filtered["error"] = np.mean(np.square(df_filtered[features_scaler] - reconstructed_values), axis=1)

    # Détection des anomalies
    df_filtered["anomaly"] = df_filtered["error"] > threshold
    total_anomalies_detectées = df_filtered["anomaly"].sum()
    seuil_anomalies = 10
    panne_imminente = total_anomalies_detectées >= seuil_anomalies

    # ✅ **Affichage des résultats**
    st.markdown("### 🔍 Résultat de la Prédiction des Pannes")
    with st.container():
        st.markdown(
            """
            <style>
            .results-container {
                max-height: 200px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 15px;
                border-radius: 10px;
                background-color: #eaf2ff;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
    f"""
    <style>
    .results-table {{
        margin: auto;
        border-collapse: collapse;
        width: 50%;
        text-align: center;
        font-size: 18px;
    }}

    .results-table th, .results-table td {{
        border: 1px solid #ddd;
        padding: 10px;
    }}

    .results-table th {{
        background-color: #007BFF;
        color: white;
        font-weight: bold;
    }}

    .results-table td {{
        background-color: #f9f9f9;
    }}
    </style>

    <table class="results-table">
        <tr>
            <th>📊 Résultat</th>
            <th>Valeur</th>
        </tr>
        <tr>
            <td>📌 Nombre total d’anomalies détectées</td>
            <td><b>{total_anomalies_detectées}</b></td>
        </tr>
        <tr>
            <td>⚠️ Panne imminente détectée ?</td>
            <td><b>{"OUI" if panne_imminente else "NON"}</b></td>
        </tr>
    </table>
    """,
    unsafe_allow_html=True
)

    # ================================================================
    #  📌 VISUALISATION DES ANOMALIES
    # ================================================================

    st.markdown("### 📊 Visualisation des Anomalies")

    with st.expander("🔍 Afficher le graphique des anomalies détectées"):
	    fig, ax = plt.subplots(figsize=(5, 2))  # Taille plus réduite
	    sns.set_style("whitegrid")

	    # Courbe d'erreur
	    ax.plot(df_filtered["timestamp"], df_filtered["error"], label="Erreur de reconstruction",
	            color='#1f77b4', linewidth=0.8)

	    # Seuil d'anomalie
	    ax.axhline(threshold, color="r", linestyle="--", label="Seuil d'anomalie", linewidth=0.8)

	    # Anomalies détectées
	    ax.scatter(df_filtered.loc[df_filtered["anomaly"], "timestamp"],
	            df_filtered.loc[df_filtered["anomaly"], "error"],
	            color="red", marker="o", label="Anomalies détectées", s=10)  # Marqueurs plus petits

	    # Ajustement des ticks pour éviter la surcharge
	    ax.set_xticks(df_filtered["timestamp"][::50])
	    ax.set_xticklabels(df_filtered["timestamp"][::50], rotation=25, ha="right", fontsize=5)
	    ax.set_yticklabels(ax.get_yticks(), fontsize=5)


	    # Labels et titre réduits
	    ax.set_xlabel("Temps", fontsize=6)
	    ax.set_ylabel("Erreur", fontsize=6)
	    ax.set_title("📊 Anomalies détectées", fontsize=7, fontweight='bold')

	    # Légende plus compacte
	    ax.legend(loc="upper right", fontsize=5, frameon=True)

	    # 🔥 Réduction des marges pour que Streamlit ne l'agrandisse pas
	    plt.subplots_adjust(left=0.1, right=0.95, top=0.85, bottom=0.2)

	    # 🔥 Cette fois, on empêche complètement l’agrandissement par Streamlit
	    st.pyplot(fig, use_container_width=False)

    # ================================================================
    #  📌 VISUALISATION DES ANOMALIES
    # ================================================================

    st.markdown("### 🔍 Évolution des Variables autour des Anomalies")

    # Filtrer uniquement les anomalies
    df_anomalies = df_filtered[df_filtered["anomaly"]]

    with st.expander("📊 Afficher l'évolution des variables autour des anomalies"):
	    fig, ax = plt.subplots(figsize=(5, 2))  # Taille compacte
	    sns.set_style("whitegrid")
	    colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

	    # Tracer les variables importantes avec des lignes fines
	    for col, color in zip(["TP2", "DV_pressure", "Oil_temperature", "Motor_current"], colors):
	        ax.plot(df_filtered["timestamp"], df_filtered[col], label=col, color=color, linewidth=0.8)

	    # Marquer les anomalies avec des points rouges plus petits
	    ax.scatter(df_anomalies["timestamp"], df_anomalies["TP2"],
	            color="red", marker="o", label="Anomalies détectées", s=10)

	    # Ajustement des ticks pour éviter trop d’encombrement
	    ax.set_xticks(df_filtered["timestamp"][::50])
	    ax.set_xticklabels(df_filtered["timestamp"][::50], rotation=25, ha="right", fontsize=5)
	    ax.set_yticklabels(ax.get_yticks(), fontsize=5)

	    # Labels et titre réduits
	    ax.set_xlabel("Temps", fontsize=6)
	    ax.set_ylabel("Valeurs", fontsize=6)
	    ax.set_title("🔍 Variables & Anomalies", fontsize=7, fontweight='bold')

	    # Légende plus compacte
	    ax.legend(loc="upper left", fontsize=5, frameon=True)

	    # 🔥 Réduction des marges pour que Streamlit ne l'agrandisse pas
	    plt.subplots_adjust(left=0.1, right=0.95, top=0.85, bottom=0.2)

	    # 🔥 Désactivation du redimensionnement automatique par Streamlit
	    st.pyplot(fig, use_container_width=False)