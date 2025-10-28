"""Test shims used to adapt upstream APIs for the test environment."""

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
    pass
"""Test shims used to adapt upstream APIs for the test environment."""

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
    pass
