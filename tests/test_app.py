import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("participants" in v for v in data.values())


def test_signup_activity():
    # Use a test email and activity
    email = "testuser@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    url = f"/activities/{activity}/signup?email={email}"
    response = client.post(url)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Try duplicate signup
    response2 = client.post(url)
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"].lower()


def test_unregister_activity():
    email = "testuser@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    url = f"/api/activities/{activity}/unregister"
    response = client.post(url, json={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Try to unregister again (should fail)
    response2 = client.post(url, json={"email": email})
    assert response2.status_code == 400
    assert "not registered" in response2.json()["detail"].lower()
