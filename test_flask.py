from flask import Flask
import os
from waitress import serve

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Test Flask API is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Récupérer le port depuis Render
    print(f"Lancement du serveur Flask avec Waitress sur le port {port}...")
    serve(app, host="0.0.0.0", port=port)
