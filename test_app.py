import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """The 'Quality Gate' test for the pipeline"""
    response = client.get('/status')
    assert response.status_code == 200
    assert response.json['status'] == "Healthy"

def test_members_api(client):
    response = client.get('/members')
    assert response.status_code == 200
    assert isinstance(response.json, list)