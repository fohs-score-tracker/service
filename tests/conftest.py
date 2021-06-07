import pytest
from fakeredis import FakeRedis
from fastapi.testclient import TestClient
from scoretracker import app
from scoretracker.deps import get_redis, get_settings

settings = get_settings()

# the settings object is cached so this will affect all future requests
settings.SCORETRACKER_TESTING_MODE = True


@pytest.yield_fixture
def client() -> TestClient:
    """A FastAPI test client."""
    fake_db = get_redis()
    assert isinstance(fake_db, FakeRedis)  # just making sure
    yield TestClient(app)
    fake_db.flushall()
