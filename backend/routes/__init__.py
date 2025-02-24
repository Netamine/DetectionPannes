from .general import general_bp
from .imputation import imputation_bp
from .prediction import prediction_bp
import logging

def register_routes(app):
    logging.info("📌 Tentative d'enregistrement des routes...")  
    print("📌 Tentative d'enregistrement des routes...")  

    app.register_blueprint(general_bp, url_prefix='/')
    logging.info("✅ Route 'general' enregistrée !")
    print("✅ Route 'general' enregistrée !")

    app.register_blueprint(imputation_bp, url_prefix='/')
    logging.info("✅ Route 'imputation' enregistrée !")
    print("✅ Route 'imputation' enregistrée !")

    app.register_blueprint(prediction_bp, url_prefix='/')
    logging.info("✅ Route 'prediction' enregistrée !")
    print("✅ Route 'prediction' enregistrée !")

    logging.info("✅ Toutes les routes ont été enregistrées avec succès.")
    print("✅ Toutes les routes ont été enregistrées avec succès.")
