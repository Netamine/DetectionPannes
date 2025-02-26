from flask import Blueprint, jsonify

general_bp = Blueprint('general', __name__)

@general_bp.route('/')
def home():
    return jsonify({"message": "L'API fonctionne et les modèles sont chargés !"}), 200
