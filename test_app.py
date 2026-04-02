import pytest
from app import app, init_db

@pytest.fixture
def client():
    init_db() # Setup database before tests
    with app.test_client() as client:
        yield client

def test_status_endpoint(client):
    res = client.get('/status')
    assert res.status_code == 200
    assert res.json['status'] == "Healthy"

def test_members_list(client):
    res = client.get('/members')
    assert res.status_code == 200
    assert len(res.json) > 0