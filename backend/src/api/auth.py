from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from typing import Dict, Any

from ..database import get_session
from ..models.user import User, UserRead
from ..config import settings
from ..utils.security import decode_access_token

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

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user.
    """
    return current_user
