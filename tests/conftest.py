import pytest
from fakeredis import FakeRedis
from fastapi.testclient import TestClient
from scoretracker import app
from scoretracker.deps import get_redis

fake_redis = FakeRedis(decode_responses=True)
app.dependency_overrides[get_redis] = lambda: fake_redis


@pytest.fixture
def client() -> TestClient:
    """A FastAPI test client."""
    fake_redis.flushdb()
    return TestClient(app)
