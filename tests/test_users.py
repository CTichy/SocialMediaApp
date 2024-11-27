import pytest
from fastapi.testclient import TestClient
from src.api import app
from src.db import Database

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    db = Database()
    db.wipe_database()
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
    client.post(
        "/users/register/",
        data={"username": "testuser", "email": "testuser@example.com", "password": "securepassword"},
    )
    response = client.post(
        "/users/login/",
        data={"username": "testuser", "password": "securepassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_user_details():
    client.post(
        "/users/register/",
        data={"username": "testuser", "email": "testuser@example.com", "password": "securepassword"},
    )
    response = client.get("/users/testuser/")
    assert response.status_code == 200
    assert response.json() == {
        "username": "testuser",
        "email": "testuser@example.com",
    }


def test_get_non_existent_user():
    response = client.get("/users/nonexistentuser/")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
