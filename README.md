# Task Tracker API

## 1. Project Overview

Task Tracker API is a FastAPI REST backend with a lightweight static HTML/JS frontend, built during the AI-Assisted Coding course and extended for the Mid-Course Project (due dates + overdue filter, combined filters, task comments).

* **Backend**: FastAPI + Pydantic v2, in-memory storage (no database)
* **Frontend**: a single static file (`frontend/index.html`) that calls the API directly with `fetch()` — no build step, no framework
* **Tests**: pytest + FastAPI `TestClient`

This project does not implement authentication, a persistent database, or deployment/production configuration — see [Section 9](#9-project-conventions-and-current-limitations).

## 2. Prerequisites

* Python 3.11 — this is the version pinned in CI and the Dockerfile and the verified baseline; newer 3.x versions have also been observed to work locally.
* `pip` (bundled with Python)
* Docker Desktop — only needed if you plan to run the container (see [Section 6](#6-run-with-docker))

## 3. Local Setup

Run these from the repository root.

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS/Linux, activate with `source venv/bin/activate` instead (and use plain `curl` wherever this README shows `curl.exe`).

`pytest` and `httpx` (required to run the test suite) are **not** pinned in `requirements.txt` (verified — see `docs/release-evidence.md`). Install them explicitly if you plan to run tests, exactly as CI does:

```powershell
pip install pytest httpx
```

Copy the example environment file if you want to override the defaults (`APP_ENV=development`, `PORT=8000`):

```powershell
Copy-Item .env.example .env
```

## 4. Run the App Locally

```powershell
uvicorn app.main:app --reload --port 8000
```

* App/API: http://127.0.0.1:8000
* Interactive docs: http://127.0.0.1:8000/docs
* Frontend (served by the API via `StaticFiles`): http://127.0.0.1:8000/frontend/index.html — you can also open `frontend/index.html` directly in a browser (the API's CORS config explicitly allows the `null` origin this produces)

The frontend's `API_BASE_URL` is hardcoded to `http://127.0.0.1:8000`, so the backend must run on that exact host/port for the frontend to work.

## 5. Run Tests

```powershell
pytest -v
```

`tests/verify_a.py` is a standalone manual verification script for `app/models.py` (not picked up by pytest's default `test_*` discovery); run it directly if needed:

```powershell
python tests/verify_a.py
```

## 6. Run with Docker

```powershell
docker build -t task-tracker-api .
docker run -p 8000:8000 task-tracker-api
```

Then visit http://127.0.0.1:8000/docs.

Notes:

* The image is a multi-stage build (`python:3.11-slim`) that installs dependencies as a non-root `app` user and copies only `app/` and `frontend/` into the runtime stage.
* `.env` is **not** copied into the image; the container runs with the defaults baked into `app/core/config.py` (`APP_ENV=development`, `PORT=8000`) unless you pass `-e` flags.
* The container's `CMD` hardcodes `--port 8000` (verified in the `Dockerfile`); passing `-e PORT=...` will not change the port the server actually listens on inside the container — map the container's fixed port 8000 to a host port with `-p <host_port>:8000` instead.

## 7. CI Workflow Summary

Defined in [.github/workflows/ci.yml](.github/workflows/ci.yml), the `CI` workflow runs on every `push` and `pull_request`:

1. Checks out the repository (`actions/checkout@v4`)
2. Sets up Python 3.11 (`actions/setup-python@v5`)
3. Upgrades `pip`
4. Installs dependencies with `pip install -r requirements.txt` followed by `pip install pytest httpx`
5. Runs `pytest -v`

Because `pytest`/`httpx` aren't pinned in `requirements.txt` (see [Section 3](#3-local-setup)), the workflow installs them explicitly in the dependency step — this was checked against the actual `ci.yml` (see the claim-vs-reality log in `docs/release-evidence.md`).

## 8. Project Structure

```text
app/
  main.py            FastAPI app, CORS, task/comment routes, mounts frontend/ as static files
  business_rules.py  validate_status_transition() — task status transition rules
  models.py          Pydantic models (TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority, CommentCreate, CommentResponse)
  storage.py         In-memory persistence; reset via storage._reset()
  core/config.py     Settings/get_settings() — reads APP_ENV/PORT from environment/.env
  api/routes/health.py  Health check router
  schemas/health.py  HealthResponse model used by the health route
  storage/           Empty scaffold directory (.gitkeep only), unused by current code
frontend/
  index.html         Single-file HTML/CSS/JS Kanban board; calls the API via fetch()
tests/
  conftest.py        TestClient + storage._reset() autouse fixture
  test_tasks.py      Task/status-transition tests
  test_frontend.py   Frontend-serving tests
  verify_a.py        Standalone manual verification script (not pytest-discovered)
docs/Mid-Course-Project/
  mini-adr.md, prompt-log.md, reflections.md, user-stories.md, verification.md
Dockerfile           Multi-stage build, non-root user, exposes 8000
requirements.txt     Pinned runtime dependencies
```

## 9. Project Conventions and Current Limitations

* **Storage is in-memory only** — all tasks/comments are lost on restart; `storage._reset()` is used as an autouse fixture in tests.
* **Status transitions** (`app/business_rules.py`, `VALID_TRANSITIONS`): only `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress` are valid. Any other transition (e.g. `ToDo → Done`, or re-setting the same status) raises HTTP 422.
* **Validation rules**: task `title` must be non-blank after stripping (max 200 characters); comment `text` must be non-blank after stripping.
* **Overdue tasks**: a task is `overdue` when `due_date` is set and earlier than the current UTC date.
* **CORS**: allowed origins are `http://localhost:5500`, `http://127.0.0.1:5500`, `http://localhost:5173`, and `null` (for `file://` access); all methods/headers are allowed, credentials are not.
* **No authentication, no database, no deployment configuration** are implemented, and none should be added without explicit confirmation.
* **No major UI redesigns** (new pages, framework adoption) to `frontend/index.html` without explicit confirmation.

## 10. Technical Decisions

See [docs/Mid-Course-Project/mini-adr.md](docs/Mid-Course-Project/mini-adr.md) for the mini-ADR covering the due dates/overdue filter and task comments features (context, decisions, alternatives considered, and consequences). Related docs: [user-stories.md](docs/Mid-Course-Project/user-stories.md), [prompt-log.md](docs/Mid-Course-Project/prompt-log.md), [verification.md](docs/Mid-Course-Project/verification.md), [reflections.md](docs/Mid-Course-Project/reflections.md).

## 11. Final Project

**Branch reviewed:** `final-project`

### What This Submission Demonstrates

- The existing Task Tracker app still runs inside the intended course scope.
- The API starts successfully and the `/health` endpoint responds correctly.
- The Kanban board and create/edit task flow are still visible and working.
- The full pytest suite passes.
- CI runs the pytest suite on push and pull request (see [.github/workflows/ci.yml](.github/workflows/ci.yml)).
- The Docker image builds and runs, with `/health` returning HTTP 200.
- AI review, security, and ownership evidence is documented in the `docs/` directory.

### How to Run Locally

From the repository root:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health check:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Verified baseline result (re-verified 2026-08-15 on macOS with Python 3.11):

```json
{"status":"ok","timestamp":"2026-08-15T20:38:37.069028+00:00"}
```

### How to Run Tests

```powershell
pytest
```

Verified baseline result (re-verified 2026-08-15):

```text
36 passed in 0.15s
```

### How to Run with Docker

```powershell
docker build -t task-tracker-api .
docker run -p 8000:8000 task-tracker-api
```

Docker runtime verification is documented separately in `docs/release-evidence.md`.

### Evidence Files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

### AI Assistance Summary

AI helped draft or review: release documentation, CI/Docker configuration, code review, and security review.

I verified the work by: running the full test suite, checking `/health`, reviewing repository diffs, verifying the Docker build/run, and a manual scan for secrets/credentials.

One AI suggestion I rejected or corrected: the Dockerfile review initially produced escaped colons (`--chown=app\:app`, `app.main\:app`); I corrected these to `app:app` and `app.main:app` before accepting the file. Full details in [docs/final-ai-review.md](docs/final-ai-review.md).