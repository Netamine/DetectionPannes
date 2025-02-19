# Utiliser la dernière version de Python 3.13
FROM python:3.13-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires à PostgreSQL et MLflow
RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev

# Installer psycopg2-binary en premier pour éviter les conflits
RUN pip install --no-cache-dir psycopg2-binary

# Installer MLflow
RUN pip install --no-cache-dir mlflow

# Créer un répertoire pour stocker les artefacts MLflow
RUN mkdir -p /mlflow/artifacts

# Exposer le port sur lequel MLflow va tourner
EXPOSE 5000

# Lancer le serveur MLflow
CMD ["mlflow", "server", "--backend-store-uri", "postgresql://mlflow:password@postgres/mlflow", "--default-artifact-root", "/mlflow/artifacts", "--host", "0.0.0.0"]
