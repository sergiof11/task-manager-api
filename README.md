# Task Manager API

[![CI](https://github.com/sergiof11/task-manager-api/actions/workflows/ci.yml/badge.svg)](https://github.com/sergiof11/task-manager-api/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue)

REST API for personal task management built with **FastAPI, PostgreSQL and SQLAlchemy**.

It provides secure JWT authentication, per-user task isolation, database migrations, automated testing, Docker support, continuous integration and cloud deployment.

## Live API

**Swagger UI**

https://task-manager-api-eb12.onrender.com/docs

> The API is hosted on Render's free tier, so the first request after a period of inactivity may take a short time while the service wakes up.

## API Features

- User registration and login
- Secure password hashing with Argon2
- JWT authentication with expiration
- Protected task endpoints
- Full task CRUD
- Per-user task ownership and isolation
- Pagination
- Filtering by completion status
- Input validation
- Consistent error handling

## Engineering & DevOps

- PostgreSQL persistence with SQLAlchemy
- Database migrations with Alembic
- Docker and Docker Compose
- Automated testing with pytest
- 100% coverage over `app/`
- Code quality checks with Ruff
- Continuous integration with GitHub Actions
- Cloud deployment with Render and Neon
- SSL database connections in production

## Tech Stack

| Area | Technologies |
|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn |
| Database | PostgreSQL, SQLAlchemy, psycopg |
| Validation & configuration | Pydantic, pydantic-settings |
| Authentication | PyJWT, Argon2, pwdlib |
| Migrations | Alembic |
| Testing | pytest, pytest-cov, httpx |
| Code quality | Ruff |
| Infrastructure | Docker, Docker Compose |
| Cloud | Render, Neon |
| CI | GitHub Actions |

## Project Structure

```text
task-manager-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── alembic/
│   ├── versions/
│   │   ├── 902afd450102_initial_schema.py
│   │   └── 5fc071f53c9f_add_user_to_tasks.py
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── users.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_health.py
│   ├── test_tasks_authorization.py
│   ├── test_tasks_crud.py
│   ├── test_tasks_filters.py
│   └── test_users.py
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Architecture

### Application

The application separates responsibilities across different modules:

- `routers/` — HTTP endpoints
- `schemas.py` — Request and response models
- `models.py` — SQLAlchemy database models
- `crud.py` — Database operations
- `dependencies.py` — Authentication dependencies
- `security.py` — Password hashing and JWT generation
- `config.py` — Environment-based configuration
- `database.py` — SQLAlchemy engine and sessions

### Production

```text
Client
  │
  ▼
Render
FastAPI + Docker
  │
  │ SSL
  ▼
Neon
PostgreSQL
```

Task ownership is derived from the authenticated JWT rather than from client input.

All task operations are scoped to the authenticated user. Resources that do not exist or belong to another user return `404 Not Found`, preventing the API from revealing the existence of other users' resources.

Alembic is used as the source of truth for database schema evolution.

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/users/register` | No | Register a user |
| `POST` | `/auth/login` | No | Authenticate and obtain a JWT |
| `GET` | `/auth/me` | Yes | Get the authenticated user |
| `GET` | `/tasks` | Yes | List the current user's tasks |
| `GET` | `/tasks/{task_id}` | Yes | Get a task |
| `POST` | `/tasks` | Yes | Create a task |
| `PUT` | `/tasks/{task_id}` | Yes | Update a task |
| `DELETE` | `/tasks/{task_id}` | Yes | Delete a task |
| `GET` | `/health` | No | Check API health |

### Pagination and Filtering

```http
GET /tasks?skip=0&limit=10
GET /tasks?completed=true
GET /tasks?completed=false
GET /tasks?completed=false&skip=0&limit=10
```

Default pagination values:

```text
skip = 0
limit = 10
```

The maximum allowed `limit` is `100`.

## Quick API Example

The following example uses the deployed API.

Set the base URL:

```bash
BASE_URL="https://task-manager-api-eb12.onrender.com"
```

### 1. Register a user

```bash
curl -X POST "$BASE_URL/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "strongpassword123"
  }'
```

### 2. Login

`/auth/login` expects a **JSON body**, not form data.

```bash
curl -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "strongpassword123"
  }'
```

A successful login returns:

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

Copy the returned token:

```bash
TOKEN="<access_token>"
```

### 3. Create a task

```bash
curl -X POST "$BASE_URL/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review FastAPI project",
    "completed": false
  }'
```

### 4. List your tasks

```bash
curl "$BASE_URL/tasks" \
  -H "Authorization: Bearer $TOKEN"
```

The complete API can also be tested through the public Swagger interface.

## Authentication and Authorization

A successful login returns a JWT containing:

- `sub` — Authenticated user ID
- `exp` — Token expiration time

Protected requests use:

```text
Authorization: Bearer <access_token>
```

The client never provides the task owner manually.

The authenticated user is obtained from the JWT, and every task operation is automatically scoped to that user.

## Configuration

Create a `.env` file based on `.env.example`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gestor_tareas
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_SSLMODE=prefer

JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The database names shown above are local defaults and can be changed through environment variables.

Production uses:

```text
DB_SSLMODE=require
```

to establish an SSL connection with Neon.

Secrets are provided through environment variables and are not committed to Git.

## Local Development

Clone the repository:

```bash
git clone https://github.com/sergiof11/task-manager-api.git
cd task-manager-api
```

Create a virtual environment:

```bash
python -m venv venv
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the local PostgreSQL databases:

```text
gestor_tareas
gestor_tareas_test
```

Apply database migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
python -m uvicorn app.main:app --reload
```

Swagger will be available at:

```text
http://127.0.0.1:8000/docs
```

## Docker

Docker Compose runs FastAPI and PostgreSQL as separate services.

Start the environment:

```bash
docker compose up --build
```

After the image has already been built:

```bash
docker compose up
```

Stop the containers:

```bash
docker compose down
```

PostgreSQL data is stored in a persistent Docker volume.

To also remove the stored database data:

```bash
docker compose down -v
```

Docker Compose waits for PostgreSQL to become healthy and applies Alembic migrations before starting Uvicorn.

## Tests and Code Quality

The current test suite contains:

```text
39 tests
100% coverage over app/
```

Run all tests:

```bash
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Run the same minimum coverage requirement used by CI:

```bash
python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

Run Ruff:

```bash
ruff check .
```

## Continuous Integration

GitHub Actions runs automatically on pushes and pull requests.

The CI workflow:

1. Starts an Ubuntu environment
2. Starts a temporary PostgreSQL database
3. Installs project dependencies
4. Runs Ruff
5. Applies Alembic migrations to an empty database
6. Runs the full test suite with coverage
7. Requires at least 90% coverage over `app/`

Workflow configuration:

```text
.github/workflows/ci.yml
```

## Cloud Deployment

The production API runs as a Dockerized FastAPI service on **Render**.

The production PostgreSQL database is hosted on **Neon** and connected through SSL.

Render uses `/health` as the service health check and automatically deploys new commits from the connected GitHub repository.

Production schema changes are reviewed and manually applied to Neon with Alembic before deployments that require database migrations.