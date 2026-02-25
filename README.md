# My App — Full-Stack Monorepo

A full-stack monorepo template with a **FastAPI** backend and a **React + TypeScript** frontend, connected via an OpenAPI-generated client.

## Local Development Setup

Run the one-liner from the repo root to get a fully working fullstack app:

```bash
./setup.sh
```

This script checks prerequisites, installs all dependencies, starts the database, runs migrations, generates the API client, and runs tests — no manual steps required.

### Prerequisites

Install these before running `setup.sh`:

- **Python 3.12+** — [python.org/downloads](https://www.python.org/downloads/)
- **uv** — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Node.js 18+** and **npm** — [nodejs.org](https://nodejs.org) or use [nvm](https://github.com/nvm-sh/nvm)
- **Docker** and **Docker Compose** (v2 plugin) — [docs.docker.com/get-docker](https://docs.docker.com/get-docker/)

### Environment files

The `.env` files (`backend/.env`, `frontend/.env`) are created by `setup.sh` from their `.env.example` templates. They are gitignored and never committed — each developer keeps their own local copy.

### Pre-commit hooks

The repo uses [pre-commit](https://pre-commit.com/) to catch issues before they reach CI. Hooks are installed automatically by `setup.sh`.

| Hook | Scope | What it catches |
| --- | --- | --- |
| **ruff (check)** | `backend/` | Python lint errors (auto-fixes where possible) |
| **ruff (format)** | `backend/` | Python formatting issues |
| **mypy** | `backend/` | Python type errors (strict mode) |
| **tsc** | `frontend/src/` | TypeScript type errors |
| **openapi-drift** | `backend/app/` | Schema or generated client out of sync with FastAPI app |
| **trailing-whitespace** | all files | Trailing whitespace |
| **end-of-file-fixer** | all files | Missing newline at end of file |

Run a single hook manually:

```bash
uv run pre-commit run <hook-id> --all-files
```

Skip hooks in an emergency (CI will still catch everything):

```bash
git commit --no-verify
```

## Stack

| Layer    | Technology                                           |
| -------- | ---------------------------------------------------- |
| Backend  | Python 3.12, FastAPI, SQLModel, Alembic, asyncpg     |
| Frontend | TypeScript, React 18, Vite, TanStack Query v5, Axios |
| Database | PostgreSQL 16                                        |
| API Gen  | @hey-api/openapi-ts                                  |

## Prerequisites

- **Python 3.12+** and [uv](https://docs.astral.sh/uv/) (backend package manager)
- **Node.js 20+** and npm (frontend)
- **PostgreSQL 16** (local dev) or **Docker** + **Docker Compose**

## Project Structure

```
├── backend/           # FastAPI application
├── frontend/          # React + Vite application
├── openapi.json       # Generated OpenAPI schema
├── scripts/
│   └── generate.sh    # Regenerate OpenAPI client
├── docker-compose.yml # Full stack via Docker
└── README.md
```

## Running Tests

### Backend Tests

```bash
cd backend

# Install dev dependencies
uv sync

# Run tests
uv run pytest
```

Tests use an in-memory SQLite database for isolation — no external database required.

### Frontend Type Checking

```bash
cd frontend
npm run typecheck
```

## Generating the API Client

The frontend API client is generated from the backend's OpenAPI schema. To regenerate after backend changes:

```bash
# From the project root
./scripts/generate.sh
```

This script:

1. Exports the OpenAPI schema from the FastAPI app to `openapi.json`
2. Generates TypeScript client code in `frontend/src/api/` using `@hey-api/openapi-ts`

Commit both `openapi.json` and the generated `src/api/` files together.

## Docker Compose

To run the entire stack with Docker:

```bash
docker compose up --build
```

| Service  | URL                    |
| -------- | ---------------------- |
| Frontend | http://localhost:3000  |
| Backend  | http://localhost:8000  |
| Database | localhost:5432         |

To stop all services:

```bash
docker compose down
```

To stop and remove volumes (clears database):

```bash
docker compose down -v
```

## API Endpoints

| Method   | Path              | Description      |
| -------- | ----------------- | ---------------- |
| `GET`    | `/users/`         | List all users   |
| `POST`   | `/users/`         | Create a user    |
| `GET`    | `/users/{id}`     | Get a user       |
| `PATCH`  | `/users/{id}`     | Update a user    |
| `DELETE` | `/users/{id}`     | Delete a user    |

## CI

This project uses GitHub Actions for continuous integration. All workflows run on push and pull requests to `main`.

| Workflow | File | What it checks |
| --- | --- | --- |
| **Backend Lint** | `backend-lint.yml` | Runs `ruff check` and `ruff format --check` on the backend |
| **Backend Typecheck** | `backend-typecheck.yml` | Runs `mypy` strict type checking on the backend |
| **Frontend Typecheck** | `frontend-typecheck.yml` | Runs `tsc --noEmit` on the frontend |
| **OpenAPI Drift Check** | `openapi-drift.yml` | Verifies the committed `openapi.json` matches what the FastAPI app generates |

### Reproduce locally

```bash
# Backend lint
cd backend
uv run ruff check .
uv run ruff format --check .

# Backend typecheck
cd backend
uv run mypy app

# Frontend typecheck
cd frontend
npm ci
npx tsc --noEmit

# OpenAPI drift check
cp openapi.json openapi.committed.json
cd backend && uv run python -m scripts.export_openapi && cd ..
diff openapi.committed.json openapi.json
```

## Linting

### Backend (Ruff)

```bash
cd backend
uv run ruff check .
```

### Frontend (TypeScript)

```bash
cd frontend
npx tsc --noEmit
```
