from flask import Blueprint, jsonify, request, current_app
import pandas as pd
import logging

# 📌 Configuration des logs
logging.basicConfig(level=logging.INFO)

# 📌 Création du Blueprint pour centraliser toutes les routes
routes_bp = Blueprint('routes', __name__)

# 📌 Route principale de test
@routes_bp.route('/')
def home():
    return jsonify({"message": "L'API fonctionne et les modèles sont chargés !"}), 200

# 📌 Endpoint pour imputer les données manquantes dans un fichier CSV
@routes_bp.route('/impute', methods=['POST'])
def impute():
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

        df = pd.read_csv(pd.compat.StringIO(content))
        logging.info(f"🔍 Données reçues avec {df.shape[0]} lignes et {df.shape[1]} colonnes")

        # 📌 Récupération des modèles d'imputation
        imputation_models = current_app.config.get('IMPUTATION_MODELS', {})

        imputable_columns = list(imputation_models.keys())
        missing_columns = [col for col in df.columns if col in imputable_columns and df[col].isnull().any()]

        if not missing_columns:
            logging.info("✅ Aucune colonne imputable n'a de valeurs manquantes.")
            return jsonify({"message": "Aucune colonne imputable n'a de valeurs manquantes."}), 200

        logging.info(f"⚙️ Imputation des colonnes manquantes : {missing_columns}")

        for col in missing_columns:
            model = imputation_models.get(col)
            if model:
                logging.info(f"🔍 Modèle utilisé pour la colonne {col}")

                # Vérifier si le modèle a la méthode `predict`
                if not hasattr(model, 'predict'):
                    logging.error(f"❌ Le modèle {col} ne contient pas la méthode predict.")
                    return jsonify({"error": f"Le modèle {col} ne contient pas la méthode predict"}), 500

                missing_rows = df[df[col].isnull()]
                if not missing_rows.empty:
                    features = missing_rows.drop(columns=[col])
                    predictions = model.predict(features)
                    df.loc[df[col].isnull(), col] = predictions

        logging.info("✅ Imputation terminée avec succès")
        return df.to_csv(index=False), 200

    except Exception as e:
        logging.error(f"❌ Erreur interne : {str(e)}")
        return jsonify({"error": str(e)}), 500