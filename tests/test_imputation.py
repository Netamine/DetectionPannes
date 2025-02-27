import pytest
from backend import create_app

@pytest.fixture
def client():
    """Créer un client Flask pour les tests."""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_home(client):
    """Test que l'API répond correctement sur la route /."""
    response = client.get('/')
    print(f"🔍 Réponse brute de l'API : {response.data.decode()}")  # Debug

    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json is not None, "L'API ne retourne pas de JSON valide."
    assert "message" in response_json, "La clé 'message' est absente de la réponse."
    assert response_json["message"] == "L'API fonctionne et les modèles sont chargés !"


def test_impute_no_file(client):
    """Test que l'API retourne une erreur lorsqu'aucun fichier n'est envoyé."""
    response = client.post('/impute')
    assert response.status_code == 400
    response_json = response.get_json()
    assert "error" in response_json
    assert response_json["error"] == "Aucun fichier n'a été envoyé."
