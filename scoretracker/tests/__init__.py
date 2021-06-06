from fastapi.testclient import TestClient
from scoretracker import app
import base64
client = TestClient(app)


def auth(data: str):
    return str(base64.b64encode(data.encode("utf-8")), "utf-8")

