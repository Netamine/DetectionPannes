import os
from flask import Flask, jsonify
from waitress import serve

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "API en ligne avec Waitress !"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Lancement de l'API Flask avec Waitress sur le port {port}...")
    serve(app, host="0.0.0.0", port=port)
