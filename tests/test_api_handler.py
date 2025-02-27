import os
import requests
import pandas as pd
import pytest
from backend.api_handler import send_to_api


def test_send_to_api():
    """Test d'envoi de données à l'API et validation du retour JSON."""

    headers = {"x-api-key": os.getenv("API_KEY")}  # Injection explicite dans la requête
    print(f"🔍 Clé API utilisée dans Pytest : {headers['x-api-key']}")  # Debug

    # Vérifier si l'API est accessible
    api_url = "http://localhost:5000/health"  # Remplace avec ton endpoint de santé
    try:
        response = requests.get(api_url, timeout=5)  # Timeout pour éviter de bloquer le test
        if response.status_code != 200:
            pytest.skip(f"🚨 L'API est down ! Status code : {response.status_code}")
    except requests.exceptions.RequestException:
        pytest.skip("🚨 L'API est down ! Impossible de se connecter.")

    # Données de test
    df = pd.DataFrame(
        {
            "timestamp": ["2024-02-18 12:00:00"],
            "TP2": [1.0], "TP3": [1.0], "H1": [1.0], "DV_pressure": [1.0],
            "Reservoirs": [1.0], "Oil_temperature": [50.0], "Motor_current": [2.0],
            "COMP": [0], "DV_eletric": [1], "Towers": [0], "MPG": [1],
            "LPS": [0], "Pressure_switch": [1], "Oil_level": [0], "Caudal_impulses": [1]
        }
    )

    result = send_to_api(df, headers=headers)  # Ajout des headers

    assert result is not None, "L'API a retourné None"
