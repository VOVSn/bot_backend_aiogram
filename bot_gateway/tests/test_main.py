from fastapi.testclient import TestClient

from bot_gateway.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 404  # As we don't have a root endpoint
