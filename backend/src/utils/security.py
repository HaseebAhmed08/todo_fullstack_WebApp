from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from ..config import settings
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the provided plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes the provided password.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Decodes a JWT access token and returns its payload.
    Raises HTTPException for invalid tokens.
    """
    try:
        print(f"Attempting to decode token: {token[:30]}...")  # Debug log
        print(f"Using secret: {settings.BETTER_AUTH_SECRET[:20]}...")  # Debug log

        # Handle potential "Bearer " prefix
        if token.lower().startswith("bearer "):
            token = token[7:]
        
        # Better Auth JWT plugin should create standard JWTs with HS256
        # Let's also try to verify the token format first
        if '.' not in token:
            raise JWTError("Invalid token format - not a valid JWT")

        # Split the token to check parts
        parts = token.split('.')
        if len(parts) != 3:
            raise JWTError("Invalid JWT format - wrong number of parts")

        # Try to decode with HS256 algorithm (most common for Better Auth)
        payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub") or payload.get("user_id") or payload.get("id")
        print(f"✅ JWT decoded successfully. User ID: {user_id}, Payload: {payload}")
        return payload
    except JWTError as e:
        print(f"JWT Error: {str(e)}")  # Debug log
        print(f"Token verification failed. This might be due to:")
        print(f"- Incorrect secret key")
        print(f"- Wrong algorithm")
        print(f"- Expired token")
        print(f"- Malformed token")
        print(f"- Missing Bearer prefix")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - token validation failed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(f"Unexpected error during token decoding: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - unexpected error",
            headers={"WWW-Authenticate": "Bearer"},
        )