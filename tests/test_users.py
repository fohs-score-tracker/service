from fastapi.testclient import TestClient


def test_list_empty(client: TestClient):
    response = client.get("/users")
    assert response.status_code == 200 and response.json() == []


def test_create_and_list(client: TestClient):
    expected1 = {"name": "First User", "id": 1, "email": "test1@example.com"}
    expected2 = {"name": "Second User", "id": 2, "email": "test2@example.com"}

    response1 = client.post(
        "/users/new",
        json={"name": "First User", "email": "test1@example.com", "password": "a"},
    )
    assert response1.status_code == 201 and response1.json() == expected1

    response2 = client.post(
        "/users/new",
        json={"name": "Second User", "email": "test2@example.com", "password": "a"},
    )
    assert response2.status_code == 201 and response2.json() == expected2

    response3 = client.get("/users")
    assert response3.status_code == 200
    user_list = response3.json()
    assert len(user_list) == 2 and expected1 in user_list and expected2 in user_list


def test_edit_and_list(client: TestClient):
    expected = {"name": "Edited User", "id": 1, "email": "edited@example.com"}

    client.post(
        "/users/new",
        json={"name": "User", "email": "test@example.com", "password": "a"},
    ).raise_for_status()

    response = client.patch(
        "/users/1",
        json={"name": "Edited User", "email": "edited@example.com", "password": "a"},
    )
    assert response.status_code == 200 and response.json() == expected

    assert client.get("/players").json() == [expected]


def test_remove_user(client: TestClient):
    client.post(
        "/users/new",
        json={"name": "Deleted User", "email": "deleted@example.com", "password": "a"},
    ).raise_for_status()
    client.post(
        "/users/new",
        json={"name": "User", "email": "user@example.com", "password": "a"},
    ).raise_for_status()

    assert client.delete("/users/1").status_code == 204

    assert client.get("/users").json() == [
        {"name": "User", "id": 2, "email": "user@example.com"}
    ]


def test_login(client: TestClient):
    client.post(
        "/users/new",
        json={"name": "Test", "email": "test@example.com", "password": "123456"},
    ).raise_for_status()

    no_credentials = client.get("/users/me")
    assert (
        no_credentials.status_code == 401
        and no_credentials.json()["detail"] == "Not authenticated"
    )
    wrong_email = client.get("/users/me", auth=("wrong@email.com", "123456"))
    assert (
        wrong_email.status_code == 401
        and wrong_email.json()["detail"] == "User does not exist"
    )
    wrong_password = client.get("/users/me", auth=("test@example.com", "654321"))
    assert (
        wrong_password.status_code == 401
        and wrong_password.json()["detail"] == "Invalid password"
    )
    correct = client.get("/users/me", auth=("test@example.com", "123456"))
    assert correct.status_code == 200 and correct.json() == {
        "name": "Test",
        "email": "test@example.com",
        "id": 1,
    }
