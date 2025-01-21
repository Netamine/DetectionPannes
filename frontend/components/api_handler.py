import requests
import io
import pandas as pd

def send_to_api(df: pd.DataFrame):
    """Envoie les données à l'API pour imputation et retourne le DataFrame imputé."""
    csv_data = df.to_csv(index=False)
    try:
        response = requests.post("http://127.0.0.1:5000/impute", files={"file": ("file.csv", io.StringIO(csv_data))})

        if response.status_code == 200:
            return pd.read_csv(io.StringIO(response.text))
        else:
            print(f"❌ Erreur API : {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"❌ Erreur lors de l'appel API : {e}")
        return None