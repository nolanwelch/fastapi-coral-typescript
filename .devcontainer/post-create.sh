#!/usr/bin/env bash
set -euo pipefail

PREFIX="[devcontainer]"

cd "$(git rev-parse --show-toplevel)"

echo "$PREFIX Starting post-create setup..."

# ─── 1. Install uv if not already present ───────────────────────────────────

if ! command -v uv &>/dev/null; then
    echo "$PREFIX Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # shellcheck source=/dev/null
    source "$HOME/.cargo/env"
fi

# ─── 2. Copy .env files from templates ──────────────────────────────────────

if [ -f backend/.env ]; then
    echo "$PREFIX   backend/.env already exists — skipping"
else
    cp backend/.env.example backend/.env
    echo "$PREFIX   Created backend/.env from backend/.env.example"
    # Point DATABASE_URL at the compose service hostname instead of localhost
    sed -i 's|@localhost:|@db:|' backend/.env
fi

if [ -f frontend/.env ]; then
    echo "$PREFIX   frontend/.env already exists — skipping"
else
    cp frontend/.env.example frontend/.env
    echo "$PREFIX   Created frontend/.env from frontend/.env.example"
fi

# ─── 3. Backend setup ───────────────────────────────────────────────────────

echo "$PREFIX Installing backend dependencies..."
(cd backend && uv sync)

echo "$PREFIX Installing pre-commit hooks..."
(cd backend && uv run pre-commit install)

# ─── 4. Frontend setup ──────────────────────────────────────────────────────

echo "$PREFIX Installing frontend dependencies..."
(cd frontend && npm ci)

# ─── 5. Run database migrations ─────────────────────────────────────────────

echo "$PREFIX Running database migrations..."
(cd backend && uv run alembic upgrade head)

# ─── 6. Generate OpenAPI schema and frontend client ─────────────────────────

echo "$PREFIX Generating OpenAPI schema and frontend client..."
./scripts/generate.sh

# ─── Done ────────────────────────────────────────────────────────────────────

echo "$PREFIX ✓ Ready. See README.md for how to start the services."
