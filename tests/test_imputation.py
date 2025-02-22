import pytest
import json
from backend import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

    # ✅ Correction : Extraire proprement le JSON et vérifier le message
    response_json = response.get_json()
    assert response_json["message"] == "L'API fonctionne et les modèles sont chargés !"


def test_impute_no_file(client):
    response = client.post('/impute')
    assert response.status_code == 400

    # Vérification du contenu JSON
    response_json = response.get_json()
    assert response_json["error"] == "Aucun fichier n'a été envoyé."
