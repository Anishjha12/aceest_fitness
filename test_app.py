import pytest # type: ignore
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_status_endpoint(client):
    """Checks the health status logic from your latest version"""
    res = client.get('/status')
    assert res.status_code == 200
    assert res.json['status'] == "Healthy"

def test_get_members(client):
    """Ensures gym member retrieval works"""
    res = client.get('/members')
    assert res.status_code == 200
    assert isinstance(res.json, list)