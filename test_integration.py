import pytest
import httpx
from fastapi.testclient import TestClient
from crm_10_implementation import app
from datetime import datetime, timedelta
import os
import jwt
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

# Fixtures
@pytest.fixture(scope="module")
def test_app():
    """Fixture to create a test FastAPI app instance"""
    return app

@pytest.fixture(scope="module")
def client(test_app):
    """Fixture to create a TestClient for the app"""
    return TestClient(test_app)

@pytest.fixture(scope="module")
def auth_token(client):
    """Fixture to generate an authentication token for testing"""
    # Create a test user
    test_user = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Register the user (simulated)
    register_response = client.post("/register", json=test_user)
    assert register_response.status_code == 201, "User registration failed"

    # Login to get the token
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, "Login failed"

    return login_response.json()["access_token"]

@pytest.fixture(scope="module")
def headers(client, auth_token):
    """Fixture to provide authentication headers for protected endpoints"""
    return {"Authorization": f"Bearer {auth_token}"}

# Test cases
def test_user_registration(client):
    """Test user registration endpoint"""
    test_user = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/register", json=test_user)
    assert response.status_code == 201
    assert "user_id" in response.json()
    assert "username" in response.json()
    assert "created_at" in response.json()

def test_user_login(client):
    """Test user login endpoint"""
    test_user = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/login", data=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()

def test_protected_endpoint(client, headers):
    """Test access to a protected endpoint"""
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "This is a protected endpoint"

def test_token_expiration(client):
    """Test token expiration and refresh"""
    test_user = {
        "username": "testuser",
        "password": "testpassword"
    }
    # Register user
    register_response = client.post("/register", json=test_user)
    assert register_response.status_code == 201

    # Login to get initial token
    login_response = client.post("/login", data=test_user)
    assert login_response.status_code == 200
    initial_token = login_response.json()["access_token"]

    # Check initial token expiration
    decoded_initial = jwt.decode(
        initial_token,
        os.getenv("SECRET_KEY"),
        algorithms=["HS256"],
        options={"verify_exp": False}
    )
    initial_exp = decoded_initial["exp"]
    current_time = datetime.now().timestamp()
    assert initial_exp - current_time < 1800  # Token should expire in 30 minutes

    # Wait for token to expire (simulate)
    import time
    time.sleep(180)  # Sleep for 3 minutes to ensure token is expired

    # Try to access protected endpoint with expired token
    response = client.get("/protected", headers={"Authorization": f"Bearer {initial_token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Token has expired"

def test_token_renewal(client, headers):
    """Test token renewal after expiration"""
    # Get initial token
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    initial_token = headers["Authorization"].split(" ")[1]

    # Wait for token to expire (simulate)
    import time
    time.sleep(180)  # Sleep for 3 minutes to ensure token is expired

    # Try to access protected endpoint with expired token
    response = client.get("/protected", headers={"Authorization": f"Bearer {initial_token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Token has expired"

    # Renew token
    renewal_response = client.post("/renew_token", headers=headers)
    assert renewal_response.status_code == 200
    new_token = renewal_response.json()["access_token"]

    # Access protected endpoint with new token
    response = client.get("/protected", headers={"Authorization": f"Bearer {new_token}"})
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "This is a protected endpoint"

def test_invalid_credentials(client):
    """Test login with invalid credentials"""
    test_user = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/login", data=test_user)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_missing_credentials(client):
    """Test login with missing credentials"""
    response = client.post("/login", data={"username": "testuser"})
    assert response.status_code == 422
    assert "password" in response.json()["detail"]

def test_token_revocation(client, headers):
    """Test token revocation"""
    # Get initial token
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    initial_token = headers["Authorization"].split(" ")[1]

    # Revocate token
    revocation_response = client.post("/revoke_token", headers=headers)
    assert revocation_response.status_code == 200
    assert revocation_response.json()["message"] == "Token revoked successfully"

    # Try to access protected endpoint with revoked token
    response = client.get("/protected", headers={"Authorization": f"Bearer {initial_token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Token has been revoked"

def test_token_blacklist_check(client, headers):
    """Test token blacklist check"""
    # Get initial token
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    initial_token = headers["Authorization"].split(" ")[1]

    # Check if token is in blacklist
    blacklist_response = client.get("/check_blacklist", headers={"Authorization": f"Bearer {initial_token}"})
    assert blacklist_response.status_code == 200
    assert blacklist_response.json()["in_blacklist"] is True

def test_token_blacklist_check_after_revoke(client, headers):
    """Test token blacklist check after revocation"""
    # Get initial token
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    initial_token = headers["Authorization"].split(" ")[1]

    # Revocate token
    revocation_response = client.post("/revoke_token", headers=headers)
    assert revocation_response.status