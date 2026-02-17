from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Authentication-related schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserRegisterRequest(BaseModel):
    email: str
    password: str
    name: str

class AuthResponse(BaseModel):
    token: str
    user: dict

class LogoutResponse(BaseModel):
    success: bool

# Todo-related schemas
class TodoCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"  # 'low', 'medium', 'high'
    due_date: Optional[datetime] = None
    user_id: str

class TodoUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[str] = None
    priority: Optional[str] = None  # 'low', 'medium', 'high'
    due_date: Optional[datetime] = None

class TodoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str  # 'low', 'medium', 'high'
    due_date: Optional[datetime] = None
    user_id: str
    created_at: datetime
    updated_at: datetime

class TodoListResponse(BaseModel):
    todos: List[TodoResponse]
    pagination: dict

class BulkOperationRequest(BaseModel):
    operation: str  # 'update', 'delete', 'complete', 'uncomplete'
    ids: List[str]
    data: Optional[dict] = None

class BulkOperationResponse(BaseModel):
    success: bool
    affected_count: int

# Error response schema
class ErrorResponse(BaseModel):
    error: dict

# Health check response
class HealthResponse(BaseModel):
    status: str
    service: str