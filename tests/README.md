# Tests

This project includes a small pytest-based test to validate the authentication
flow (signup -> token -> private).

Run tests locally:

```bash
python -m pip install -r requirements_minimal.txt pytest
pytest -q
```

Formatting and linting

We use Black (line-length 88), isort and flake8. To run locally:

```bash
python -m pip install black isort flake8
isort --profile black src tests
black --line-length 88 src tests
flake8 src tests
```

You can also install and enable pre-commit hooks (recommended):

```bash
python -m pip install pre-commit
pre-commit install
pre-commit run --all-files
```

If you already have pre-commit installed, run `pre-commit run --all-files` after pulling changes to ensure your working tree matches the repository style.
