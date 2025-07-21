from fastapi.testclient import TestClient
from main import app
from database import get_db, SessionLocal
import pytest
import os
import random
import string

client = TestClient(app)

# Set a dummy secret key for testing
os.environ["SECRET_KEY"] = "test_secret_key"

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def test_create_user(db):
    username = f"testuser_{random_string()}"
    response = client.post(
        "/users/",
        json={"username": username, "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert "id" in data

def test_login(db):
    username = f"testuser_{random_string()}"
    # First, create a user
    client.post(
        "/users/",
        json={"username": username, "password": "testpassword2"},
    )

    response = client.post(
        "/token",
        data={"username": username, "password": "testpassword2"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_read_main():
    response = client.get("/users/me/")
    assert response.status_code == 401  # Unauthorized
