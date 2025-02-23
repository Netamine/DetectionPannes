from flask import request, jsonify
import os
from functools import wraps
import logging

# Récupération sécurisée de l'API Key
# API_KEY = os.getenv("api_key")

# ✅ Vérification de l'API Key (force string pour éviter NoneType)
API_KEY = str(os.getenv("API_KEY", "")).strip()
if not API_KEY:
    logging.warning("⚠️ La variable d'environnement API_KEY est vide ou non définie.")
else:
    logging.info(f"🔑 API_KEY chargée : {API_KEY[:5]}*** (sécurisée)")

def api_key_required(f: object) -> object:
    """ Vérifie que l'API Key est valide pour accéder aux endpoints sécurisés. """
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        logging.info(f"🔍 Clé API reçue : {api_key}")  # 🔹 Log pour voir la clé reçue
        logging.info(f"🔐 Clé API stockée : {API_KEY}")  # 🔹 Log pour voir la clé stockée
        if not api_key or api_key != API_KEY:
            logging.warning("❌ Accès refusé : API Key invalide !")
            return jsonify({"error": "❌ Accès refusé ! API Key invalide."}), 403
        return f(*args, **kwargs)
    return decorated


