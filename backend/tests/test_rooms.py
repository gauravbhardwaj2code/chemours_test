def test_list_rooms(client):
    res = client.get("/rooms")
    assert res.status_code == 200
    assert [r["name"] for r in res.json()] == ["Focus Room", "Board Room", "Huddle"]


def test_create_room(client):
    res = client.post("/rooms", json={"name": "Phone Booth", "capacity": 1})
    assert res.status_code == 201
    assert res.json()["name"] == "Phone Booth"


def test_create_room_duplicate_name(client):
    res = client.post("/rooms", json={"name": "Huddle", "capacity": 3})
    assert res.status_code == 409


def test_list_users(client):
    res = client.get("/users")
    assert res.status_code == 200
    roles = {u["name"]: u["role"] for u in res.json()}
    assert roles["Divya"] == "intern"
    assert roles["Chen"] == "manager"
