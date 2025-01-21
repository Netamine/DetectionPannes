import streamlit as st
import pandas as pd
from components import send_to_api, upload_file, validate_missing_data

# 🌟 Titre de l'application
st.title('Imputation Automatique des Données avec LightGBM')

# 📤 Téléchargement du fichier CSV
uploaded_file = upload_file()

# 🛠️ Traitement du fichier
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("📊 **Aperçu du fichier téléchargé :**", df.head())

    # 🔍 Validation des données manquantes
    validate_missing_data(df)

    # 📨 Envoi des données à l'API pour imputation
    if st.button('🛠️ Imputer les données manquantes'):
        imputed_df = send_to_api(df)
        if imputed_df is not None:
            st.success("✅ Données imputées avec succès !")
            st.write("📊 **Aperçu des données imputées :**", imputed_df.head())
        else:
            st.error("❌ Échec de l'imputation. Consultez les logs pour plus d'informations.")