import subprocess
import sys
import mlflow

# Configurer MLflow pour utiliser le répertoire local 'mlruns'
mlflow.set_tracking_uri("mlruns")
mlflow.set_experiment("web_app_experiment")



def run_flask():
    """Lancer l'API Flask."""
    subprocess.Popen([sys.executable, "run_flask.py"])


def run_streamlit():
    """Lancer l'application Streamlit."""
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])


if __name__ == '__main__':
    # Début de la session MLflow
    with mlflow.start_run():
        # Enregistrer les paramètres de l'application (exemple)
        mlflow.log_param("service", "Flask + Streamlit")

        # Lancer Flask
        run_flask()

        # Lancer Streamlit
        run_streamlit()

        # Garder le script actif
        print("✅ Flask et Streamlit sont lancés. Appuyez sur CTRL+C pour quitter.")
        try:
            while True:
                pass  # Garder le processus principal actif pour les sous-processus
        except KeyboardInterrupt:
            print("\n❌ Arrêt des applications.")
            mlflow.end_run()  # Assurer la fin propre de la session MLflow
