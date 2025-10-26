import os
import sys

# Ensure the repository's src/ is importable for tests
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

# Compatibility shim for upstream flask-admin API changes used only in tests.
try:
    import flask_admin

    _OrigAdmin = getattr(flask_admin, "Admin", None)
    if _OrigAdmin is not None:

        class _CompatAdmin(_OrigAdmin):
            def __init__(self, *args, **kwargs):
                # some versions accept template_mode; pop it if present
                kwargs.pop("template_mode", None)
                super().__init__(*args, **kwargs)

        flask_admin.Admin = _CompatAdmin
except Exception:
    # If flask_admin isn't installed in the environment yet, tests/install will
    # bring it in; ignore here to avoid import-time failures.
    pass
