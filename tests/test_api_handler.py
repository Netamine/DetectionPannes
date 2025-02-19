import pytest
import pandas as pd
import requests
from frontend.components.api_handler import send_to_api

def test_send_to_api():
    # Création d'un DataFrame avec toutes les colonnes attendues
    df = pd.DataFrame({
        "timestamp": ["2024-02-18 12:00:00"],  # Exemple de timestamp valide
        "TP2": [1.0],
        "TP3": [1.0],
        "H1": [1.0],
        "DV_pressure": [1.0],
        "Reservoirs": [1.0],
        "Oil_temperature": [50.0],
        "Motor_current": [2.0],
        "COMP": [0],
        "DV_eletric": [1],
        "Towers": [0],
        "MPG": [1],
        "LPS": [0],
        "Pressure_switch": [1],
        "Oil_level": [0],
        "Caudal_impulses": [1]
    })

    result = send_to_api(df)

    print(f"Résultat API : {result}")  # Debugging

    assert result is not None, "L'API a retourné None"
    assert isinstance(result, dict), "L'API n'a pas retourné un dictionnaire JSON"
    assert "panne_imminente" in result, "La clé 'panne_imminente' n'est pas présente"
    assert "total_anomalies_detectées" in result, "La clé 'total_anomalies_detectées' n'est pas présente"
