# Utiliser une image légère de Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y git && \
    pip install --no-cache-dir dvc[gdrive] && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copier uniquement les fichiers nécessaires
COPY requirements.txt ./

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'ensemble du projet
COPY . .

# Copier la clé d'authentification Google Drive
COPY keys/CleDVCJason.json /root/.config/dvc/CleDVCJason.json

# Définir la variable d’environnement pour DVC
ENV GDRIVE_CREDENTIALS_DATA="/root/.config/dvc/CleDVCJason.json"

# ✅ Ajouter une API Key pour sécuriser les requêtes
ENV API_KEY="sqfXkiRRxFXaso4dT9GzJL5nST4VjBHUzvVip4EGBa0y/lWrIA3doxiYHEgoaS+y"

# Initialiser DVC et configurer le remote Google Drive
RUN dvc init --no-scm && \
    dvc remote add -d dvc_data gdrive://1G3bpMF46owL-_Z1mnEtmrJ_61nWQlRfO && \
    dvc remote modify dvc_data gdrive_use_service_account true && \
    dvc remote modify dvc_data gdrive_service_account_json_file_path /root/.config/dvc/CleDVCJason.json

# Vérifier si les modèles existent, sinon les récupérer
RUN if [ ! -d "data/models" ] || [ -z "$(ls -A data/models)" ]; then \
        echo "📌 Modèles absents, récupération avec DVC..."; \
        dvc pull && rm -rf .dvc/cache; \
    else \
        echo "✅ Modèles déjà présents, pas de récupération nécessaire."; \
    fi

# Nettoyer le cache DVC
RUN rm -rf .dvc/cache

# Exposer les ports nécessaires pour Flask et Streamlit
EXPOSE 5000 8501

# Définition des variables d'environnement
ENV TF_ENABLE_ONEDNN_OPTS=0

# Lancer `dvc pull` au démarrage (au cas où ça a échoué avant)
CMD ["sh", "-c", "dvc pull && python run_flask.py & streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0"]
