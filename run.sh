#!/usr/bin/env bash
# Build the frontend and run the unified FastAPI server on :8000.
# Usage: ./run.sh [--skip-build]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PORT="${PORT:-8000}"

if [[ "${1:-}" != "--skip-build" ]]; then
  echo "==> Installing frontend deps & building"
  (cd "$ROOT/frontend" && npm install --silent && npm run build)
fi

echo "==> Installing backend deps"
pip install --quiet -r "$ROOT/backend/requirements.txt"

echo "==> Starting server on http://localhost:$PORT"
cd "$ROOT/backend"
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
