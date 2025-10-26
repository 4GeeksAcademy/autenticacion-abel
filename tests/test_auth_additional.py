from api.auth import create_token


def test_invalid_credentials(client):
    # requesting a token with wrong password should fail
    r = client.post("/api/signup", json={"email": "bob@example.com", "password": "pw"})
    assert r.status_code == 200

    r = client.post(
        "/api/token", json={"email": "bob@example.com", "password": "wrong"}
    )
    assert r.status_code == 401


def test_signup_duplicate(client):
    r = client.post("/api/signup", json={"email": "dupe@example.com", "password": "pw"})
    assert r.status_code == 200
    # second signup with same email should return 400
    r = client.post("/api/signup", json={"email": "dupe@example.com", "password": "pw"})
    assert r.status_code == 400


def test_expired_token(client):
    # create a user and generate a token that's already expired
    r = client.post("/api/signup", json={"email": "old@example.com", "password": "pw"})
    assert r.status_code == 200
    # token with negative minutes -> already expired
    token = create_token(1, minutes=-1)
    r = client.get("/api/private", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401


def test_logout_revokes_token(client):
    # signup and get a token
    r = client.post(
        "/api/signup", json={"email": "logout@example.com", "password": "pw"}
    )
    assert r.status_code == 200
    r = client.post(
        "/api/token", json={"email": "logout@example.com", "password": "pw"}
    )
    assert r.status_code == 200
    token = r.json.get("token") if hasattr(r, "json") else r.get_json().get("token")
    # access private should work
    r = client.get("/api/private", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    # logout (revoke)
    r = client.post("/api/logout", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    # subsequent access must fail
    r = client.get("/api/private", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
