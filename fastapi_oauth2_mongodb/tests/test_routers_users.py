import pymongo
import pytest
from fastapi.testclient import TestClient
from fastapi_oauth2_mongodb import fastapi_oauth2_mongodb


@pytest.fixture(scope="module")
def client():
    with TestClient(fastapi_oauth2_mongodb.app) as client:
        yield client


@pytest.fixture(scope="module")
def register_data():
    return {
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com",
    }


def delete_testuser():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["falra_db"]
    collection = db["users"]
    collection.delete_one({"username": "testuser"})


def test_register_success(client, register_data):
    delete_testuser()
    response = client.post("/api/users/v1/register", json=register_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Registration success."


def test_register_user_exists(client, register_data):
    # register user once
    client.post("/api/users/v1/register", json=register_data)
    # try to register same user again
    response = client.post("/api/users/v1/register", json=register_data)
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["message"] == "Registration failed, user existed."


@pytest.fixture(scope="module")
def login_data():
    return {
        "username": "testuser",
        "password": "testpassword",
        "grant_type": "password",
    }


def test_login_success(client, register_data, login_data):
    # register user
    client.post("/api/users/v1/register", json=register_data)
    # login
    response = client.post("/api/users/v1/login", data=login_data)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "token" in response.json()


def test_login_invalid_username(client, register_data, login_data):
    # register user
    client.post("/api/users/v1/register", json=register_data)
    # try to login with invalid username
    login_data["username"] = "invalid_username"
    response = client.post("/api/users/v1/login", data=login_data)
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["message"] == "Login failed."


def test_login_invalid_password(client, register_data, login_data):
    # register user
    client.post("/api/users/v1/register", json=register_data)
    # try to login with invalid password
    login_data["password"] = "invalid_password"
    response = client.post("/api/users/v1/login", data=login_data)
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["message"] == "Login failed."
