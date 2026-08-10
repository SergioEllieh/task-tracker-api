# CLAUDE.md

Guidance for Claude Code (and other AI agents) working in this repository.

## Project Overview

Task Tracker API — a FastAPI REST backend with a lightweight static HTML/JS frontend, built during the AI-Assisted Coding course and extended for the Mid-Course Project (due dates/overdue filter, search + combined filters).

- Backend entrypoint: `app/main.py`
- Domain logic: `app/business_rules.py`, `app/models.py`
- Persistence: `app/storage.py` (in-memory; reset via `storage._reset()`)
- Config: `app/core/config.py`
- Frontend: `frontend/index.html` (plain HTML/CSS/JS, calls the API directly)
- Tests: `tests/` (pytest + FastAPI `TestClient`)
- Docs: `docs/Mid-Course-Project/`

## Environment Setup

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 1. Tech Stack

- Python 3.11+ per README.md. `[VERIFY]` the project's `venv` interpreter currently reports 3.13.1 — confirm which version the course actually targets.
- FastAPI 0.115.6 (pinned in `requirements.txt`)
- Pydantic v2 — 2.10.4 (pinned in `requirements.txt`)
- Uvicorn 0.34.0, `uvicorn[standard]` (pinned in `requirements.txt`)
- pytest — installed in `venv`. `[VERIFY]` not currently pinned in `requirements.txt`.
- httpx — installed in `venv`, required by FastAPI's `TestClient`. `[VERIFY]` not currently pinned in `requirements.txt`.
- Frontend: vanilla HTML/CSS/JavaScript (`frontend/index.html`), no framework, no build step

## 2. Run Command

```powershell
uvicorn app.main:app --reload --port 8000
```

- App: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs

## 3. Test Command

```powershell
pytest -v
```

Known pre-existing failure: `tests/test_tasks.py::test_patch_same_status_returns_422` (actual 200). Not caused by unrelated changes — don't "fix" it incidentally while working on something else; call it out separately if addressing it.

## 4. Architecture Summary

- **Backend entrypoint**: `app/main.py` — FastAPI app, CORS middleware, task/comment routes, mounts `frontend/` as static files at `/frontend`
- **Task rules**: `app/business_rules.py` — `validate_status_transition()`; this is where task status transition rules live
- **Data models**: `app/models.py` — Pydantic models (`TaskCreate`, `TaskUpdate`, `TaskResponse`, `TaskStatus`, `TaskPriority`, `CommentCreate`, `CommentResponse`)
- **Persistence**: `app/storage.py` (in-memory; reset via `storage._reset()`, used as an autouse fixture in tests)
- **Config**: `app/core/config.py` — `Settings`/`get_settings()`, reads `APP_ENV`/`PORT` from environment/`.env`
- **Other routes**: `app/api/routes/health.py` (health check router included in `app/main.py`)
- **Frontend**: `frontend/index.html` — single-file HTML/CSS/JS Kanban board, calls the API directly via `fetch()`
- **Tests**: `tests/` (pytest + FastAPI `TestClient`) — `conftest.py`, `test_tasks.py`, `test_frontend.py`, `verify_a.py`
- **Docs**: `docs/Mid-Course-Project/`

## 5. Business Rules

Task status values (`app/models.py`, `TaskStatus` enum):
- `ToDo`
- `InProgress`
- `Done`

Status transition rules (`app/business_rules.py`, `VALID_TRANSITIONS`):
- `ToDo → InProgress`
- `InProgress → Done`
- `Done → InProgress`

Any transition not in this set (e.g. `ToDo → Done`, or re-setting the same status) raises a 422 via `validate_status_transition()`. `[VERIFY]` the known pre-existing failure in `test_patch_same_status_returns_422` suggests the same-status case may not currently 422 as expected — don't assume it's fixed.

Other implemented rules:
- `title` must be non-blank after stripping, max 200 characters (`TaskCreate`/`TaskUpdate` validators)
- comment `text` must be non-blank after stripping (`CommentCreate` validator)
- a task is `overdue` when `due_date` is set and earlier than the current UTC date (`app/storage.py::_is_overdue`)
- default `status` on creation is `ToDo`; default `priority` is `Medium`

## 6. UI States and CORS

UI states (`frontend/index.html`, `boardState` variable):
- `loading` — while `fetchTasks()` awaits the API response (skeleton board)
- `ready` — tasks returned and rendered onto the Kanban board
- `empty` — request succeeded but returned zero tasks
- `error` — request failed (network error or non-2xx response); shows a retry button

CORS (`app/main.py`, `CORSMiddleware`):
- Allowed origins: `http://localhost:5500`, `http://127.0.0.1:5500`, `http://localhost:5173`, and `null` (sent by browsers when `index.html` is opened directly as a `file://` page)
- All methods and headers allowed; credentials not allowed
- The frontend's `API_BASE_URL` is hardcoded to `http://127.0.0.1:8000` — the backend must run on that exact host/port for the frontend to work

## 7. Do-Not Rules

Do not do the following without explicitly asking first:
- Do not add authentication/authorization
- Do not add a database or other persistent storage (in-memory storage is intentional)
- Do not add deployment steps/configuration (Dockerfiles, CI/CD, hosting config, etc.)
- Do not make major UI changes to `frontend/index.html` (structural redesigns, new pages, framework adoption)

## Branch Conventions

- Default branch: `main`
- Active work happens on feature branches, e.g. `mid-course-project` (current branch, tied to PR #1)
- Do not push directly to `main`; open a PR from a feature branch instead
- Do not force-push or rewrite published history without explicit confirmation

## Ground Rules for AI Agents

- **Ask before editing**: propose changes and get explicit confirmation before modifying files, unless the user has clearly requested the edit in the current turn.
- **Ask before running tests** if the user hasn't requested it yet.
- **Never commit or push** without explicit user confirmation.
- **Never edit `.env`** or print its contents; use `.env.example` as the template for documenting required variables.
- Keep changes scoped to what's requested — avoid unrelated refactors or "improvements".
- Prefer editing existing files over creating new ones.
