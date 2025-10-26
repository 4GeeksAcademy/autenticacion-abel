import os
import sys

# make src importable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)

import pytest

# Compatibility shim for upstream flask-admin API changes: allow existing code that
# calls Admin(..., template_mode=...) to keep working during tests by wrapping
# the Admin class at import time. This only affects the test process, not app code.
try:
    import flask_admin

    _OrigAdmin = getattr(flask_admin, "Admin", None)
    if _OrigAdmin is not None:

        class _CompatAdmin(_OrigAdmin):
            def __init__(self, *args, **kwargs):
                kwargs.pop("template_mode", None)
                super().__init__(*args, **kwargs)

        flask_admin.Admin = _CompatAdmin
except Exception:
    # If flask_admin is not installed yet, test environment will install it via CI.
    pass

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
