import pytest
from fastapi.testclient import TestClient
from crm_13_implementation import app, UserLoginRequest, UserLoginResponse, AuthException, get_user_repository
from unittest.mock import patch, MagicMock
import bcrypt
import jwt
import datetime
from uuid import uuid4
from enum import Enum
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Fixture for test client
@pytest.fixture
def client():
    return TestClient(app)

# Fixture for user repository
@pytest.fixture
def user_repo():
    repo = UserRepository()
    yield repo
    repo.users.clear()

# Fixture for mock bcrypt
@pytest.fixture
def mock_bcrypt():
    with patch('bcrypt.hashpw') as mock_hashpw, \
         patch('bcrypt.checkpw') as mock_checkpw:
        yield mock_hashpw, mock_checkpw

# Fixture for mock jwt
@pytest.fixture
def mock_jwt():
    with patch('jwt.decode') as mock_decode, \
         patch('jwt.encode') as mock_encode, \
         patch('jwt.get_signature_algorithm') as mock_get_algorithm:
        yield mock_decode, mock_encode, mock_get_algorithm

# Fixture for mock datetime
@pytest.fixture
def mock_datetime():
    with patch('datetime.datetime') as mock_datetime:
        yield mock_datetime

# Test UserRepository class
def test_user_repository_create_user_success(user_repo):
    """Test successful user creation"""
    user_data = {
        "username": "testuser",
        "password": "securepassword123"
    }
    result = user_repo.create_user(user_data)
    assert "id" in result
    assert "created_at" in result
    assert result["username"] == "testuser"
    assert bcrypt.hashpw in user_repo.create_user

def test_user_repository_create_user_username_exists(user_repo):
    """Test user creation when username already exists"""
    user_repo.create_user({
        "username": "testuser",
        "password": "securepassword123"
    })
    with pytest.raises(ValueError, match="Username already exists"):
        user_repo.create_user({
            "username": "testuser",
            "password": "anotherpassword"
        })

def test_user_repository_create_user_missing_fields(user_repo):
    """Test user creation with missing required fields"""
    with pytest.raises(ValueError, match="Username and password are required"):
        user_repo.create_user({
            "username": "testuser"
        })

def test_user_repository_get_user_by_username_found(user_repo):
    """Test retrieving user by username when found"""
    user_repo.create_user({
        "username": "testuser",
        "password": "securepassword123"
    })
    result = user_repo.get_user_by_username("testuser")
    assert result["username"] == "testuser"

def test_user_repository_get_user_by_username_not_found(user_repo):
    """Test retrieving user by username when not found"""
    result = user_repo.get_user_by