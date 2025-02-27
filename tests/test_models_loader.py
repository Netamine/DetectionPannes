import os
import pytest
from backend.utils.models_loader import load_models

@pytest.fixture
def model_dir():
    """Fixture pour définir le chemin du répertoire de modèles."""
    return "data/models"

def test_load_models(model_dir):
    """Test de chargement des modèles depuis le dossier des modèles."""
    os.makedirs(model_dir, exist_ok=True)
    assert os.path.exists(model_dir), f"Le dossier {model_dir} n'existe pas."

    models = load_models(model_dir)
    assert isinstance(models, dict), "Le retour doit être un dictionnaire"
