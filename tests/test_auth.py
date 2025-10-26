import pytest
from api.models import db
from app import app


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["TESTING"] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
        client = app.test_client()
        yield client
        try:
            db.session.remove()
        except Exception:
            pass


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
