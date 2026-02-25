# My App — Full-Stack Monorepo

A full-stack monorepo template with a **FastAPI** backend and a **React + TypeScript** frontend, connected via an OpenAPI-generated client.

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

## Local Development Setup

### 1. Database

Start a local PostgreSQL instance or use Docker:

```bash
docker compose up db -d
```

This starts PostgreSQL on port `5432` with user `postgres`, password `postgres`, and database `myapp`.

### 2. Backend

```bash
cd backend

# Copy env file and adjust if needed
cp .env.example .env

# Install dependencies with uv
uv sync

# Run the development server
uv run uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### 3. Frontend

```bash
cd frontend

# Copy env file
cp .env.example .env

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`.

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
