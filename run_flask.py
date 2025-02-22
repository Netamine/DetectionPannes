from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import os
import logging
import subprocess
from backend.utils.models_loader import load_models
from waitress import serve

# 📌 Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# 📌 Vérifier si les modèles existent, sinon, les récupérer via DVC
model_dir = "data/models"
if not os.path.exists(model_dir) or not os.listdir(model_dir):
    logging.info("📥 Modèles absents, tentative de récupération via DVC...")
    subprocess.run(["dvc", "pull"], check=True)
    logging.info("✅ Modèles récupérés avec succès !")

# 📌 Initialisation de l'application Flask
app = Flask(__name__)

# 📌 Chargement des modèles
models = load_models(model_dir)

# 📌 Vérification des modèles chargés
sae = models.get("sae")
scaler = models.get("scaler")
threshold = models.get("threshold", 0.0045)  # Valeur par défaut
seuil_anomalies = 10  # 🔹 Seuil à partir duquel une panne est imminente

if sae is None or scaler is None:
    logging.error("❌ Le modèle SAE ou le scaler n'a pas été chargé. Vérifiez `models_loader.py` et `data/models/`.")
    raise ValueError("Modèle SAE ou scaler manquant. Vérifiez que `sae_trained.keras` et `scaler.pkl` existent.")

# 📌 API Key pour sécuriser les endpoints
API_KEY = os.getenv("API_KEY", "sqfXkiRRxFXaso4dT9GzJL5nST4VjBHUzvVip4EGBa0y/lWrIA3doxiYHEgoaS+y")  # Remplace en prod

def api_key_required(f):
    """ Middleware pour vérifier l'API Key dans les requêtes. """
    def decorated(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key != API_KEY:
            return jsonify({"message": "❌ Accès refusé ! API Key invalide."}), 403
        return f(*args, **kwargs)
    return decorated

# ✅ Vérifier que l'API est en ligne
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API de prédiction en ligne !"}), 200

# ✅ Endpoint sécurisé avec API Key pour la prédiction
@app.route('/predict_csv', methods=['POST'])
@api_key_required  # Sécurisation avec API Key
def predict_from_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier envoyé"}), 400

        file = request.files['file']
        df = pd.read_csv(file)

        # Vérification des colonnes requises
        required_columns = [
            "timestamp", "TP2", "TP3", "H1", "DV_pressure", "Reservoirs",
            "Oil_temperature", "Motor_current", "COMP", "DV_eletric",
            "Towers", "MPG", "LPS", "Pressure_switch", "Oil_level", "Caudal_impulses"
        ]

        if not set(required_columns).issubset(df.columns):
            return jsonify({"error": "Colonnes manquantes"}), 400

        # Normalisation
        df[scaler.feature_names_in_] = scaler.transform(df[scaler.feature_names_in_])

        # Prédiction
        reconstructed_values = sae.predict(df[scaler.feature_names_in_])
        df["error"] = np.mean(np.square(df[scaler.feature_names_in_] - reconstructed_values), axis=1)
        df["anomaly"] = df["error"] > threshold

        # Détection de panne imminente
        total_anomalies = int(df["anomaly"].sum())
        panne_imminente = "OUI" if total_anomalies >= seuil_anomalies else "NON"

        return jsonify({
            "total_anomalies_detectées": total_anomalies,
            "panne_imminente": panne_imminente
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)