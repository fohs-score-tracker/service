from datetime import date

from fastapi.testclient import TestClient

new_player = {"name": "test"}
new_team = {"name": "test", "coaches": [], "players": []}
new_shot = {"x": 50, "y": 25, "points": 3, "game_id": 1, "missed": False}
new_game = {"team_id": 1, "other_team": "test", "date": str(date.today())}

expected_shot = {"id": 1, **new_shot}


def test_delete_player_with_shots(redis, client: TestClient):
    client.post("/players/new", json=new_player).raise_for_status()
    client.post("/teams/new", json=new_team).raise_for_status()
    client.post("/games/new", json=new_game).raise_for_status()
    client.post("/players/1/shots/new", json=new_shot).raise_for_status()
    client.delete("/players/1").raise_for_status()

    # no shots should exist in the database after
    assert not redis.keys("shot:*")


def test_add_shot(client: TestClient):
    client.post("/players/new", json=new_player).raise_for_status()
    client.post("/teams/new", json=new_team).raise_for_status()
    client.post("/games/new", json=new_game).raise_for_status()
    resp = client.post("/players/1/shots/new", json=new_shot)
    assert resp.status_code == 201 and resp.json() == {
        "id": 1,
        "name": "test",
        "shots": [expected_shot],
    }


def test_delete_shot(client: TestClient):
    client.post("/players/new", json=new_player).raise_for_status()
    client.post("/teams/new", json=new_team).raise_for_status()
    client.post("/games/new", json=new_game).raise_for_status()
    client.post("/players/1/shots/new", json=new_shot).raise_for_status()
    resp = client.delete("/players/1/shots/1")
    assert resp.status_code == 200 and resp.json() == {
        "id": 1,
        "name": "test",
        "shots": [],
    }


def test_404(client: TestClient):
    assert client.post("/players/1/shots/new", json=new_shot).status_code == 404
    assert client.delete("/players/1/shots/1").status_code == 404
    client.post("/players/new", json=new_player).raise_for_status()
    assert client.post("/players/1/shots/new", json=new_shot).status_code == 404
    assert client.delete("/players/1/shots/1").status_code == 404
    client.post("/teams/new", json=new_team).raise_for_status()
    assert client.post("/players/1/shots/new", json=new_shot).status_code == 404
    assert client.delete("/players/1/shots/1").status_code == 404
    client.post("/games/new", json=new_game).raise_for_status()
    assert client.delete("/players/1/shots/1").status_code == 404


def test_422(client: TestClient):
    assert client.post("/players/0/shots/new", json=new_shot).status_code == 422
    assert client.delete("/players/0/shots/1").status_code == 422
    assert client.delete("/players/0/shots/0").status_code == 422
    assert client.delete("/players/1/shots/0").status_code == 422
