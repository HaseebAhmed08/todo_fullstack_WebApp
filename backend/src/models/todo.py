from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")  # 'low', 'medium', 'high'
    due_date: Optional[datetime] = None

class Todo(TodoBase, table=True):
    """
    Todo entity representing a task item owned by a specific user.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TodoCreate(TodoBase):
    """
    Schema for creating a new todo.
    """
    title: str  # Required field
    user_id: str  # Required field

class TodoRead(TodoBase):
    """
    Schema for reading todo data.
    """
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class TodoUpdate(SQLModel):
    """
    Schema for updating todo information.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None  # 'low', 'medium', 'high'
    due_date: Optional[datetime] = None