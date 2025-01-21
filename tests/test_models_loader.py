import pytest
from backend.models_loader import load_models

def test_load_models():
    models = load_models()
    assert isinstance(models, dict)
    assert len(models) > 0  # Vérifie si au moins un modèle est chargé
    assert "TP2" in models  # Vérifie qu'un modèle spécifique est chargé
