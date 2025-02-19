from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import os
from backend.models_loader import load_models

# 🌍 **Initialisation de l'API Flask**
app = Flask(__name__)

# 📌 **Chemin du dossier des modèles**
MODEL_DIR = "data/models"

# ✅ **Chargement des modèles UNE SEULE FOIS**
models = load_models(MODEL_DIR)

# **Récupération des modèles nécessaires**
sae = models.get("sae")
scaler = models.get("scaler")
threshold = models.get("threshold", 0.0045)  # Valeur par défaut si non chargée


# ✅ **Vérifier que l'API est en ligne**
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": " API de prediction en ligne !"}), 200


# ✅ **Définition de l'endpoint pour charger un fichier CSV**
@app.route('/predict_csv', methods=['POST'])
def predict_from_csv():
    try:
        # 📌 **1️⃣ Vérifier si un fichier a été envoyé**
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier envoyé"}), 400

        file = request.files['file']

        # 📌 **2️⃣ Vérifier que le fichier est un CSV**
        if file.filename == '':
            return jsonify({"error": "Nom de fichier invalide"}), 400

        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Le fichier doit être au format CSV"}), 400

        # 📌 **3️⃣ Charger les données**
        df = pd.read_csv(file)

        if df.empty:
            return jsonify({"error": "Le fichier CSV est vide"}), 400

        # 📌 **4️⃣ Vérification des colonnes requises**
        required_columns = [
            "timestamp", "TP2", "TP3", "H1", "DV_pressure", "Reservoirs",
            "Oil_temperature", "Motor_current", "COMP", "DV_eletric",
            "Towers", "MPG", "LPS", "Pressure_switch", "Oil_level", "Caudal_impulses"
        ]

        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            return jsonify({"error": f"Colonnes manquantes : {', '.join(missing_cols)}"}), 400

        # 📌 **5️⃣ Normalisation des données**
        features_scaler = scaler.feature_names_in_
        df[features_scaler] = scaler.transform(df[features_scaler])

        # 📌 **6️⃣ Prédiction avec le modèle SAE**
        reconstructed_values = sae.predict(df[features_scaler])

        # **Calcul de l'erreur de reconstruction (MSE)**
        df["error"] = np.mean(np.square(df[features_scaler] - reconstructed_values), axis=1)

        # 📌 **7️⃣ Détection des anomalies**
        df["anomaly"] = df["error"] > threshold

        # 📌 **8️⃣ Détection de panne imminente**
        total_anomalies = df["anomaly"].sum()
        seuil_anomalies = 10  # Nombre d'anomalies avant d'alerter une panne
        panne_imminente = total_anomalies >= seuil_anomalies

        # 📌 **9️⃣ Retourner le résultat**
        result = {
            "total_anomalies_detectées": int(total_anomalies),
            "panne_imminente": "OUI" if panne_imminente else "NON"
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ **Lancement de l'API Flask**
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
