import subprocess
import sys
import mlflow
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Configurer MLflow pour utiliser le répertoire local 'mlruns'
mlflow.set_tracking_uri("mlruns")
mlflow.set_experiment("web_app_experiment")

def run_flask():
    """Lancer l'API Flask."""
    return subprocess.Popen([sys.executable, "run_flask.py"])

def run_streamlit():
    """Lancer l'application Streamlit."""
    return subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])

if __name__ == '__main__':
    with mlflow.start_run():
        mlflow.log_param("service", "Flask + Streamlit")

        # Lancer Flask et Streamlit en arrière-plan
        flask_process = run_flask()
        streamlit_process = run_streamlit()

        print("✅ Flask et Streamlit sont lancés. Appuyez sur CTRL+C pour quitter.")

        try:
            while True:
                pass  # Maintenir le processus principal actif
        except KeyboardInterrupt:
            print("\n❌ Arrêt des applications.")
            flask_process.terminate()  # Arrêter Flask proprement
            streamlit_process.terminate()  # Arrêter Streamlit proprement
            mlflow.end_run()
