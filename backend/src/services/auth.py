from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from ..models.user import User, UserCreate

# Secret key for JWT - in production, this should be in environment variables
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "W5OTzWvIpdfwtwLzzgaLFE9yru9LQ3AA")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = session.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decode a JWT access token and return the payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise JWTError("Could not decode token")

def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user in the database."""
    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create the user object
    db_user = User(
        email=user_create.email,
        name=user_create.name,
        password_hash=hashed_password
    )

    # Add to session and commit
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user