from flask import Flask
import os
from waitress import serve
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Test Flask API is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Récupération du port de Render
    print(f"🔄 Attente avant le lancement du serveur...")
    time.sleep(5)  # Attendre 5 secondes pour laisser Render scanner les ports
    print(f"🚀 Lancement du serveur Flask avec Waitress sur le port {port}...")
    try:
        serve(app, host="0.0.0.0", port=port)
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
