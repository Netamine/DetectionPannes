import pandas as pd
import time
import streamlit as st
from tqdm import tqdm

#  **Colonnes requises pour le dataset**
REQUIRED_COLUMNS = [
    "timestamp", "TP2", "TP3", "H1", "DV_pressure", "Reservoirs",
    "Oil_temperature", "Motor_current", "COMP", "DV_eletric",
    "Towers", "MPG", "LPS", "Pressure_switch", "Oil_level", "Caudal_impulses"
]

def adjust_last_digit_of_seconds(timestamp):
    """Ajuste uniquement le dernier chiffre des secondes du timestamp."""
    seconds = timestamp.second
    last_digit = seconds % 10  # Extraire le dernier chiffre

    if 1 <= last_digit <= 5:
        adjustment = -last_digit  # Arrondir vers 0
    elif last_digit > 5:
        adjustment = 10 - last_digit  # Arrondir au multiple de 10 suivant
    else:
        adjustment = 0  # Déjà correct

    return timestamp + pd.Timedelta(seconds=adjustment)


def correct_timestamp_intervals(df):
    """
    Corrige les écarts de timestamps en ajustant les secondes et en insérant les timestamps manquants.

    :param df: DataFrame à corriger.
    :return: DataFrame avec des timestamps alignés à 10 secondes.
    """
    st.markdown("### 🛠️ Correction des Timestamps Manquants...")

    # Étape 1 : Ajuster les timestamps avec une barre de progression
    tqdm.pandas(desc="Ajustement des timestamps")
    df["timestamp"] = df["timestamp"].progress_apply(adjust_last_digit_of_seconds)

    #  Étape 2 : Ajouter les timestamps manquants
    start_time = time.time()

    while True:
        # Calculer les intervalles
        time_diffs = df["timestamp"].diff().dt.total_seconds()

        # Identifier les intervalles problématiques
        problematic_indices = time_diffs[time_diffs > 10].index

        if len(problematic_indices) == 0:
            break  # Tous les écarts sont corrigés

        # Correction du premier écart
        idx = problematic_indices[0]
        start = df.loc[idx - 1, "timestamp"]
        end = df.loc[idx, "timestamp"]

        # Générer les timestamps intermédiaires
        new_times = pd.date_range(start=start, end=end, freq="10S")

        # Insérer dans le DataFrame
        missing_data = pd.DataFrame({"timestamp": new_times})
        df = pd.concat([df, missing_data]).drop_duplicates(subset="timestamp").sort_values("timestamp").reset_index(
            drop=True)

    # 🚀 Statistiques finales
    execution_time = time.time() - start_time
    st.success(f"✅ Correction des timestamps terminée en {execution_time:.2f} secondes.")

    return df

def impute_missing_values(df, models):
    """
    Effectue l'imputation des valeurs manquantes dans le dataset à l'aide des modèles.

    :param df: DataFrame contenant les données.
    :param models: Dictionnaire des modèles d'imputation.
    :return: DataFrame après imputation.
    """
    st.markdown(
        "<h3 style='color:#007BFF; font-weight:bold;'>..Imputation des Données</h3>",
        unsafe_allow_html=True
    )
    # **Créer une copie temporaire du dataset avant imputation**
    df_original = df.copy()

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce').astype('int64') // 10 ** 9

    #  **Imputation des valeurs manquantes**
    for col in filter(lambda c: c != "timestamp", REQUIRED_COLUMNS):
        if col in models and col in df.columns:
            missing_indices = df[df[col].isnull()].index
            if not missing_indices.empty:
                try:
                    # 🛠️ Extraire les features utilisées lors de l'entraînement du modèle
                    expected_features = models[col].feature_names_in_

                    # ✅ Vérifier que `timestamp` est bien exclu des features passées au modèle
                    expected_features = [feat for feat in expected_features if feat != "timestamps"]

                    # 🛠️ Sélectionner uniquement les features attendues par le modèle
                    df_features = df.loc[missing_indices, expected_features].copy()

                    # 🛠️ Convertir les colonnes en float si nécessaire
                    df_features = df_features.astype(float)

                    # 🔄 Faire la prédiction
                    df.loc[missing_indices, col] = models[col].predict(df_features)

                    st.markdown(f"<div class='alert-success'>✅ Imputation effectuée pour {col}.</div>",
                                unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"<div class='alert-error'>❌ Erreur d'imputation pour {col} : {e}</div>",
                                unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-warning'>⚠️ Modèle introuvable pour {col}, aucune imputation faite.</div>",
                        unsafe_allow_html=True)

    # ✅ **Réintégrer `timestamp` après l'imputation**
    df["timestamp"] = df_original["timestamp"]

    return df