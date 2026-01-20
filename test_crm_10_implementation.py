import pytest
from fastapi.testclient import TestClient
from crm_10_implementation import app, LoginRequest, TokenResponse, UserRepository
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import bcrypt
import jwt
import datetime
import os
from dotenv import load_dotenv
import pytest_asyncio
from typing import Optional, Dict, Any

load_dotenv()

@pytest_asyncio.fixture
def client():
    app.dependency_overrides = {}
    with TestClient(app) as client:
        yield client

@pytest_asyncio.fixture
def user_repository():
    return UserRepository()

def test_user_repository_get_user_by_username():
    """
    Test the get_user_by_username method of UserRepository.
    """
    user_repo = UserRepository()
    user = user_repo.get_user_by_username("user1")
    assert user is not None
    assert user["username"] == "user1"
    assert "hashed_password" in user

def test_user_repository_get_user_by_username_not_found():
    """
    Test the get_user_by_username method when the user is not found.
    """
    user_repo = UserRepository()
    user = user_repo.get_user_by_username("nonexistent_user")
    assert user is None

def test_user_repository_authenticate_user_success():
    """
    Test the authenticate_user method with valid credentials.
    """
    user_repo = UserRepository()
    user = user_repo.authenticate_user("user1", "password1")
    assert user is not None
    assert user["username"] == "user1"

def test_user_repository_authenticate_user_invalid_password():
    """
    Test the authenticate_user method with invalid password.
    """
    user_repo = UserRepository()
    user = user_repo.authenticate_user("user1", "wrong_password")
    assert user is None

def test_user_repository_authenticate_user_nonexistent_user():
    """
    Test the authenticate_user method with non-existent user.
    """
    user_repo = UserRepository()
    user = user_repo.authenticate_user("nonexistent_user", "password")
    assert user is None

def test_create_access_token():
    """
    Test the create_access_token function with default expiration.
    """
    data = {"sub": "test_user"}
    token = create_access_token(data)
    assert isinstance(token, str)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "test_user"
    assert "exp" in decoded

def test_create_access_token_with_custom_expiration():
    """
    Test the create_access_token function with custom expiration.
    """
    data = {"sub": "test_user"}
    expires_delta = datetime.timedelta(minutes=60)
    token = create_access_token(data, expires_delta)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "test_user"
    assert "exp" in decoded

def test_login_for_access_token_success(client):
    """
    Test the login endpoint with valid credentials.
    """
    response = client.post("/login", json={"username": "user1", "password": "password1"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_for_access_token_invalid_credentials(client):
    """
    Test the login endpoint with invalid credentials.
    """
    response = client.post("/login", json={"username": "user1", "password": "wrong_password"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_for_access_token_nonexistent_user(client):
    """
    Test the login endpoint with non-existent user.
    """
    response = client.post("/login", json={"username": "nonexistent_user", "password": "password"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_for_access_token_missing_username(client):
    """
    Test the login endpoint with missing username.
    """
    response = client.post("/login", json={"password": "password1"})
    assert response.status_code == 422

def test_login_for_access_token_missing_password(client):
    """
    Test the login endpoint with missing password.
    """
    response = client.post("/login", json={"username": "user1"})
    assert response.status_code == 422