from fastapi.testclient import TestClient


def test_list_empty(client: TestClient):
    response = client.get("/players")
    assert response.status_code == 200 and response.json() == []


def test_create_get_list(client: TestClient):
    expected1 = {"name": "First Player", "id": 1, "shots": []}
    expected2 = {"name": "Second Player", "id": 2, "shots": []}

    # create
    response1 = client.post(
        "/players/new",
        json={"name": "First Player"},
    )
    assert response1.status_code == 201 and response1.json() == expected1

    response2 = client.post(
        "/players/new",
        json={"name": "Second Player"},
    )
    assert response2.status_code == 201 and response2.json() == expected2

    # get
    response3 = client.get("/players/1")
    assert response3.status_code == 200 and response3.json() == expected1

    # list
    response4 = client.get("/players")
    assert response4.status_code == 200
    player_list = response4.json()
    assert (
        len(player_list) == 2 and expected1 in player_list and expected2 in player_list
    )


def test_edit_and_list(client: TestClient):
    expected = {"name": "Edited Player", "id": 1, "shots": []}

    client.post(
        "/players/new",
        json={"name": "Player"},
    ).raise_for_status()

    response = client.patch(
        "/players/1",
        json={"name": "Edited Player"},
    )
    assert response.status_code == 200 and response.json() == expected

    assert client.get("/players").json() == [expected]


def test_remove_player(client: TestClient):
    client.post(
        "/players/new",
        json={
            "name": "Deleted Player",
        },
    ).raise_for_status()

    client.post(
        "/players/new",
        json={"name": "Player"},
    ).raise_for_status()

    assert client.delete("/players/1").status_code == 204

    assert client.get("/players").json() == [{"name": "Player", "id": 2, "shots": []}]


def test_404(client: TestClient):
    for response in (
        client.get("/players/1"),
        client.delete("/players/1"),
        client.patch("/players/1", json={"name": "a"}),
    ):
        assert (
            response.status_code == 404
        ), f"{response.request.method} => {response.status_code}"


def test_422(client: TestClient):
    for response in (
        client.get("/players/0"),
        client.delete("/players/0"),
        client.patch("/players/0", json={"name": "a"}),
    ):
        assert (
            response.status_code == 422
        ), f"{response.request.method} => {response.status_code}"
