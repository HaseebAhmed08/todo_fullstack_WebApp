from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, nullable=False, max_length=255)
    name: str = Field(max_length=100)
    image: Optional[str] = Field(default=None, max_length=500)
    emailVerified: bool = Field(default=False)

class User(UserBase, table=True):
    """
    User entity aligning with Better Auth schema.
    """
    __tablename__ = "user"

    id: str = Field(primary_key=True)
    password: Optional[str] = Field(default=None, max_length=255)

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"name": "createdAt"}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"name": "updatedAt"}
    )

class UserCreate(UserBase):
    password: str = Field(min_length=1, max_length=72)

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    image: Optional[str] = None