import pytest # type: ignore
from app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_api_status(client):
    """Test if the DevOps health check endpoint works"""
    res = client.get('/status')
    assert res.status_code == 200
    assert res.json['status'] == "Healthy"

def test_members_list(client):
    """Test if database retrieval works"""
    res = client.get('/members')
    assert res.status_code == 200
    assert len(res.json) > 0