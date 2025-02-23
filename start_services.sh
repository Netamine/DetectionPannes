#!/bin/sh

set -e  # Arrêter le script en cas d'erreur

echo "📌 Mise à jour des modèles avec DVC..."
dvc pull || { echo "⚠️ Erreur lors de la mise à jour des modèles avec DVC"; exit 1; }

echo "✅ Démarrage de Prometheus..."
/prometheus/prometheus --config.file=/monitoring/prometheus.yml &

echo "✅ Démarrage de Grafana..."
/grafana/bin/grafana-server --homepath=/grafana --config /grafana/conf/grafana.ini &

echo "✅ Démarrage de Flask..."
python /app/run_flask.py &

echo "✅ Démarrage de Streamlit..."
streamlit run /app/frontend/app.py --server.port=8501 --server.address=0.0.0.0 &

# Garder le conteneur actif et surveiller les processus
wait
