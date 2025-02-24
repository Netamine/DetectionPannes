import os
from flasgger import swag_from
from flask import Blueprint, request, jsonify
import pandas as pd
import io
import logging
import traceback

# Configuration des logs
logging.basicConfig(level=logging.INFO)

# Création du blueprint
imputation_bp = Blueprint('imputation', __name__)

# 📌 Chemin du fichier YAML
swagger_yaml_path = os.path.join(os.path.dirname(__file__), "..", "..", "swagger", "imputation.yaml")

@imputation_bp.route('/impute', methods=['POST'])
@swag_from(swagger_yaml_path)
def impute():
    """
    Endpoint pour imputer les données manquantes dans un fichier CSV.
    """
    logging.info("📩 Réception d'une requête d'imputation")

    try:
        file = request.files.get('file')
        if not file:
            logging.error("❌ Aucun fichier n'a été envoyé.")
            return jsonify({"error": "Aucun fichier n'a été envoyé."}), 400

        content = file.read().decode('utf-8')
        if not content.strip():
            logging.error("❌ Le fichier CSV est vide.")
            return jsonify({"error": "Le fichier CSV est vide."}), 400

        data = pd.read_csv(io.StringIO(content))
        logging.info(f"🔍 Données reçues avec {data.shape[0]} lignes et {data.shape[1]} colonnes")

        return data.to_csv(index=False), 200

    except pd.errors.EmptyDataError:
        logging.error("❌ Le fichier CSV est vide ou invalide.")
        return jsonify({"error": "Le fichier CSV est vide ou invalide."}), 400

    except Exception as e:
        logging.error(f"❌ Erreur interne : {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
