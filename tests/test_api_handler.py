import os
import requests
import pandas as pd
import pytest
from frontend.components.api_handler import send_to_api

def is_api_available():
    """Vérifie si l'API est en ligne"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

@pytest.mark.skipif(not is_api_available(), reason="L'API est down, test ignoré.")
def test_send_to_api():
    """Test d'envoi de données à l'API et validation du retour JSON."""
    headers = {"x-api-key": os.getenv("API_KEY")}

    df = pd.DataFrame({
        "timestamp": ["2024-02-18 12:00:00"],
        "TP2": [1.0], "TP3": [1.0], "H1": [1.0], "DV_pressure": [1.0],
        "Reservoirs": [1.0], "Oil_temperature": [50.0], "Motor_current": [2.0],
        "COMP": [0], "DV_eletric": [1], "Towers": [0], "MPG": [1],
        "LPS": [0], "Pressure_switch": [1], "Oil_level": [0], "Caudal_impulses": [1]
    })

    result = send_to_api(df, headers=headers)

    assert result is not None, "L'API a retourné None"
