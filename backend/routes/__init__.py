from .general import general_bp
from .imputation import imputation_bp

def register_routes(app):
    app.register_blueprint(general_bp)
    app.register_blueprint(imputation_bp)