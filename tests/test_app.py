import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data
    assert "participants" in data["Soccer Team"]

def test_signup_for_activity():
    # Use a unique email to avoid duplicate error
    test_email = "pytestuser@mergington.edu"
    response = client.post(f"/activities/Soccer%20Team/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email} for Soccer Team" in response.json().get("message", "")
    # Try to sign up again, should fail
    response2 = client.post(f"/activities/Soccer%20Team/signup?email={test_email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json().get("detail", "")

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
