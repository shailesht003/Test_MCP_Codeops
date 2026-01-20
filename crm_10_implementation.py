from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, Dict, Any
import bcrypt
import jwt
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pydantic model for login request
class LoginRequest(BaseModel):
    username: str
    password: str

# Pydantic model for token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# In-memory database simulation
users_db: Dict[str, Dict[str, Any]] = {
    "user1": {
        "username": "user1",
        "hashed_password": bcrypt.hashpw("password1".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    },
    "user2": {
        "username": "user2",
        "hashed_password": bcrypt.hashpw("password2".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    }
}

# Repository pattern implementation
class UserRepository:
    """
    Repository class for user data access operations.
    Implements the repository pattern for database interactions.
    """

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user by username from the database.
        
        Args:
            username: The username to search for.
            
        Returns:
            User data if found, None otherwise.
        """
        return users_db.get(username)

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user by verifying credentials.
        
        Args:
            username: The username to authenticate.
            password: The password to verify.
            
        Returns:
            User data if authentication is successful, None otherwise.
        """
        user = self.get_user_by_username(username)
        if not user:
            return None

        if not bcrypt.checkpw(password.encode("utf-8"), user["hashed_password"].encode("utf-8")):
            return None

        return user

# Dependency for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Utility function for token generation
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    """
    Generate a JWT access token.
    
    Args:
        data: Dictionary containing data to encode in the token.
        expires_delta: Optional expiration time for the token.
        
    Returns:
        Encoded JWT token string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Main API endpoint for login
@app.post("/login", response_model=TokenResponse)
async def login_for_access_token(login_request: LoginRequest, db: UserRepository = Depends()):
    """
    API endpoint for user login.
    
    Validates user credentials and returns an access token.
    
    Args:
        login_request: Login request containing username and password.
        db: UserRepository dependency for database operations.
        
    Returns:
        TokenResponse containing the access token.
        
    Raises:
        HTTPException: If authentication fails.
    """
    user = db.authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate access token with expiration
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return TokenResponse(access_token=access_token, token_type="bearer")