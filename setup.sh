#!/usr/bin/env bash
set -euo pipefail

PREFIX="[setup]"

# ─── 1. Check prerequisites ─────────────────────────────────────────────────

echo "$PREFIX Checking prerequisites..."

errors=()

# Python 3.12+
if command -v python3 &>/dev/null; then
    py_version=$(python3 --version 2>&1 | awk '{print $2}')
    py_minor=$(echo "$py_version" | cut -d. -f2)
    if [ "$py_minor" -lt 12 ]; then
        errors+=("  - python3 >= 3.12 required (found $py_version). Install from https://www.python.org/downloads/")
    fi
else
    errors+=("  - python3 is not installed. Install from https://www.python.org/downloads/")
fi

# uv
if ! command -v uv &>/dev/null; then
    errors+=("  - uv is not installed. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
fi

# Node.js 18+
if command -v node &>/dev/null; then
    node_major=$(node --version | sed 's/^v//' | cut -d. -f1)
    if [ "$node_major" -lt 18 ]; then
        errors+=("  - node >= 18 required (found $(node --version)). Install from https://nodejs.org or use nvm")
    fi
else
    errors+=("  - node is not installed. Install from https://nodejs.org or use nvm")
fi

# npm
if ! command -v npm &>/dev/null; then
    errors+=("  - npm is not installed. Install from https://nodejs.org or use nvm")
fi

# docker
if ! command -v docker &>/dev/null; then
    errors+=("  - docker is not installed. Install from https://docs.docker.com/get-docker/")
fi

# docker compose (v2 plugin)
if ! docker compose version &>/dev/null 2>&1; then
    errors+=("  - docker compose (v2 plugin) is not available. Install from https://docs.docker.com/get-docker/")
fi

if [ ${#errors[@]} -gt 0 ]; then
    echo ""
    echo "$PREFIX Missing prerequisites:"
    for err in "${errors[@]}"; do
        echo "$err"
    done
    echo ""
    echo "$PREFIX Please install the missing tools and re-run this script."
    exit 1
fi

echo "$PREFIX All prerequisites found."

# ─── 2. Copy .env files ─────────────────────────────────────────────────────

echo "$PREFIX Copying .env files..."

if [ -f backend/.env ]; then
    echo "$PREFIX   backend/.env already exists — skipping"
else
    cp backend/.env.example backend/.env
    echo "$PREFIX   Created backend/.env from backend/.env.example"
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

# ─── 5. Start Docker services (DB only) ─────────────────────────────────────

echo "$PREFIX Starting PostgreSQL container..."
docker compose up -d db

echo "$PREFIX Waiting for PostgreSQL to be ready..."
attempts=0
max_attempts=30
until docker compose exec db pg_isready -U postgres &>/dev/null; do
    attempts=$((attempts + 1))
    if [ "$attempts" -ge "$max_attempts" ]; then
        echo "$PREFIX ERROR: PostgreSQL did not become ready within ${max_attempts} seconds."
        exit 1
    fi
    sleep 1
done
echo "$PREFIX PostgreSQL is ready."

# ─── 6. Run backend migrations ──────────────────────────────────────────────

echo "$PREFIX Running database migrations..."
(cd backend && uv run alembic upgrade head)

# ─── 7. Generate OpenAPI schema and frontend client ─────────────────────────

echo "$PREFIX Generating OpenAPI schema and frontend client..."
./scripts/generate.sh

# ─── 8. Run tests ───────────────────────────────────────────────────────────

echo "$PREFIX Running backend tests..."
(cd backend && uv run pytest tests/ -q) || true
echo ""
echo "  If tests failed, check the output above before committing."

# ─── 9. Done ────────────────────────────────────────────────────────────────

echo ""
cat <<'BANNER'
╔════════════════════════════════════════╗
║  Setup complete!                       ║
╠════════════════════════════════════════╣
║  Start everything:                     ║
║    docker compose up                   ║
║                                        ║
║  Or run services individually:         ║
║    Backend:  cd backend && uv run      ║
║              uvicorn app.main:app      ║
║              --reload                  ║
║    Frontend: cd frontend && npm run dev║
║                                        ║
║  Backend:   http://localhost:8000      ║
║  Docs:      http://localhost:8000/docs ║
║  Frontend:  http://localhost:5173      ║
╚════════════════════════════════════════╝
BANNER
