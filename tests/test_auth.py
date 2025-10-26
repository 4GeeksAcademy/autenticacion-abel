def test_signup_token_private(client):
    # signup
    r = client.post(
        "/api/signup", json={"email": "pytest@example.com", "password": "pw"}
    )
    assert r.status_code == 200

    # token
    r = client.post(
        "/api/token", json={"email": "pytest@example.com", "password": "pw"}
    )
    assert r.status_code == 200
    data = r.get_json()
    assert "token" in data
    token = data["token"]

    # private
    r = client.get("/api/private", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["user"]["email"] == "pytest@example.com"
