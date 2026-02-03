from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta
from typing import Dict, Any
import os
from ..services.database import get_session
from ..services.auth import authenticate_user, create_access_token, create_user
from ..models.user import User, UserCreate, UserLogin
from ..utils.jwt_utils import ACCESS_TOKEN_EXPIRE_MINUTES
from ..services.user_service import UserService
from ..middleware.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(
    user_credentials: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT token.
    """
    user = UserService.authenticate_user(session, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token that expires in 7 days to match Better Auth default
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }


@router.post("/signup")
def signup(
    user_create: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Register a new user account.
    """
    # Check if user already exists
    existing_user = UserService.get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists"
        )

    # Create the new user
    user = UserService.create_user(session, user_create)

    # Create access token for the new user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }


@router.post("/auto-create-user")
def auto_create_user_from_jwt(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a backend user from JWT token if user doesn't exist.
    This endpoint is called when a user authenticates via Better Auth
    but doesn't exist in the backend database.
    """
    user_id = current_user.get("user_id")
    email = current_user.get("email")
    name = current_user.get("name", "")

    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JWT token: missing user_id or email"
        )

    # Check if user already exists in backend
    existing_user = UserService.get_user_by_email(session, email)
    if existing_user:
        return {
            "user": {
                "id": existing_user.id,
                "email": existing_user.email,
                "name": existing_user.name
            },
            "created": False
        }

    # Create new user based on JWT information
    user_create = UserCreate(
        email=email,
        name=name if name else email.split("@")[0],  # Use email prefix as name if not provided
        password=os.getenv("DEFAULT_USER_PASSWORD", "TempPassword123!")  # This will be hashed
    )

    new_user = UserService.create_user(session, user_create)

    return {
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.name
        },
        "created": True
    }