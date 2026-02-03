from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, nullable=False, max_length=255)
    name: str = Field(max_length=100)


class User(UserBase, table=True):
    """
    User entity representing a registered account with attributes:
    user_id (unique identifier), email (authentication credential),
    name (display name), password_hash (securely stored credential)
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login_at: Optional[datetime] = None
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    """
    Schema for creating a new user with password validation.
    """
    password: str = Field(min_length=8)


class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information).
    """
    id: str
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    is_active: bool


class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, unique=True, max_length=255)


class UserLogin(SQLModel):
    """
    Schema for user login credentials.
    """
    email: str
    password: str