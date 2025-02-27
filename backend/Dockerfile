# Utiliser une image légère de Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Désactiver CUDA si nécessaire
ENV CUDA_VISIBLE_DEVICES=""

# Installer Tini pour la gestion des processus
RUN apt-get update && apt-get install -y tini && apt-get clean && rm -rf /var/lib/apt/lists/*

# Définir l'entrée de commande avec Tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# Installer les dépendances système et DVC
RUN apt-get update && apt-get install -y \
    git \
    wget \
    && pip install --no-cache-dir dvc[gdrive] \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances et les installer
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Installer Flasgger
RUN pip install --no-cache-dir flasgger

# Copier les scripts principaux
COPY run.py /app/run.py
COPY run_flask.py /app/run_flask.py
COPY data/models.dvc /app/data/models.dvc


# Copier la clé d'authentification Google Drive
COPY keys/CleDVCJason.json /root/.config/dvc/CleDVCJason.json

# Copier le backend et le frontend
COPY backend /app/backend
COPY frontend /app/frontend

# Définir la variable d'environnement pour DVC
ENV GDRIVE_CREDENTIALS_DATA="/root/.config/dvc/CleDVCJason.json"

# Initialiser DVC et configurer le remote Google Drive
RUN dvc init --no-scm && \
    dvc remote add -d dvc_data gdrive://1G3bpMF46owL-_Z1mnEtmrJ_61nWQlRfO && \
    dvc remote modify dvc_data gdrive_use_service_account true && \
    dvc remote modify dvc_data gdrive_service_account_json_file_path /root/.config/dvc/CleDVCJason.json

# Vérifier si le répertoire des modèles existe, sinon le créer
RUN mkdir -p /app/data/models

# Vérifier si models.dvc existe, puis récupérer les modèles avec DVC
RUN if [ -f "/app/data/models.dvc" ]; then \
        echo "📌 models.dvc trouvé, récupération avec DVC..."; \
        dvc pull && rm -rf .dvc/tmp; \
    else \
        echo "⚠️ models.dvc non trouvé, aucun modèle récupéré."; \
    fi

# Nettoyer les fichiers temporaires inutiles
RUN rm -rf .dvc/tmp

# Exposer les ports pour Flask et Streamlit
EXPOSE 5000 8501

# Lancer l'API
CMD ["python", "/app/run.py"]
