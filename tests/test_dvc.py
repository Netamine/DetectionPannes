import os
import pytest
import subprocess
import os
import pytest
import subprocess
import joblib
import tensorflow as tf

MODEL_DIR = "data/models"

def test_dvc_installed():
    """Vérifie que DVC est installé et accessible."""
    result = subprocess.run(["dvc", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, f"DVC n'est pas installé ou ne fonctionne pas : {result.stderr}"

def test_dvc_directory_exists():
    """Vérifie que le dossier .dvc existe."""
    assert os.path.isdir(".dvc"), "Le dossier .dvc est manquant, DVC n'a peut-être pas été initialisé."

def test_dvc_files_exist():
    """Vérifie que les fichiers de configuration DVC existent."""
    assert os.path.isfile("dvc.yaml"), "Le fichier dvc.yaml est manquant."
    assert os.path.isfile("data/models.dvc"), "Le fichier models.dvc est manquant."

def test_dvc_status():
    """Exécute `dvc status` et vérifie qu'il n'y a pas de problème."""
    result = subprocess.run(["dvc", "status"], capture_output=True, text=True)
    print(f"🔍 Résultat de `dvc status` :\n{result.stdout}")  # Debugging

    assert result.returncode == 0, "DVC status a retourné une erreur."
    assert "not tracked" not in result.stdout.lower(), "Certains fichiers ne sont pas suivis par DVC."


def test_dvc_pull():
    """Vérifie que `dvc pull` récupère les modèles correctement."""
    result = subprocess.run(["dvc", "pull"], capture_output=True, text=True)
    print(f"🔍 Résultat de `dvc pull` :\n{result.stdout}")  # Debugging

    assert result.returncode == 0, f"DVC pull a échoué : {result.stderr}"
    assert "error" not in result.stderr.lower(), "Erreur détectée lors du `dvc pull`."


def test_model_files_exist():
    """Vérifie que tous les modèles sont présents après `dvc pull`."""
    expected_models = [
        "Caudal_impulses.pkl", "COMP.pkl", "DV_eletric.pkl", "DV_pressure.pkl",
        "H1.pkl", "LPS.pkl", "Motor_current.pkl", "MPG.pkl",
        "Oil_level.pkl", "Oil_temperature.pkl", "Pressure_switch.pkl",
        "Reservoirs.pkl", "Towers.pkl", "TP2.pkl", "TP3.pkl",
        "sae_trained.keras", "scaler.pkl", "threshold_final.pkl"
    ]

    missing_files = [model for model in expected_models if not os.path.isfile(os.path.join(MODEL_DIR, model))]

    assert not missing_files, f"Les fichiers suivants sont manquants : {missing_files}"


def test_load_models():
    """Vérifie que tous les modèles peuvent être chargés sans erreur."""
    for model_file in os.listdir(MODEL_DIR):
        model_path = os.path.join(MODEL_DIR, model_file)

        if model_file.endswith(".pkl"):
            try:
                model = joblib.load(model_path)
                assert model is not None, f"Le modèle {model_file} est corrompu."
            except Exception as e:
                pytest.fail(f"Impossible de charger {model_file} : {e}")

        elif model_file.endswith(".keras"):
            try:
                model = tf.keras.models.load_model(model_path)
                assert model is not None, f"Le modèle {model_file} est corrompu."
            except Exception as e:
                pytest.fail(f"Impossible de charger {model_file} : {e}")