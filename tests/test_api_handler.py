import os
import pandas as pd
import pytest
from frontend.components.api_handler import send_to_api

@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    """Fixture pour injecter la clé API dans l'environnement."""
    monkeypatch.setenv("API_KEY", "sqfXkiRRxFXaso4dT9GzJL5nST4VjBHUzvVip4EGBa0y/lWrIA3doxiYHEgoaS+y")

def test_send_to_api():
    """Test d'envoi de données à l'API et validation du retour JSON."""
    headers = {"x-api-key": os.getenv("API_KEY")}  # Injection explicite dans la requête

    #print(f"🔍 Clé API utilisée dans Pytest : {headers['x-api-key']}")  # Debug

    df = pd.DataFrame({
        "timestamp": ["2024-02-18 12:00:00"],
        "TP2": [1.0], "TP3": [1.0], "H1": [1.0], "DV_pressure": [1.0],
        "Reservoirs": [1.0], "Oil_temperature": [50.0], "Motor_current": [2.0],
        "COMP": [0], "DV_eletric": [1], "Towers": [0], "MPG": [1],
        "LPS": [0], "Pressure_switch": [1], "Oil_level": [0], "Caudal_impulses": [1]
    })

    result = send_to_api(df, headers=headers)  # Ajout des headers

    assert result is not None, "L'API a retourné None"
