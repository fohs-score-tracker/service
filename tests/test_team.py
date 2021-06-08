from fastapi.testclient import TestClient
from requests.models import Response



def create_team(client: TestClient) ->  Response:
    client.post('/players/new', json={"name": "TestJeff"})
    client.post('/users/new', json={"name": "test",
                "password": "test", "email": "jeff@example.com"})
    return client.post("/teams/new", json={"name": "testTeam", "players": [1], "coaches": [1]})

def test_empty_team(client: TestClient):
    response = client.get('/teams')
    assert response.status_code == 200 and response.json() == []

def test_new_team(client: TestClient):
     response = create_team(client)
     assert response.status_code == 201 and response.json() == {'id': 1, 'name': 'testTeam', 'coaches': [{'name': 'test', 'email': 'jeff@example.com', 'id': 1}], 'players': [{'id': 1, 'name': 'TestJeff', 'shots': []}]}

def test_new_team_422(client: TestClient):
    response = client.post(
        "/teams/new", json={"name": "junk", "players": [0], "coaches": [0]})
    assert response.status_code == 422 

def test_team_not_empty(client: TestClient):
    response = client.get("/teams")
    create_team(client)
    assert response.status_code == 200 and response.json() != {}

def test_team_id(client: TestClient):
    create_team(client)
    response = client.get("/teams/1")
    assert response.status_code == 200 and response.json() == {'id': 1, 'name': 'testTeam', 'coaches': [{'name': 'test', 'email': 'jeff@example.com', 'id': 1}], 'players': [{'id': 1, 'name': 'TestJeff', 'shots': []}]}

def test_team_id_404(client: TestClient):
    response = client.get("/teams/99999")
    assert response.status_code == 404 and response.json() == {'detail': 'Not Found'}




