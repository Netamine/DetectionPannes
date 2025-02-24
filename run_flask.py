import os
import time
import logging
import subprocess
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from backend import create_app
from backend.utils.models_loader import load_models
from waitress import serve
from functools import wraps
from flasgger import swag_from
from backend.utils.security import api_key_required

# ✅ Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", force=True)

# ✅ Initialisation de l'application Flask via create_app()
app = create_app()

logging.info("✅ Flask est initialisé avec succès !")

# ✅ Vérification de l'API Key (force string pour éviter NoneType)
API_KEY = str(os.getenv("API_KEY", "")).strip()
if not API_KEY:
    logging.warning("⚠️ La variable d'environnement API_KEY est vide ou non définie.")
else:
    logging.info(f"🔑 API_KEY chargée : {API_KEY[:5]}*** (sécurisée)")

# ✅ Endpoint pour déboguer la clé API
@app.route('/debug_api_key', methods=['GET'])
def debug_api_key():
    return jsonify({
        "api_key_stockee": API_KEY,
        "api_key_reçue": request.headers.get("x-api-key")
    }), 200

# ✅ Définition des métriques Prometheus
REQUEST_COUNT = Counter("api_requests_total", "Nombre total de requêtes", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Temps de réponse des requêtes", ["endpoint"])

# ✅ Endpoint pour Prometheus
@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# ✅ Middleware pour mesurer la latence des requêtes
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    """ Log et enregistre les métriques des requêtes """
    if hasattr(request, "start_time"):
        request_latency = time.time() - request.start_time
        REQUEST_LATENCY.labels(endpoint=request.path).observe(request_latency)
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path, http_status=response.status_code).inc()
    return response

# ✅ Vérification si les modèles existent
model_dir = "data/models"
if not os.path.exists(model_dir) or not os.listdir(model_dir):
    logging.warning("⚠️ Aucun modèle trouvé, l'API fonctionnera sans modèles.")
    models = {}
else:
    logging.info("📥 Chargement des modèles...")
    models = load_models(model_dir)
    logging.info("✅ Modèles chargés avec succès !")

# ✅ Vérification des modèles chargés
sae = models.get("sae")
scaler = models.get("scaler")
threshold = models.get("threshold", 0.0045)  # Valeur par défaut
seuil_anomalies = 10  # 🔹 Seuil à partir duquel une panne est imminente

if sae is None or scaler is None:
    logging.warning("⚠️ Le modèle SAE ou le scaler n'a pas été chargé. Vérifiez `models_loader.py` et `data/models/`.")

# ✅ Endpoint de vérification du bon fonctionnement de l'API
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "message": "L'API est en ligne et fonctionne correctement."}), 200

# ✅ Endpoint sécurisé pour la prédiction
@app.route('/predict_csv', methods=['POST'])
@swag_from("/app/swagger/predict_csv.yaml")
@api_key_required
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
            return jsonify({"error": "Colonnes manquantes dans le fichier CSV"}), 400

        # Vérification de scaler avant transformation
        if not hasattr(scaler, "feature_names_in_"):
            logging.error("❌ Scaler mal initialisé ou absent.")
            return jsonify({"error": "Scaler mal initialisé."}), 500

        # Normalisation avec gestion des erreurs
        try:
            df[scaler.feature_names_in_] = scaler.transform(df[scaler.feature_names_in_])
        except Exception as e:
            logging.error(f"❌ Erreur de normalisation : {e}")
            return jsonify({"error": "Erreur de normalisation des données"}), 500

        # Prédiction
        try:
            reconstructed_values = sae.predict(df[scaler.feature_names_in_])
            df["error"] = np.mean(np.square(df[scaler.feature_names_in_] - reconstructed_values), axis=1)
            df["anomaly"] = df["error"] > threshold
        except Exception as e:
            logging.error(f"❌ Erreur lors de la prédiction : {e}")
            return jsonify({"error": "Erreur lors de la prédiction"}), 500

        # Détection de panne imminente
        total_anomalies = int(df["anomaly"].sum())
        panne_imminente = "OUI" if total_anomalies >= seuil_anomalies else "NON"

        return jsonify({
            "total_anomalies_detectées": total_anomalies,
            "panne_imminente": panne_imminente
        }), 200

    except Exception as e:
        logging.error(f"❌ Erreur interne du serveur : {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

# ✅ Démarrage du serveur
if __name__ == "__main__":
    logging.info("🚀 Démarrage du serveur Flask avec Waitress...")
    serve(app, host="0.0.0.0", port=5000)
