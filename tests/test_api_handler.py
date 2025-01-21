import pytest
import pandas as pd
from frontend.components.api_handler import send_to_api

def test_send_to_api():
 df = pd.DataFrame({"col1": [1, 2, None], "col2": [4, 5, 6]})
 result = send_to_api(df)
 assert result is not None  # Vérifie si l'API retourne des données
 assert isinstance(result, pd.DataFrame)  # Vérifie si le retour est un DataFrame
