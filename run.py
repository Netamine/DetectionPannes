import subprocess
import sys
import mlflow
import os
from run_flask import app  # Importation de l'application Flask

# Désactive certaines optimisations TensorFlow pour éviter des warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Configurer MLflow pour utiliser le répertoire local 'mlruns'
mlflow.set_tracking_uri("mlruns")
mlflow.set_experiment("web_app_experiment")


def run_streamlit():
    """Lancer l'application Streamlit."""
    return subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])


if __name__ == '__main__':
    with mlflow.start_run():
        mlflow.log_param("service", "Flask + Streamlit")

        print("✅ Lancement de Flask et Streamlit...")

        # Lancer Flask en arrière-plan seulement si on est en local
        if "RENDER" not in os.environ:
            flask_process = subprocess.Popen([sys.executable, "run_flask.py"])
            streamlit_process = run_streamlit()

            try:
                while True:
                    pass  # Maintenir le processus principal actif
            except KeyboardInterrupt:
                print("\n❌ Arrêt des applications.")
                flask_process.terminate()  # Arrêter Flask proprement
                streamlit_process.terminate()  # Arrêter Streamlit proprement
                mlflow.end_run()
        else:
            # Si on est sur Render, on lance directement Flask ici
            app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
