from flask import Blueprint, request, jsonify, current_app
import pandas as pd
import io
import logging
import traceback

# Configuration des logs
logging.basicConfig(level=logging.INFO)

# Création du blueprint pour les routes d'imputation
imputation_bp = Blueprint('imputation', __name__)

@imputation_bp.route('/')
def home():
    return jsonify(message="L'API fonctionne et les modèles sont chargés !")

@imputation_bp.route('/impute', methods=['POST'])
def impute():
    """
    Endpoint pour imputer les données manquantes dans un fichier CSV envoyé.
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

        imputation_models = current_app.config.get('IMPUTATION_MODELS', {})

        imputable_columns = list(imputation_models.keys())
        missing_columns = [col for col in data.columns if col in imputable_columns and data[col].isnull().any()]

        if not missing_columns:
            logging.info("✅ Aucune colonne imputable n'a de valeurs manquantes.")
            return jsonify({"message": "Aucune colonne imputable n'a de valeurs manquantes."}), 200

        logging.info(f"⚙️ Imputation des colonnes manquantes : {missing_columns}")

        for col in missing_columns:
            model = imputation_models.get(col)
            if model:
                logging.info(f"🔍 Vérification du modèle pour la colonne {col}, type : {type(model)}")

                # Vérifier si le modèle a la méthode get_params
                if hasattr(model, 'get_params'):
                    logging.info(f"✅ Modèle {col} prêt à l'utilisation, paramètres : {model.get_params()}")
                else:
                    logging.error(f"❌ Le modèle {col} ne contient pas la méthode get_params.")
                    return jsonify({"error": f"Le modèle {col} ne contient pas la méthode get_params"}), 500

                missing_rows = data[data[col].isnull()]
                if not missing_rows.empty:
                    features = missing_rows.drop(columns=[col])
                    predictions = model.predict(features)
                    data.loc[data[col].isnull(), col] = predictions

        logging.info("✅ Imputation terminée avec succès")
        return data.to_csv(index=False), 200

    except pd.errors.EmptyDataError:
        logging.error("❌ Le fichier CSV est vide ou invalide.")
        return jsonify({"error": "Le fichier CSV est vide ou invalide."}), 400

    except Exception as e:
        logging.error(f"❌ Erreur interne : {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500