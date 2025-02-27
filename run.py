import subprocess
import sys
import os
import signal
import time

# Désactiver certaines optimisations TensorFlow pour éviter des warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Variables globales pour suivre les processus
flask_process = None
streamlit_process = None

def run_flask():
    """Lancer l'application Flask."""
    return subprocess.Popen([sys.executable, "/app/run_flask.py"]) #/app/     #/app/    #/app/


def run_streamlit():
    """Lancer l'application Streamlit."""
    return subprocess.Popen([
        sys.executable, "-m", "streamlit", "run",
        "/app/frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"   #/app/    #/app/    #/app/  #/app/
    ])

def signal_handler(sig, frame):
    """Gérer l'arrêt des processus proprement."""
    print("\n❌ Arrêt des applications en cours...")
    if flask_process:
        flask_process.terminate()
    if streamlit_process:
        streamlit_process.terminate()
    sys.exit(0)

# Associer les signaux d'interruption (CTRL+C, kill)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    print("✅ Lancement de Flask et Streamlit...")

    # Lancer Flask et Streamlit en parallèle
    flask_process = run_flask()
    streamlit_process = run_streamlit()

    if not flask_process:
        print("❌ Flask n'a pas pu démarrer.")
    if not streamlit_process:
        print("❌ Streamlit n'a pas pu démarrer.")

    try:
        while True:
            time.sleep(1)  # Éviter une boucle infinie bloquante
    except KeyboardInterrupt:
        signal_handler(None, None)
