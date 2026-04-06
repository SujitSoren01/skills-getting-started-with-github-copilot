import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # (No setup needed for in-memory activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "student1@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity_name]["participants"]

def test_prevent_duplicate_signup():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "student2@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

def test_unregister_participant():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "student3@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]

def test_signup_nonexistent_activity():
    # Arrange
    activity_name = "nonexistent"
    email = "student4@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
