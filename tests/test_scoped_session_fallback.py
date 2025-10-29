def test_scoped_session_fallback(client, monkeypatch):
    """Simulate a scoped_session that doesn't implement .get() and ensure
    the fallback to `User.query.get` is used by the `/api/private` route.
    """
    # create a user and obtain a token
    r = client.post(
        "/api/signup", json={"email": "scoped@example.com", "password": "pw"}
    )
    assert r.status_code == 200
    r = client.post(
        "/api/token", json={"email": "scoped@example.com", "password": "pw"}
    )
    assert r.status_code == 200
    token = r.get_json()["token"]

    # monkeypatch db.session.get to raise AttributeError when called
    from api.models import db

    def _raise_attr(*a, **kw):
        raise AttributeError("scoped_session has no get")

    # attach the attribute even if it's not present; calling it will raise
    monkeypatch.setattr(db.session, "get", _raise_attr, raising=False)

    # request private route; fallback should still allow access
    r = client.get("/api/private", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
