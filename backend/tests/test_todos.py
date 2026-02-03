import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch
from datetime import datetime
from ..src.main import app
from ..src.database import get_session
from ..src.models.user import User
from ..src.models.todo import Todo
from ..src.utils.jwt_utils import create_access_token

# Create a test database engine
@pytest.fixture(name="engine")
def fixture_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(name="session")
def fixture_session(engine):
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def fixture_client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_todo(client, session):
    """Test creating a new todo."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="todo_test@example.com",
        password="password123",
        name="Todo Test User"
    )

    user = UserService.create_user(session, user_create)

    # Create a valid JWT token for the user
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    # Create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "completed": False,
        "priority": "medium",
        "user_id": user.id
    }

    response = client.post(
        "/api/todos/",
        json=todo_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["user_id"] == user.id

def test_get_user_todos(client, session):
    """Test retrieving a user's todos."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="get_todos_test@example.com",
        password="password123",
        name="Get Todos Test User"
    )

    user = UserService.create_user(session, user_create)

    # Create a valid JWT token for the user
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    # Create a todo
    from ..src.services.todo_service import TodoService
    from ..src.models.todo import TodoCreate

    todo_create = TodoCreate(
        title="Test Todo for Get",
        description="This is a test todo for get",
        completed=False,
        priority="medium",
        user_id=user.id
    )

    TodoService.create_todo(session, todo_create)

    # Get todos
    response = client.get(
        "/api/todos/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 1
    assert any(todo["title"] == "Test Todo for Get" for todo in data)

def test_update_todo(client, session):
    """Test updating a todo."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="update_test@example.com",
        password="password123",
        name="Update Test User"
    )

    user = UserService.create_user(session, user_create)

    # Create a valid JWT token for the user
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    # Create a todo
    from ..src.services.todo_service import TodoService
    from ..src.models.todo import TodoCreate

    todo_create = TodoCreate(
        title="Original Title",
        description="Original Description",
        completed=False,
        priority="medium",
        user_id=user.id
    )

    created_todo = TodoService.create_todo(session, todo_create)

    # Update the todo
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "completed": True
    }

    response = client.put(
        f"/api/todos/{created_todo.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True

def test_delete_todo(client, session):
    """Test deleting a todo."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="delete_test@example.com",
        password="password123",
        name="Delete Test User"
    )

    user = UserService.create_user(session, user_create)

    # Create a valid JWT token for the user
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    # Create a todo
    from ..src.services.todo_service import TodoService
    from ..src.models.todo import TodoCreate

    todo_create = TodoCreate(
        title="Todo to Delete",
        description="This todo will be deleted",
        completed=False,
        priority="medium",
        user_id=user.id
    )

    created_todo = TodoService.create_todo(session, todo_create)

    # Delete the todo
    response = client.delete(
        f"/api/todos/{created_todo.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    # Verify the todo is gone
    response = client.get(
        f"/api/todos/{created_todo.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 404