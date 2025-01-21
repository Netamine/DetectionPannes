from flask import Flask
from backend.models_loader import load_models
from backend.routes import register_routes

def create_app():
    app = Flask(__name__)

    # Charger les modèles une seule fois
    app.config['IMPUTATION_MODELS'] = load_models()

    # Enregistrer les routes
    register_routes(app)

    return app
