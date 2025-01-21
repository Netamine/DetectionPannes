import streamlit as st


def upload_file():
    """Affiche un widget de téléversement de fichier."""
    return st.file_uploader("Téléchargez un fichier CSV", type=["csv"])
