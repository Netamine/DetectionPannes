import os
import pytest
from backend.utils.models_loader import load_models

def test_load_models():
    model_dir = "data/models"  # ✅ Correction du chemin
    os.makedirs(model_dir, exist_ok=True)  # ✅ Création du dossier si inexistant

    assert os.path.exists(model_dir), f"Le dossier {model_dir} n'existe pas."

    models = load_models(model_dir)
    assert isinstance(models, dict), "Le retour doit être un dictionnaire"

