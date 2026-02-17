from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Optional

from ..database import get_session
from ..models.user import UserRead, UserUpdate
from ..api.auth import get_current_user, AuthenticatedUser

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=dict)
def read_user_me(current_user: AuthenticatedUser = Depends(get_current_user)):
    """
    Get current authenticated user.
    """
    return {"id": current_user.id, "email": current_user.email, "name": current_user.name}


@router.put("/me", response_model=dict)
def update_user_me(
    user_update: UserUpdate,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update current authenticated user.
    """
    # Since we're not storing user data in our backend DB, we can't update it here
    # This would typically be handled by Better Auth directly
    # For now, we'll return the current user info
    return {"id": current_user.id, "email": current_user.email, "name": current_user.name}