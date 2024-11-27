import os
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


def test_create_post():
    """Test creating a new post."""
    with open("sample_image.jpg", "wb") as f:
        f.write(os.urandom(1024))  # Create a dummy image file

    with open("sample_image.jpg", "rb") as image_file:
        response = client.post(
            "/posts/",
            files={"image": image_file},
            data={"text": "This is a test post", "user": "testuser"},
        )

    os.remove("sample_image.jpg")  # Cleanup dummy file

    assert response.status_code == 200
    assert response.json() == {"message": "Post created successfully"}


def test_get_latest_post():
    """Test retrieving the latest post."""
    with open("sample_image.jpg", "wb") as f:
        f.write(os.urandom(1024))  # Create a dummy image file

    with open("sample_image.jpg", "rb") as image_file:
        client.post(
            "/posts/",
            files={"image": image_file},
            data={"text": "This is the latest post", "user": "testuser"},
        )

    os.remove("sample_image.jpg")  # Cleanup dummy file

    response = client.get("/posts/latest/")
    assert response.status_code == 200
    assert "image" in response.json()
    assert "text" in response.json()
    assert "user" in response.json()
    assert response.json()["text"] == "This is the latest post"


def test_create_post_no_image():
    response = client.post(
        "/posts/",
        data={"text": "Test post without image", "user": "testuser"}
    )
    assert response.status_code == 422  # FastAPI automatically checks for required fields

def test_create_post_large_image():
    # Simulate a large image
    large_image_path = "tests/large_image.jpg"
    with open(large_image_path, "wb") as f:
        f.write(b"x" * 1024 * 1024 * 10)  # Create a 10MB file

    with open(large_image_path, "rb") as large_image:
        response = client.post(
            "/posts/",
            files={"image": ("large_image.jpg", large_image, "image/jpeg")},
            data={"text": "Test post with large image", "user": "testuser"}
        )
    assert response.status_code == 200  # Expect success
    assert response.json()["message"] == "Post created successfully"
