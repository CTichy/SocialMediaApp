import os
import pytest
from fastapi.testclient import TestClient
from src.api import app
from src.db import Database

# Set up the FastAPI TestClient
client = TestClient(app)

# Fixture to wipe the database before each test
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    db = Database()
    db.wipe_database()  # Clean up database before each test
    yield
    db.close()


def test_register_user():
    response = client.post(
        "/users/register/",
        data={"username": "testuser", "email": "testuser@example.com", "password": "securepassword"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}


def test_register_duplicate_user():
    # Register the same user twice
    client.post(
        "/users/register/",
        data={"username": "testuser", "email": "testuser@example.com", "password": "securepassword"},
    )
    response = client.post(
        "/users/register/",
        data={"username": "testuser", "email": "testuser@example.com", "password": "securepassword"},
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_login_user():
    # Register a user first
    client.post(
        "/users/register/",
        data={"username": "testuser", "email": "testuser@example.com", "password": "securepassword"},
    )

    # Login with the same user
    response = client.post(
        "/users/login/",
        data={"username": "testuser", "password": "securepassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_user_details():
    # Register a user first
    client.post(
        "/users/register/",
        data={"username": "testuser", "email": "testuser@example.com", "password": "securepassword"},
    )

    # Get user details
    response = client.get("/users/testuser/")
    assert response.status_code == 200
    assert response.json() == {
        "username": "testuser",
        "email": "testuser@example.com",
    }
