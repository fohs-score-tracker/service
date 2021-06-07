def test_app(client):
    # make sure the docs don't crash when you go to /
    client.get("/").raise_for_status()
    client.get("/openapi.json").raise_for_status()
