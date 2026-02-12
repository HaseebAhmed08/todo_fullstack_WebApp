from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Optional

from ..database import get_session
from ..models.user import User, UserRead, UserUpdate
from ..api.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserRead)
def read_user_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user.
    """
    return current_user


@router.put("/me", response_model=UserRead)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update current authenticated user.
    """
    # Update only the fields that are provided
    if user_update.name is not None:
        current_user.name = user_update.name
    if user_update.email is not None:
        current_user.email = user_update.email
    if user_update.image is not None:
        current_user.image = user_update.image
    
    # Update the timestamp
    current_user.updated_at = current_user.updated_at.__class__()  # Updates to current time
    
    # Commit the changes to the database
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    return current_user