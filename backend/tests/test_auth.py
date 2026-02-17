import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch
from datetime import timedelta
from ..src.main import app
from ..src.database import get_session
from ..src.models.user import User
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

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "todo-backend-api"}

def test_register_new_user(client):
    """Test registering a new user."""
    user_data = {
        "email": "test@example.com",
        "password": "securepassword",
        "name": "Test User"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]

def test_login_valid_user(client, session):
    """Test logging in with valid credentials."""
    # First, create a user
    from ..src.services.user_service import UserService
    from ..src.models.user import UserCreate

    user_create = UserCreate(
        email="login@example.com",
        password="password123",
        name="Login User"
    )

    user = UserService.create_user(session, user_create)

    # Now try to log in
    login_data = {
        "email": "login@example.com",
        "password": "password123"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == login_data["email"]

def test_login_invalid_credentials(client):
    """Test logging in with invalid credentials."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401