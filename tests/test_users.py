from fastapi.testclient import TestClient


def test_list_empty(client: TestClient):
    response = client.get("/users")
    assert response.status_code == 200 and response.json() == []


def test_create_get_list(client: TestClient):
    expected1 = {"name": "First User", "id": 1, "email": "test1@example.com"}
    expected2 = {"name": "Second User", "id": 2, "email": "test2@example.com"}

    # create
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

    # get
    response3 = client.get("/users/1")
    assert response3.status_code == 200 and response3.json() == expected1

    # list
    response4 = client.get("/users")
    assert response4.status_code == 200
    user_list = response4.json()
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

    assert client.get("/users").json() == [expected]


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


def test_404(client: TestClient):
    for response in (
        client.get("/users/1"),
        client.delete("/users/1"),
        client.patch(
            "/users/1", json={"email": "a@example.com", "password": "a", "name": "a"}
        ),
    ):
        assert (
            response.status_code == 404
        ), f"{response.request.method} => {response.status_code}"


def test_422(client: TestClient):
    for response in (
        client.get("/users/0"),
        client.delete("/users/0"),
        client.patch(
            "/users/0", json={"email": "a@example.com", "password": "a", "name": "a"}
        ),
    ):
        assert (
            response.status_code == 422
        ), f"{response.request.method} => {response.status_code}"
