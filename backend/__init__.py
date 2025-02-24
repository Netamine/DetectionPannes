import os
import logging
from flask import Flask
from flasgger import Swagger
from backend.utils.models_loader import load_models

# ✅ Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def create_app():
    """Création et configuration de l'application Flask."""
    app = Flask(__name__)

    # 📌 Importer `register_routes` ici pour éviter l'importation circulaire
    from backend.routes import register_routes

    # 📌 Définition du répertoire des modèles
    model_dir = os.path.join(os.path.dirname(__file__), "..", "data", "models")

    # 📌 Chargement des modèles UNE SEULE FOIS
    if os.path.exists(model_dir):
        app.config["IMPUTATION_MODELS"] = load_models(model_dir)
        logging.info("✅ Modèles d'imputation chargés et stockés dans la config Flask.")
    else:
        app.config["IMPUTATION_MODELS"] = {}
        logging.warning("⚠️ Aucun modèle trouvé, l'API fonctionnera sans imputation.")

    # ✅ Enregistrer les routes AVANT Swagger
    register_routes(app)

    # 📌 Vérifier si les fichiers Swagger existent avant d'activer Swagger
    swagger_dir = os.path.join(os.path.dirname(__file__), "..", "swagger")
    if os.path.exists(swagger_dir) and any(f.endswith(".yaml") for f in os.listdir(swagger_dir)):
        logging.info("✅ Fichiers Swagger détectés, activation de Swagger...")

        swagger_config = {
            "headers": [],
            "specs": [
                {
                    "endpoint": "apispec_1",
                    "route": "/apispec_1.json",
                    "rule_filter": lambda rule: True,  # Applique la doc à toutes les routes
                    "model_filter": lambda tag: True,  # Inclut tous les modèles
                }
            ],
            "static_url_path": "/flasgger_static",
            "swagger_ui": True,
            "specs_route": "/apidocs/"
        }

        # ✅ Vérifier que Swagger n'est pas déjà activé
        if not hasattr(app, "swagger"):
            Swagger(app, config=swagger_config)
            logging.info("✅ Swagger activé avec configuration personnalisée.")
    else:
        logging.warning("⚠️ Aucun fichier Swagger trouvé, Swagger ne sera pas activé.")

    return app

__all__ = ["create_app"]
