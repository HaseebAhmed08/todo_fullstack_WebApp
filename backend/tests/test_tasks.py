import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch
from datetime import datetime
from ..src.main import app
from ..src.database import get_session
from ..src.models.user import User
from ..src.models.task import Task
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

def test_create_task(client, session):
    """Test creating a new task."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="task_test@example.com",
        password="password123",
        name="Task Test User"
    )

    user = UserService.create_user(session, user_create)

    # Create a valid JWT token for the user
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    # Create a task
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }

    response = client.post(
        f"/api/{user.id}/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] == task_data["completed"]
    assert data["user_id"] == user.id
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_user_tasks(client, session):
    """Test retrieving a user's tasks."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="get_tasks_test@example.com",
        password="password123",
        name="Get Tasks Test User"
    )

    user = UserService.create_user(session, user_create)

    # Create a valid JWT token for the user
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    # Create a task
    from ..src.services.task_service import TaskService
    from ..src.models.task import TaskCreate

    task_create = TaskCreate(
        title="Test Task for Get",
        description="This is a test task for get",
        completed=False
    )

    TaskService.create_task(session, task_create, user.id)

    # Get tasks
    response = client.get(
        f"/api/{user.id}/tasks/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 1
    assert any(task["title"] == "Test Task for Get" for task in data)

def test_get_specific_task(client, session):
    """Test retrieving a specific task."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="get_specific_task_test@example.com",
        password="password123",
        name="Get Specific Task Test User"
    )

    user = UserService.create_user(session, user_create)

    # Create a valid JWT token for the user
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    # Create a task
    from ..src.services.task_service import TaskService
    from ..src.models.task import TaskCreate

    task_create = TaskCreate(
        title="Specific Task",
        description="This is a specific test task",
        completed=False
    )

    created_task = TaskService.create_task(session, task_create, user.id)

    # Get the specific task
    response = client.get(
        f"/api/{user.id}/tasks/{created_task.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Specific Task"
    assert data["description"] == "This is a specific test task"
    assert data["id"] == created_task.id

def test_update_task(client, session):
    """Test updating a task."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="update_task_test@example.com",
        password="password123",
        name="Update Task Test User"
    )

    user = UserService.create_user(session, user_create)

    # Create a valid JWT token for the user
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    # Create a task
    from ..src.services.task_service import TaskService
    from ..src.models.task import TaskCreate

    task_create = TaskCreate(
        title="Original Title",
        description="Original Description",
        completed=False
    )

    created_task = TaskService.create_task(session, task_create, user.id)

    # Update the task
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "completed": True
    }

    response = client.put(
        f"/api/{user.id}/tasks/{created_task.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True

def test_update_task_completion(client, session):
    """Test updating task completion status."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="update_completion_test@example.com",
        password="password123",
        name="Update Completion Test User"
    )

    user = UserService.create_user(session, user_create)

    # Create a valid JWT token for the user
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    # Create a task
    from ..src.services.task_service import TaskService
    from ..src.models.task import TaskCreate

    task_create = TaskCreate(
        title="Completion Test Task",
        description="Task to test completion update",
        completed=False
    )

    created_task = TaskService.create_task(session, task_create, user.id)

    # Update the task completion
    completion_data = {
        "completed": True
    }

    response = client.patch(
        f"/api/{user.id}/tasks/{created_task.id}/complete",
        json=completion_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["completed"] is True

def test_delete_task(client, session):
    """Test deleting a task."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="delete_task_test@example.com",
        password="password123",
        name="Delete Task Test User"
    )

    user = UserService.create_user(session, user_create)

    # Create a valid JWT token for the user
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    # Create a task
    from ..src.services.task_service import TaskService
    from ..src.models.task import TaskCreate

    task_create = TaskCreate(
        title="Task to Delete",
        description="This task will be deleted",
        completed=False
    )

    created_task = TaskService.create_task(session, task_create, user.id)

    # Delete the task
    response = client.delete(
        f"/api/{user.id}/tasks/{created_task.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    # Verify the task is gone by trying to get it
    response = client.get(
        f"/api/{user.id}/tasks/{created_task.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 404

def test_unauthorized_access_to_other_users_tasks(client, session):
    """Test that users cannot access other users' tasks."""
    # Create two users
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user1_create = UserCreate(
        email="user1@example.com",
        password="password123",
        name="User 1"
    )
    user1 = UserService.create_user(session, user1_create)

    user2_create = UserCreate(
        email="user2@example.com",
        password="password123",
        name="User 2"
    )
    user2 = UserService.create_user(session, user2_create)

    # Create valid JWT tokens for both users
    access_token_user1 = create_access_token(
        data={"sub": user1.id, "email": user1.email, "name": user1.name}
    )
    access_token_user2 = create_access_token(
        data={"sub": user2.id, "email": user2.email, "name": user2.name}
    )

    # Create a task for user1
    from ..src.services.task_service import TaskService
    from ..src.models.task import TaskCreate

    task_create = TaskCreate(
        title="User1's Private Task",
        description="This task belongs to user1",
        completed=False
    )
    created_task = TaskService.create_task(session, task_create, user1.id)

    # Try to access user1's task with user2's token (should fail)
    response = client.get(
        f"/api/{user1.id}/tasks/{created_task.id}",
        headers={"Authorization": f"Bearer {access_token_user2}"}
    )
    assert response.status_code == 403  # Forbidden

def test_request_validation_errors(client, session):
    """Test request validation errors."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="validation_test@example.com",
        password="password123",
        name="Validation Test User"
    )

    user = UserService.create_user(session, user_create)

    # Create a valid JWT token for the user
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    # Try to create a task with invalid data (missing required fields)
    invalid_task_data = {
        "description": "Task without title"
        # Missing required "title" field
    }

    response = client.post(
        f"/api/{user.id}/tasks/",
        json=invalid_task_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 422  # Validation error