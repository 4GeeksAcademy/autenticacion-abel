Branch protection guidance
=========================

Recommended checks (use these exact check names when configuring GitHub branch protection for `main`):

- "Run tests (pytest)" — the workflow defined in `.github/workflows/tests.yml`.
- "requirements-check" — the workflow that validates pinned `requirements.txt` when run on the fix/requirements branch.
- "CI" — if present (some branches/workflows may also create a job called "CI").

How to enable branch protection (repo owner/admin required):

1. Go to the repository Settings → Branches → Branch protection rules.
2. Add a rule for `main`.
3. Enable "Require status checks to pass before merging".
4. In the list of checks, select the checks above (e.g. "Run tests (pytest)", "requirements-check", "CI").
5. Optionally require "Require branches to be up to date before merging".

Notes
- Only admins can add branch protection rules.
- If a check name does not appear immediately, wait until that workflow has run at least once on `main` (or a PR) so GitHub registers the check name.
- If flake8 is enabled in CI and failing on historical files, consider excluding generated files (migrations, docs) via `.flake8` before enabling strict checks.
