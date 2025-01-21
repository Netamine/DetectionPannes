from flask import Blueprint

general_bp = Blueprint('general', __name__)

@general_bp.route('/')
def home():
    return "L'API fonctionne et les modèles sont chargés !"
