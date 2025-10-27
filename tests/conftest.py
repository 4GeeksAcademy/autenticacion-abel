"""Test fixtures for the application test suite."""

import os
import sys

import pytest

import tests._shims as _shims

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

_ = _shims


@pytest.fixture
def client(tmp_path):
    """Provide a Flask test client with a temporary SQLite database."""
    from api.models import db
    from app import app

    db_path = tmp_path / "test.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(db_path)
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
