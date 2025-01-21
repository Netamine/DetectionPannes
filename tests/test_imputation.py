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
    #assert b"API is running!" in response.data
    assert b"L'API fonctionne et les mod\xc3\xa8les sont charg\xc3\xa9s !" in response.data

def test_impute_no_file(client):
    response = client.post('/impute')
    assert response.status_code == 400
    #assert "Aucun fichier n'a été envoyé." in response.data.decode('utf-8')
    # Charger la réponse JSON et vérifier le contenu du message d'erreur
    response_json = response.get_json()
    assert response_json["error"] == "Aucun fichier n'a été envoyé."