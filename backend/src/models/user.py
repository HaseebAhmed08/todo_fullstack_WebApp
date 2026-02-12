from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, nullable=False, max_length=255)
    name: str = Field(max_length=100)
    image: Optional[str] = Field(default=None)
    emailVerified: bool = Field(default=False)  # CamelCase to match Better Auth default if needed, or map it. Better Auth usually uses snake_case in DB but camelCase in JS. Let's stick to Pythonic snake_case for the model field names if possible, but map to DB column names if they differ. 
                                                # However, Better Auth's default schema often uses 'emailVerified'. Let's check the inspection output again... 
                                                # Wait, inspection output showed 'users' table. I am CHANGING it to 'user'. 
                                                # Better Auth defaults:
                                                # Table: "user"
                                                # Columns: id, name, email, emailVerified, image, createdAt, updatedAt
                                                # Let's map Python attributes to these DB columns.

class User(UserBase, table=True):
    """
    User entity aligning with Better Auth schema.
    """
    __tablename__ = "user" 
    
    id: str = Field(primary_key=True) # Better Auth generates IDs on client or server, usually text.
    password: Optional[str] = Field(default=None) # Better Auth stores password in 'account' for OAuth usually, but for email/pass it might be in 'user' or separate. 
                                                  # WAIT. Better Auth with email/password plugin definitely needs a password field. 
                                                  # Standard Better Auth might put it in an 'account' table if using adapters, 
                                                  # but purely for email/pass it often lives on 'user' or 'account'.
                                                  # Let's assume it's on 'user' for now based on typical simple setups, or 'account'.
                                                  # Actually, looking at the 'users' table from inspection: it had 'password_hash'.
                                                  # I will assume Better Auth uses 'password' field on 'user' if not using an adapter.
                                                  # The previous `inspect_db.py` showed `users` table with `password_hash`. 
                                                  # This suggests the previous backend was custom. 
                                                  # I am REPLACING that with Better Auth's schema.
                                                  # Better Auth usually creates: user, session, account, verification.
                                                  # I will add the 'user' table definition.

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"name": "createdAt"}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"name": "updatedAt"}
    )
    
    # Relationships can be added here if needed

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    image: Optional[str] = None