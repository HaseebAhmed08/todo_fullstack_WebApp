import pytest
import asyncio
import time
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from concurrent.futures import ThreadPoolExecutor
from ..src.main import app
from ..src.database import get_session

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

def test_concurrent_user_performance(client):
    """
    Test performance with concurrent users making requests.
    """
    def make_request():
        response = client.get("/health")
        return response.status_code == 200

    # Simulate 10 concurrent users
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [future.result() for future in futures]

    # All requests should succeed
    assert all(results), f"Some requests failed: {results}"

    # Test that the average response time is acceptable
    start_time = time.time()
    for _ in range(10):
        client.get("/health")
    end_time = time.time()

    avg_response_time = (end_time - start_time) / 10
    # Assert that average response time is under 100ms
    assert avg_response_time < 0.1, f"Average response time too high: {avg_response_time}s"