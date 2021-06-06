from scoretracker.tests import client, auth
test_account_details = {}

def test_read_users():
    response = client.get("/users")
    assert response.status_code == 200

def test_create_user():
    global test_account_details
    response = client.post("/users/new", json={"name": "Jeffthetest",
    "password": "qwerty1234", "email": "jeffthetest@example.com" })
    assert response.status_code == 201
    test_account_details = response.json()

def test_find_user():
    global test_account_details
    id = test_account_details["id"]
    response = client.get(f"/users/{id}")
    assert response.status_code == 200
    assert  response.json() == test_account_details

#TODO ask for help with basic auth 

def test_remove_user():
    global test_account_details
    id = test_account_details["id"]
    response = client.delete(f"/users/{id}")
    assert response.status_code == 204



