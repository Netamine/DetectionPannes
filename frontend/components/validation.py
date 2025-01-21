import streamlit as st
import pandas as pd

def validate_missing_data(df: pd.DataFrame):
    """Valide les données pour détecter les colonnes avec des valeurs manquantes."""
    missing_data = df.isnull().sum()
    if missing_data.any():
        st.warning("⚠️ Des colonnes avec des données manquantes ont été détectées :")
        for col, missing in missing_data[missing_data > 0].items():
            st.write(f"- **{col}** : {missing} valeurs manquantes")
    else:
        st.success("✅ Aucune donnée manquante détectée !")
