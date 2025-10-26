#!/usr/bin/env bash
set -euo pipefail

echo "Setting up development environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_minimal.txt

echo "Database migrations (SQLite)"
export FLASK_APP=src/app.py
flask db upgrade || true

echo "Dev environment ready. Activate with: source .venv/bin/activate"
