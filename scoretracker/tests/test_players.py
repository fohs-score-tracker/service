from scoretracker.tests import client
test_player_details = {}

def tests_players_list():
    response = client.get('/players')
    assert response.status_code == 200


def test_make_players():
    global test_player_details
    response = client.post('/players/new', json={"name": "testJeff"})
    assert response.status_code == 201
    test_player_details = response.json()


def test_edit_players():
    global test_player_details
    id = test_player_details["id"]
    response = client.patch(f"/players/{id}", json={"name": "test"})
    assert response.status_code == 200
    assert response.json() != test_player_details

def test_remove_user():
    global test_player_details
    id = test_player_details["id"]
    response = client.delete(f"/players/{id}")
    assert response.status_code == 204