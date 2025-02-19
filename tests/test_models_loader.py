import pytest
import os
from backend.models_loader import load_models

def test_load_models():
    model_dir = "backend/models"  # Assure-toi que le dossier existe
    assert os.path.exists(model_dir), f"Le dossier {model_dir} n'existe pas."

    models = load_models(model_dir=model_dir)  # Passage du bon argument
    assert isinstance(models, dict), "Le retour doit être un dictionnaire"
    assert len(models) > 0, "Aucun modèle n'a été chargé"
    assert "TP2" in models, "Le modèle TP2 n'est pas chargé"
