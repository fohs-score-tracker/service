import datetime
from fastapi.testclient import TestClient

#! Keep formator off when editing

new_user = {"name": "dan", "email": "dan@example.com", "password": "a"}
new_player = {"name": "test", "user_id": 1}
new_player_two = {"name": "test2", "user_id": 1}
new_shot = {"x": 50, "y": 25, "points": 3, "game_id": 1, "missed": False}
new_shot_two = {"x": 50, "y": 25, "points": 3, "game_id": 2, "missed": False}

new_game = {
    "name": "TestGame",
    "other_team": "test",
    "date": "2022-01-01",
    "user_id": 1,
    "player_ids": [1]
}

new_game_two = {
    "name": "TestGameTwo",
    "other_team": "test",
    "date": "2022-01-02",
    "user_id": 1,
    "player_ids": [2]
}


def test_create_game(client: TestClient):

    client.post("/users/new", json=new_user).raise_for_status()
    client.post("/players/new", json=new_player).raise_for_status()
    resp = client.post("/games/new", json=new_game)
    assert resp.status_code == 201 and resp.json() == {
        "name": "TestGame",
        "id": 1,
        "user": {"name": "dan", "email": "dan@example.com", "id": 1},
        "players": [
            {
                "name": "test",
                "id": 1,
                "user": {"name": "dan", "email": "dan@example.com", "id": 1},
                "shots": [],
            },
        ],
        "other_team": "test",
        "date": "2022-01-01",
    }


def test_Get_Game(client: TestClient):
    client.post("/users/new", json=new_user).raise_for_status()
    client.post("/players/new", json=new_player).raise_for_status()
    client.post("/games/new", json=new_game).raise_for_status()
    client.post("/players/1/shots/new", json=new_shot).raise_for_status()
    res = client.get("/games/1")
    assert res.status_code == 200 and res.json() == {
        "name": "TestGame",
        "id": 1,
        "user": {"name": "dan", "email": "dan@example.com", "id": 1},
        "players": [
            {
                "name": "test",
                "id": 1,
                "user": {"name": "dan", "email": "dan@example.com", "id": 1},
                "shots": [
                    {
                        "x": 50,
                        "y": 25,
                        "points": 3,
                        "game_id": 1,
                        "missed": False,
                        "id": 1,
                    },
                ],
            },
        ],
        "other_team": "test",
        "date": "2022-01-01",
    }


def test_Get_Game_List(client: TestClient):

    expected_game_one = {
        "name": "TestGame",
        "id": 1,
        "user": {"name": "dan", "email": "dan@example.com", "id": 1},
        "players": [
            {
                "name": "test",
                "id": 1,
                "user": {"name": "dan", "email": "dan@example.com", "id": 1},
                "shots": [],
            }
        ],
        "other_team": "test",
        "date": "2022-01-01",
    }

    expected_game_two = {
        "name": "TestGameTwo",
        "id": 2,
        "user": {"name": "dan", "email": "dan@example.com", "id": 1},
        "players": [
            {
                "name": "test2",
                "user": {"name": "dan", "email": "dan@example.com", "id": 1},
                "id": 2,
                "shots": [
                    {
                        "x": 50,
                        "y": 25,
                        "points": 3,
                        "game_id": 2,
                        "missed": False,
                        "id": 1,
                    }
                ],
            },
        ],
        "other_team": "test",
        "date": "2022-01-02",
    }

    client.post("/users/new", json=new_user).raise_for_status()
    client.post("/players/new", json=new_player).raise_for_status()
    client.post("/players/new", json=new_player_two).raise_for_status()
    client.post("/games/new", json=new_game).raise_for_status()
    client.post("/games/new", json=new_game_two).raise_for_status()
    client.post("/players/2/shots/new", json=new_shot_two).raise_for_status()
    res = client.get("/games")
    assert res.status_code == 200 and res.json() == [
        expected_game_one,
        expected_game_two,
    ]


def test_delete_game(client: TestClient):
    client.post("/users/new", json=new_user).raise_for_status()
    client.post("/players/new", json=new_player).raise_for_status()
    client.post("/players/new", json=new_player_two).raise_for_status()
    client.post("/games/new", json=new_game).raise_for_status()
    client.post("/games/new", json=new_game_two).raise_for_status()
    client.post("/players/2/shots/new", json=new_shot_two).raise_for_status()
    res = client.delete("/games/2")
    assert res.status_code == 204
    assert client.get("/games").json() == [
        {
            "name": "TestGame",
            "id": 1,
            "user": {"name": "dan", "email": "dan@example.com", "id": 1},
            "players": [
                {
                    "name": "test",
                    "id": 1,
                    "user": {"name": "dan", "email": "dan@example.com", "id": 1},
                    "shots": [],
                },
            ],
            "other_team": "test",
            "date": "2022-01-01",
        },
    ]


def test_update_game(client: TestClient):
    shot_for_player_two = {"x": 50, "y": 25, "points": 3, "game_id": 1, "missed": False}
    client.post("/users/new", json=new_user).raise_for_status()
    client.post("/players/new", json=new_player).raise_for_status()
    client.post("/players/new", json=new_player_two).raise_for_status()
    client.post("/games/new", json=new_game).raise_for_status()
    client.post("/players/2/shots/new", json=shot_for_player_two).raise_for_status()    
    res = client.patch("/games/1", json=new_game_two)
    assert res.status_code == 200 and res.json() == {
        "name": "TestGameTwo",
        "id": 1,
        "user": {"name": "dan", "email": "dan@example.com", "id": 1},
        "players": [
            {
                "name": "test2",
                "user": {"name": "dan", "email": "dan@example.com", "id": 1},
                "id": 2,
                "shots": [
                    {
                        "x": 50,
                        "y": 25,
                        "points": 3,
                        "game_id": 1,
                        "missed": False,
                        "id": 1,
                    }
                ],
            },
        ],
        "other_team": "test",
        "date": "2022-01-02",
    }


def test_games_422(client: TestClient):
    fakeData = {"name": "TestGame", "date": "2022-01-01"}
    client.post("/users/new", json=new_user).raise_for_status()
    client.post("/players/new", json=new_player).raise_for_status()
    client.post("/games/new", json=new_game).raise_for_status()
    assert client.post("/games/new", json=fakeData).status_code == 422
    assert client.patch("/games/1", json=fakeData).status_code == 422


def test_games_404(client: TestClient):
    assert client.get("/games/1").status_code == 404
    assert client.patch("/games/1", json=new_game_two).status_code == 404
    assert client.delete("/games/1").status_code == 404
    assert client.post("/games/new", json=new_game).status_code == 404

    
