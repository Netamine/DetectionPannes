# Utiliser une image légère de Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Désactiver CUDA (si besoin)
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

# Assurer que Flasgger (Swagger pour Flask) est bien installé
RUN pip install --no-cache-dir flasgger

# Copier `run.py`
COPY run.py /app/run.py

# Copier la clé d'authentification Google Drive
COPY keys/CleDVCJason.json /root/.config/dvc/CleDVCJason.json

# Copier uniquement le backend dans `/app/backend`
COPY backend /app/backend

# Copier uniquement le frontend dans `/app/frontend`
COPY frontend /app/frontend

# Définir la variable d’environnement pour DVC
ENV GDRIVE_CREDENTIALS_DATA="/root/.config/dvc/CleDVCJason.json"

# Initialiser DVC et configurer le remote Google Drive
RUN dvc init --no-scm && \
    dvc remote add -d dvc_data gdrive://1G3bpMF46owL-_Z1mnEtmrJ_61nWQlRfO && \
    dvc remote modify dvc_data gdrive_use_service_account true && \
    dvc remote modify dvc_data gdrive_service_account_json_file_path /root/.config/dvc/CleDVCJason.json

# Vérifier si les modèles existent, sinon les récupérer
RUN if [ ! -d "data/models" ] || [ -z "$(ls -A data/models)" ]; then \
        echo "📌 Modèles absents, récupération avec DVC..."; \
        dvc pull && rm -rf .dvc/tmp; \
    else \
        echo "✅ Modèles déjà présents, pas de récupération nécessaire."; \
    fi

# Nettoyer les fichiers temporaires inutiles
RUN rm -rf .dvc/tmp

# Exposer les ports pour Flask et Streamlit
EXPOSE 5000 8501

# Lancer le script de démarrage
CMD ["python", "/app/run.py"]
