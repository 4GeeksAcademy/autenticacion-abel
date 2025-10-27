"""Test fixtures for the application test suite."""

import importlib.util
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

_shims_path = os.path.join(os.path.dirname(__file__), "_shims.py")
_spec = importlib.util.spec_from_file_location("_test_shims", _shims_path)
_shims = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_shims)
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
