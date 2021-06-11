from fastapi.testclient import TestClient


def test_login(client: TestClient):
    client.post(
        "/users/new",
        json={"name": "Test", "email": "test@example.com", "password": "123456"},
    ).raise_for_status()

    no_credentials = client.post("/token")
    assert no_credentials.status_code == 422

    wrong_email = client.post(
        "/token", data={"username": "wrong username", "password": "?"}
    )
    assert (
        wrong_email.status_code == 401
        and wrong_email.json()["detail"] == "User does not exist"
    )
    wrong_password = client.post(
        "/token", data={"username": "test@example.com", "password": "654321"}
    )
    assert (
        wrong_password.status_code == 401
        and wrong_password.json()["detail"] == "Invalid password"
    )
    correct = client.post(
        "/token", data={"username": "test@example.com", "password": "123456"}
    )
    assert correct.status_code == 200
    token = correct.json()["access_token"]

    invalid_token = client.get("/users/me", headers={"Authorization": "Bearer test"})
    assert (
        invalid_token.status_code == 401
        and invalid_token.json()["detail"] == "Invalid or expired token"
    )

    assert client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    ).json() == {"name": "Test", "id": 1, "email": "test@example.com"}


def test_logout(client: TestClient):
    client.post(
        "/users/new",
        json={"name": "Test", "email": "test@example.com", "password": "123456"},
    ).raise_for_status()

    token = client.post(
        "/token", data={"username": "test@example.com", "password": "123456"}
    ).json()["access_token"]

    revoke = client.post("/token/revoke", headers={"Authorization": f"Bearer {token}"})
    assert revoke.status_code == 204

    expired_token = client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert (
        expired_token.status_code == 401
        and expired_token.json()["detail"] == "Invalid or expired token"
    )
