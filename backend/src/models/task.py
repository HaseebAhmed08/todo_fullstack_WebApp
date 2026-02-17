from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task entity representing a user-owned task with attributes:
    task_id (unique identifier), title (task name), description (detailed information),
    completed (status flag), user_id (foreign key linking to owning user)
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    title: str  # Required field
    user_id: str  # Required field


class TaskRead(TaskBase):
    """
    Schema for reading task data.
    """
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """
    Schema for updating task information.
    """
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TaskComplete(SQLModel):
    """
    Schema for marking a task as complete/incomplete.
    """
    completed: bool