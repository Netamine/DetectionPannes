from flask import Flask
from flasgger import Swagger
from backend.models_loader import load_models
from backend.routes import register_routes
import os
from backend.models_loader import load_models

def create_app():
    app = Flask(__name__)

    # 📍 Correction du chemin pour `model_dir`
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'models')


    # Charger les modèles une seule fois
    app.config['IMPUTATION_MODELS'] = load_models(model_dir)

    # Initialisation de Swagger
    swagger = Swagger(app)

    # Enregistrer les routes
    register_routes(app)

    return app
