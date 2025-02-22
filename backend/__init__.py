import os
import logging
from flask import Flask
from backend.routes import routes_bp
from backend.utils.models_loader import load_models

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_app():
    """Création et configuration de l'application Flask."""
    app = Flask(__name__)

    # 📌 Définition du répertoire des modèles
    model_dir = os.path.join(os.path.dirname(__file__), "..", "data", "models")

    # 📌 Chargement des modèles UNE SEULE FOIS
    if os.path.exists(model_dir):
        app.config["IMPUTATION_MODELS"] = load_models(model_dir)
        logging.info("✅ Modèles d'imputation chargés et stockés dans la config Flask.")
    else:
        app.config["IMPUTATION_MODELS"] = {}
        logging.warning("⚠️ Aucun modèle trouvé, l'API fonctionnera sans imputation.")

    # 📌 Enregistrement des routes
    app.register_blueprint(routes_bp)

    # Vérifier que tous les modèles sont bien chargés
    logging.info(f"📌 Modèles disponibles dans Flask : {list(app.config['IMPUTATION_MODELS'].keys())}")

    logging.info("🚀 Application Flask créée avec succès !")

    return app
