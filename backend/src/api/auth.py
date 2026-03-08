from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from typing import Dict, Any
from datetime import timedelta

from ..database import get_session
from ..models.user import User, UserRead, UserCreate
from ..models.schemas import UserLoginRequest, Token
from ..config import settings
from ..utils.security import decode_access_token, get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# We use the tokenUrl mostly for Swagger UI to know where to send credentials,
# but effectively we rely on Better Auth frontend to get the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    """
    Dependency to get the current authenticated user from the JWT token.
    Validates the token issued by Better Auth and retrieves the user.
    """
    # 1. Decode the token using the shared secret
    payload = decode_access_token(token)
    
    # 2. Extract user ID from 'sub' claim
    user_id = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Fetch user from database
    user = session.exec(select(User).where(User.id == user_id)).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Create a new user account.
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Create the user
    user = User(
        id=str(__import__("uuid").uuid4()),
        email=user_data.email,
        name=user_data.name,
        password=hashed_password,
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

@router.post("/login", response_model=Token)
def login(login_data: UserLoginRequest, session: Session = Depends(get_session)):
    """
    Authenticate user and return JWT token.
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == login_data.email)).first()
    
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user.
    """
    return current_user
