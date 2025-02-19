import streamlit as st
import pandas as pd

# 📌 **Colonnes requises pour le dataset**
REQUIRED_COLUMNS = [
    "timestamp", "TP2", "TP3", "H1", "DV_pressure", "Reservoirs",
    "Oil_temperature", "Motor_current", "COMP", "DV_eletric",
    "Towers", "MPG", "LPS", "Pressure_switch", "Oil_level", "Caudal_impulses"
]


def validate_missing_data(df: pd.DataFrame):
    """Valide les données pour détecter les colonnes avec des valeurs manquantes."""
    missing_data = df.isnull().sum()
    if missing_data.any():
        st.markdown("<div class='alert-warning'>⚠️ **Données manquantes détectées** :</div>", unsafe_allow_html=True)
        for col, missing in missing_data[missing_data > 0].items():
            st.write(f"- **{col}** : {missing} valeurs manquantes")
    else:
        st.markdown("<div class='alert-success'>✅ **Aucune donnée manquante détectée !**</div>", unsafe_allow_html=True)

def display_message(message, status="info", col=None):
    """Affiche un message formaté avec couleur selon le statut dans la colonne spécifiée."""
    color_map = {
        "success": "#d4edda",  # Vert doux
        "warning": "#fff3cd",  # Jaune doux
        "error": "#f8d7da"  # Rouge doux
    }
    icon_map = {
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }

    if col:
        col.markdown(
            f"<div style='padding:8px;border-radius:5px;background:{color_map[status]};"
            f"border-left: 5px solid {color_map[status]};margin-bottom:5px;'>"
            f"<b>{icon_map[status]} {message}</b></div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='padding:8px;border-radius:5px;background:{color_map[status]};"
            f"border-left: 5px solid {color_map[status]};margin-bottom:5px;'>"
            f"<b>{icon_map[status]} {message}</b></div>",
            unsafe_allow_html=True
        )


def validate_data(df):
    """
    Valide le dataset et affiche les résultats en deux colonnes.
    """

    st.markdown(
        "<h3 style='color:#007BFF; font-weight:bold;'>..Validation des Données</h3>",
        unsafe_allow_html=True
    )

    # Créer deux colonnes pour séparer validations et erreurs/avertissements
    col_success, col_warning = st.columns(2)

    # 📌 **1. Vérification du fichier**
    if not isinstance(df, pd.DataFrame):
        display_message("Format incorrect. Veuillez télécharger un fichier CSV.", "error", col_warning)
        return False, None

    # 📌 **2. Vérification des colonnes**
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        display_message(f"Colonnes manquantes : {', '.join(missing_columns)}", "error", col_warning)
        return False, None
    display_message("Toutes les colonnes requises sont présentes.", "success", col_success)

    # 📌 **3. Validation des timestamps**
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    if df["timestamp"].isnull().sum() > 0:
        display_message("Certains timestamps sont invalides.", "error", col_warning)
        return False, None
    display_message("Les timestamps sont valides.", "success", col_success)

    # 📌 **4. Nombre d'observations**
    if df.shape[0] < 10:
        display_message("Le dataset doit contenir au moins 10 observations.", "error", col_warning)
        return False, None
    display_message(f"Nombre d'observations : {df.shape[0]}.", "success", col_success)

    # 📌 **5. Vérification des doublons**
    duplicate_timestamps = df["timestamp"].duplicated().sum()
    duplicates_count = df.duplicated(subset=REQUIRED_COLUMNS).sum()

    warning_messages = []
    if duplicate_timestamps > 0:
        warning_messages.append(f"{duplicate_timestamps} timestamps en double détectés.")
    if duplicates_count > 0:
        df.drop_duplicates(subset=REQUIRED_COLUMNS, inplace=True)
        warning_messages.append(f"{duplicates_count} doublons supprimés.")

    if warning_messages:
        display_message("Problèmes détectés et corrigés:<br>" + "<br>".join(warning_messages), "warning",
                        col_warning)

    # 📌 **6. Vérification de l'intervalle de l’échantillon**
    total_duration = (df["timestamp"].max() - df["timestamp"].min()).total_seconds() / 60
    if total_duration > 30:
        display_message("L'intervalle de l'échantillon dépasse 30 minutes.", "error", col_warning)
        return False, None
    display_message("Intervalle de l'échantillon respecté (<30 minutes).", "success", col_success)

    # 📌 **7. Vérification du respect du gap de 10 secondes**
    gaps = df["timestamp"].diff().dt.total_seconds().dropna()
    incorrect_gaps = (gaps != 10).sum()
    if incorrect_gaps > 0:
        display_message(f"{incorrect_gaps} écarts incorrects détectés.", "warning", col_warning)

    # 📌 **8. Vérification des valeurs manquantes**
    missing_percentage = df.isnull().mean().max() * 100
    if missing_percentage > 12:
        display_message(f"Trop de valeurs manquantes ({missing_percentage:.2f}%).", "error", col_warning)
        return False, None
    elif missing_percentage > 0:
        display_message(f"Des valeurs manquantes détectées ({missing_percentage:.2f}%).", "warning", col_warning)

    # 📌 **9. Suppression des colonnes inutiles**
    df = df[[col for col in REQUIRED_COLUMNS if col in df.columns]]
    display_message("Colonnes inutiles supprimées.", "success", col_success)

    # 📌 **10. Résumé final**
    display_message(f"Validation terminée.","success", col_success)

    return True, df
