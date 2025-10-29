def test_logout_revokes_token(client):
    r = client.post(
        "/api/signup", json={"email": "logout@example.com", "password": "pw"}
    )
    assert r.status_code == 200

    r = client.post(
        "/api/token", json={"email": "logout@example.com", "password": "pw"}
    )
    assert r.status_code == 200
    token = r.get_json()["token"]

    r = client.get("/api/private", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200

    r = client.post("/api/logout", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200

    r = client.get("/api/private", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
