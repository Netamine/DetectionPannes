import subprocess
import sys

def run_flask():
    """Lancer l'API Flask."""
    subprocess.Popen([sys.executable, "run_flask.py"])

def run_streamlit():
    """Lancer l'application Streamlit."""
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])

if __name__ == '__main__':
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
        print("❌ Arrêt des applications.")