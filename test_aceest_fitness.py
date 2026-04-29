"""
Unit Tests for ACEest Fitness & Gym Management System
Uses pytest + Flask test client
"""

import pytest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

import ACEest_Fitness as app_module
from ACEest_Fitness import app


# ──────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def reset_data():
    """Reset all in-memory stores and counters before each test."""
    app_module.members.clear()
    app_module.classes.clear()
    app_module.trainers.clear()
    app_module.bookings.clear()
    app_module._member_id_counter = 1
    app_module._class_id_counter = 1
    app_module._trainer_id_counter = 1
    app_module._booking_id_counter = 1
    yield


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def post_json(client, url, data):
    return client.post(url, data=json.dumps(data), content_type="application/json")


def put_json(client, url, data):
    return client.put(url, data=json.dumps(data), content_type="application/json")


# ──────────────────────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────────────────────
class TestHealthCheck:
    def test_health_check_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_health_check_response_fields(self, client):
        data = resp = client.get("/").get_json()
        assert data["status"] == "healthy"
        assert data["app"] == "ACEest Fitness & Gym"
        assert "version" in data
        assert "timestamp" in data


# ──────────────────────────────────────────────────────────────
# Members
# ──────────────────────────────────────────────────────────────
class TestMembers:
    def test_get_members_empty(self, client):
        resp = client.get("/members")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_add_member_success(self, client):
        resp = post_json(client, "/members", {"name": "Alice", "email": "alice@gym.com"})
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "Alice"
        assert data["email"] == "alice@gym.com"
        assert data["id"] == 1
        assert data["membership_type"] == "basic"

    def test_add_member_missing_name(self, client):
        resp = post_json(client, "/members", {"email": "alice@gym.com"})
        assert resp.status_code == 400

    def test_add_member_missing_email(self, client):
        resp = post_json(client, "/members", {"name": "Alice"})
        assert resp.status_code == 400

    def test_add_member_with_premium_type(self, client):
        resp = post_json(client, "/members", {
            "name": "Bob", "email": "bob@gym.com", "membership_type": "premium"
        })
        assert resp.status_code == 201
        assert resp.get_json()["membership_type"] == "premium"

    def test_get_member_by_id(self, client):
        post_json(client, "/members", {"name": "Alice", "email": "alice@gym.com"})
        resp = client.get("/members/1")
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "Alice"

    def test_get_member_not_found(self, client):
        resp = client.get("/members/999")
        assert resp.status_code == 404

    def test_update_member(self, client):
        post_json(client, "/members", {"name": "Alice", "email": "alice@gym.com"})
        resp = put_json(client, "/members/1", {"name": "Alice Updated"})
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "Alice Updated"

    def test_update_member_not_found(self, client):
        resp = put_json(client, "/members/999", {"name": "Nobody"})
        assert resp.status_code == 404

    def test_delete_member(self, client):
        post_json(client, "/members", {"name": "Alice", "email": "alice@gym.com"})
        resp = client.delete("/members/1")
        assert resp.status_code == 200
        assert client.get("/members/1").status_code == 404

    def test_delete_member_not_found(self, client):
        resp = client.delete("/members/999")
        assert resp.status_code == 404

    def test_multiple_members_listed(self, client):
        post_json(client, "/members", {"name": "Alice", "email": "a@gym.com"})
        post_json(client, "/members", {"name": "Bob",   "email": "b@gym.com"})
        resp = client.get("/members")
        assert len(resp.get_json()) == 2


# ──────────────────────────────────────────────────────────────
# Classes
# ──────────────────────────────────────────────────────────────
class TestClasses:
    def test_get_classes_empty(self, client):
        resp = client.get("/classes")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_add_class_success(self, client):
        resp = post_json(client, "/classes", {"name": "Yoga", "schedule": "Mon 9AM"})
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "Yoga"
        assert data["capacity"] == 20
        assert data["enrolled"] == 0

    def test_add_class_missing_name(self, client):
        resp = post_json(client, "/classes", {"schedule": "Mon 9AM"})
        assert resp.status_code == 400

    def test_add_class_missing_schedule(self, client):
        resp = post_json(client, "/classes", {"name": "Yoga"})
        assert resp.status_code == 400

    def test_get_class_by_id(self, client):
        post_json(client, "/classes", {"name": "Yoga", "schedule": "Mon 9AM"})
        resp = client.get("/classes/1")
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "Yoga"

    def test_get_class_not_found(self, client):
        resp = client.get("/classes/999")
        assert resp.status_code == 404


# ──────────────────────────────────────────────────────────────
# Trainers
# ──────────────────────────────────────────────────────────────
class TestTrainers:
    def test_get_trainers_empty(self, client):
        resp = client.get("/trainers")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_add_trainer_success(self, client):
        resp = post_json(client, "/trainers", {"name": "John", "specialization": "Yoga"})
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "John"
        assert data["specialization"] == "Yoga"

    def test_add_trainer_missing_fields(self, client):
        resp = post_json(client, "/trainers", {"name": "John"})
        assert resp.status_code == 400


# ──────────────────────────────────────────────────────────────
# Bookings
# ──────────────────────────────────────────────────────────────
class TestBookings:
    def _add_member_and_class(self, client, capacity=5):
        post_json(client, "/members", {"name": "Alice", "email": "alice@gym.com"})
        post_json(client, "/classes", {"name": "Yoga", "schedule": "Mon 9AM", "capacity": capacity})

    def test_create_booking_success(self, client):
        self._add_member_and_class(client)
        resp = post_json(client, "/bookings", {"member_id": 1, "class_id": 1})
        assert resp.status_code == 201
        assert resp.get_json()["status"] == "confirmed"

    def test_booking_increments_enrolled(self, client):
        self._add_member_and_class(client)
        post_json(client, "/bookings", {"member_id": 1, "class_id": 1})
        assert client.get("/classes/1").get_json()["enrolled"] == 1

    def test_booking_invalid_member(self, client):
        post_json(client, "/classes", {"name": "Yoga", "schedule": "Mon 9AM"})
        resp = post_json(client, "/bookings", {"member_id": 999, "class_id": 1})
        assert resp.status_code == 404

    def test_booking_invalid_class(self, client):
        post_json(client, "/members", {"name": "Alice", "email": "alice@gym.com"})
        resp = post_json(client, "/bookings", {"member_id": 1, "class_id": 999})
        assert resp.status_code == 404

    def test_booking_class_full(self, client):
        self._add_member_and_class(client, capacity=1)
        post_json(client, "/bookings", {"member_id": 1, "class_id": 1})
        # Second member
        post_json(client, "/members", {"name": "Bob", "email": "bob@gym.com"})
        resp = post_json(client, "/bookings", {"member_id": 2, "class_id": 1})
        assert resp.status_code == 409

    def test_cancel_booking(self, client):
        self._add_member_and_class(client)
        post_json(client, "/bookings", {"member_id": 1, "class_id": 1})
        resp = client.delete("/bookings/1")
        assert resp.status_code == 200
        # Enrolled count decremented
        assert client.get("/classes/1").get_json()["enrolled"] == 0

    def test_cancel_booking_not_found(self, client):
        resp = client.delete("/bookings/999")
        assert resp.status_code == 404

    def test_get_all_bookings(self, client):
        self._add_member_and_class(client)
        post_json(client, "/bookings", {"member_id": 1, "class_id": 1})
        resp = client.get("/bookings")
        assert len(resp.get_json()) == 1
