from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, Dict, Any
import bcrypt
import jwt
import datetime
from uuid import uuid4
from enum import Enum

# ==============================
# Data Access Layer
# ==============================
class UserRepository:
    """
    Repository pattern implementation for user data access.
    Handles database interactions for user management.
    """
    
    def __init__(self):
        """Initialize in-memory user storage"""
        self.users: Dict[str, Dict[str, Any]] = {}
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user by username.
        
        Args:
            username: User identifier
            
        Returns:
            User data if found, None otherwise
        """
        return self.users.get(username)
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user with secure password handling.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            Created user data
            
        Raises:
            ValueError: If username already exists or invalid data
        """
        if not user_data.get("username") or not user_data.get("password"):
            raise ValueError("Username and password are required")
            
        if self.get_user_by_username(user_data["username"]):
            raise ValueError("Username already exists")
            
        # Hash password using bcrypt
        hashed_password = bcrypt.hashpw(
            user_data["password"].encode("utf-8"),
            bcrypt.gensalt()
        )
        
        user_data["password"] = hashed_password.decode("utf-8")
        user_data["id"] = str(uuid4())
        user_data["created_at"] = datetime.datetime.now().isoformat()
        
        self.users[user_data["username"]] = user_data
        return user_data

# ==============================
# API Layer
# ==============================
class UserLoginRequest(BaseModel):
    """
    Request model for user login.
    """
    username: str
    password: str

class UserLoginResponse(BaseModel):
    """
    Response model for user login.
    """
    token: str
    username: str
    expires_in: int

class AuthException(Exception):
    """Custom exception for authentication errors"""
    pass

class TokenType(Enum):
    """Token types for JWT authentication"""
    ACCESS = "access"
    REFRESH = "refresh"

def get_user_repository():
    """Dependency injector for user repository"""
    return UserRepository()

def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
    """
    Dependency to get current user from JWT token.
    
    Args:
        token: JWT token from authentication
        
    Returns:
        User data from token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            "SECRET_KEY",  # In production, use environment variable
            algorithms=["HS256"],
            options={"require_exp": True}
        )
        username = payload.get("sub")
        if not username:
            raise AuthException("Invalid token")
            
        user_repo = get_user_repository()
        user = user_repo.get_user_by_username(username)
        if not user:
            raise AuthException("User not found")
            
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """
    Authenticate user with provided credentials.
    
    Args:
        username: User identifier
        password: User password
        
    Returns:
        User data if authentication succeeds
        
    Raises:
        HTTPException: If authentication fails
    """
    user_repo = get_user_repository()
    user = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
        
    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
        
    return user

def create_access_token(data: Dict[str, Any], expires_delta: datetime.timedelta) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in token
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        "SECRET_KEY",  # In production, use environment variable
        algorithm="HS256"
    )
    return encoded_jwt

# ==============================
# Main Application
# ==============================
app = FastAPI(
    title="Telco Authentication Service",
    version="1.0.0"
)

# Dependency for secure token generation
def get_token_type() -> TokenType:
    """Dependency to get token type (access/refresh)"""
    return TokenType.ACCESS

# Login endpoint
@app.post("/login", response_model=UserLoginResponse)
def login(user_data: UserLoginRequest):
    """
    User login endpoint.
    
    Authenticates user and returns JWT access token.
    
    Returns:
        UserLoginResponse with token and expiration time
    """
    try:
        user = authenticate_user(user_data.username, user_data.password)
        
        # Create access token with 15-minute expiration
        access_token = create_access_token(
            data={"sub": user["username"]},
            expires_delta=datetime.timedelta(minutes=15)
        )
        
        return UserLoginResponse(
            token=access_token,
            username=user["username"],
            expires_in=15
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

# Protected endpoint example
@app.get("/protected")
def protected_route(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Protected endpoint requiring authentication.
    
    Returns:
        User information from authentication
    """
    return current_user

# ==============================
# Security and Configuration
# ==============================
# Add middleware for security (CSRF protection, rate limiting, etc.)
# Configure CORS if needed
# Set up environment variables for secret keys and other sensitive data