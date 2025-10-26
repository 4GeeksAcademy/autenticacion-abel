import os
import sys
import json
import traceback

# make sure src is importable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
sys.path.insert(0, SRC)

# Compatibility shim: older code expects flask_admin.Admin to accept `template_mode` kwarg.
try:
    import flask_admin
    _OrigAdmin = getattr(flask_admin, 'Admin', None)
    if _OrigAdmin is not None:
        class _CompatAdmin(_OrigAdmin):
            def __init__(self, *args, **kwargs):
                kwargs.pop('template_mode', None)
                super().__init__(*args, **kwargs)
        flask_admin.Admin = _CompatAdmin
except Exception:
    # if flask_admin not installed yet, the test runner will fail later; ignore here
    pass

from app import app
from api.models import db


def run():
    db_path = '/tmp/test_autenticacion.db'
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except Exception:
        pass

    # ensure app uses the file DB
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['TESTING'] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

        client = app.test_client()

        print('1) POST /api/signup')
        signup_resp = client.post('/api/signup', json={
            'email': 'quicktest@example.com',
            'password': 's3cret'
        })
        print(signup_resp.status_code, signup_resp.get_data(as_text=True))

        print('\n2) POST /api/token')
        token_resp = client.post('/api/token', json={
            'email': 'quicktest@example.com',
            'password': 's3cret'
        })
        print(token_resp.status_code, token_resp.get_data(as_text=True))

        token_json = None
        try:
            token_json = token_resp.get_json()
        except Exception:
            pass

        token = None
        if token_json and 'token' in token_json:
            token = token_json['token']

        print('\n3) GET /api/private (with bearer token)')
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        private_resp = client.get('/api/private', headers=headers)
        print(private_resp.status_code, private_resp.get_data(as_text=True))

        # cleanup
        try:
            db.session.remove()
        except Exception:
            pass
    # remove DB file
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except Exception:
        pass


if __name__ == '__main__':
    try:
        run()
    except Exception:
        traceback.print_exc()
        sys.exit(2)
