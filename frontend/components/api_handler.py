import requests
import io
import pandas as pd

def send_to_api(df: pd.DataFrame):
    """Envoie les données à l'API pour obtenir une prédiction."""
    csv_data = df.to_csv(index=False)

    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict_csv",
            files={"file": ("file.csv", io.BytesIO(csv_data.encode("utf-8")))}
        )

        if response.status_code == 200:
            try:
                return response.json()  # 🔹 Correction : On lit directement la réponse en JSON
            except ValueError:
                print("❌ Erreur : Impossible de lire la réponse JSON de l'API.")
                return None
        else:
            print(f"❌ Erreur API : {response.status_code} - {response.text}")
            return None

    except requests.ConnectionError:
        print("❌ Erreur : Impossible de se connecter à l'API.")
        return None
    except requests.Timeout:
        print("❌ Erreur : Temps d'attente dépassé.")
        return None
    except requests.RequestException as e:
        print(f"❌ Erreur API : {e}")
        return None
