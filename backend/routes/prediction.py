from flask import Blueprint, request, jsonify
import pandas as pd
import numpy as np
import os
#from run_flask import api_key_required
from backend.utils.security import api_key_required
from backend.utils.models_loader import load_models  # Charger les modèles

# ✅ Création du blueprint pour la prédiction
prediction_bp = Blueprint('prediction', __name__)

# ✅ Charger les modèles UNE SEULE FOIS
model_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "models")
models = load_models(model_dir)

# ✅ Vérifier que les modèles sont bien chargés
sae = models.get("sae")
scaler = models.get("scaler")
threshold = models.get("threshold", 0.0045)  # Valeur par défaut
seuil_anomalies = 10  # Seuil à partir duquel une panne est imminente

if sae is None or scaler is None:
    raise ValueError("❌ ERREUR : Le modèle SAE ou le scaler n'a pas été chargé.")

# ✅ Endpoint principal de test
@prediction_bp.route('/')
def home():
    return jsonify(message="L'API Prediction fonctionne et les modèles sont chargés !")

# ✅ Endpoint de prédiction
@prediction_bp.route('/predict_csv', methods=['POST'])
@api_key_required
def predict_from_csv():
    """
    Endpoint pour analyser un fichier CSV et détecter les anomalies.
    """
    try:
        # 📌 Vérifier si un fichier a été envoyé
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier envoyé"}), 400

        file = request.files['file']

        # 📌 Vérifier si le fichier est valide
        if file.filename == '':
            return jsonify({"error": "Nom de fichier invalide"}), 400
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Le fichier doit être au format CSV"}), 400

        # 📌 Charger le fichier CSV
        df = pd.read_csv(file)

        if df.empty:
            return jsonify({"error": "Le fichier CSV est vide"}), 400

        # 📌 Vérification des colonnes requises
        required_columns = [
            "timestamp", "TP2", "TP3", "H1", "DV_pressure", "Reservoirs",
            "Oil_temperature", "Motor_current", "COMP", "DV_eletric",
            "Towers", "MPG", "LPS", "Pressure_switch", "Oil_level", "Caudal_impulses"
        ]

        if not set(required_columns).issubset(df.columns):
            return jsonify({"error": "Colonnes manquantes dans le fichier CSV"}), 400

        # 📌 Normalisation des données
        df[scaler.feature_names_in_] = scaler.transform(df[scaler.feature_names_in_])

        # 📌 Prédiction
        reconstructed_values = sae.predict(df[scaler.feature_names_in_])
        df["error"] = np.mean(np.square(df[scaler.feature_names_in_] - reconstructed_values), axis=1)
        df["anomaly"] = df["error"] > threshold

        # 📌 Détection de panne imminente
        total_anomalies = int(df["anomaly"].sum())
        panne_imminente = "OUI" if total_anomalies >= seuil_anomalies else "NON"

        return jsonify({
            "total_anomalies_detectées": total_anomalies,
            "panne_imminente": panne_imminente
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
