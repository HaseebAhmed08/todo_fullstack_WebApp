from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from typing import Dict, Any
from pydantic import BaseModel
import json

from ..database import get_session
from ..models.user import User, UserRead
from ..config import settings
from ..utils.security import decode_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# HTTPBearer for token extraction from Authorization header
bearer_scheme = HTTPBearer(auto_error=False)

# Define a simple authenticated user representation for internal use
class AuthenticatedUser(BaseModel):
    id: str
    email: str = ""
    name: str = ""

async def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), session: Session = Depends(get_session)) -> AuthenticatedUser:
    """
    Dependency to get the current authenticated user.
    First tries to extract JWT from Authorization header, then falls back to session cookies.
    """
    token = None
    
    # First, try to get token from Authorization header
    if credentials and credentials.credentials:
        token = credentials.credentials
    else:
        # If no token in header, try to get from cookies (Better Auth session)
        session_cookie = request.cookies.get('__Secure-authjs.session-token') or request.cookies.get('authjs.session-token')
        if session_cookie:
            # For Better Auth, we might need to validate the session token differently
            # For now, let's try to extract user info from the session cookie if it contains JWT
            token = session_cookie
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - no token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Decode the token using the shared secret
        payload = decode_access_token(token)

        # Extract user ID from 'sub' claim (standard JWT claim) or 'user_id' from Better Auth
        user_id = payload.get("sub") or payload.get("user_id") or payload.get("id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - no user ID found in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create an authenticated user object with the ID from token
        authenticated_user = AuthenticatedUser(
            id=user_id,
            email=payload.get("email", ""),
            name=payload.get("name", "")
        )

        return authenticated_user
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the actual error for debugging
        print(f"Error validating token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - token validation failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=Dict[str, Any])
def read_users_me(current_user: AuthenticatedUser = Depends(get_current_user)):
    """
    Get current authenticated user.
    """
    return {"id": current_user.id, "email": current_user.email, "name": current_user.name}
