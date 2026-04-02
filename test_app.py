import pytest
from app import app, init_db

@pytest.fixture
def client():
    # Force database initialization before ANY test runs
    init_db() 
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """The 'Quality Gate' test for the pipeline"""
    response = client.get('/status')
    assert response.status_code == 200
    assert response.json['status'] == "Healthy"

def test_members_api(client):
    # Now the table is guaranteed to exist
    response = client.get('/members')
    assert response.status_code == 200