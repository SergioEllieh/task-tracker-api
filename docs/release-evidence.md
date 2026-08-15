# Release Evidence

## Baseline
- Branch: final-project
- Date: 2026-08-10
- Local app run command: `uvicorn app.main:app --reload`
- /health result: `{"status":"ok","timestamp":"2026-08-10T14:31:43.930345+00:00"}` — API responded successfully.
- Frontend check: `Opened frontend/index.html in the browser. The Kanban board and create/edit task flow are still visible and working.`
- Test command: `pytest`
- Test result: `36 passed in 0.42s`


## CI evidence
- Workflow file: `.github/workflows/ci.yml`
- Latest run note: CI run #2 ("Finalize CI workflow") completed successfully on the `final-project` branch.
- Test command used by CI: `pytest -v`
- Shortcut check: No `continue-on-error`, no `|| true`, pytest is not skipped, Python version is pinned to `3.11`, and dependencies are installed before tests.


## Docker evidence

- Build command: `docker build -t task-tracker-api .`
- Build result: Successful (`15/15 FINISHED`), image created as `task-tracker-api:latest`.
- Run command: `docker run --name task-tracker-final -p 8000:8000 task-tracker-api`
- /health check: `curl.exe -i http://127.0.0.1:8000/health`
- /health result: `HTTP/1.1 200 OK` with `{"status":"ok","timestamp":"2026-08-11T08:08:23.215969+00:00"}`
- Non-root check: Dockerfile creates an `app` user and runs the container with `USER app`.
- No-baked-secrets check: `.dockerignore` excludes `.env` and `.env.*`, and the runtime stage copies only `app/` and `frontend/`.
- Runtime command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`


## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| The API starts with `uvicorn app.main:app --reload`. | Ran the command locally and confirmed successful application startup. | Verified | None |
| The `/health` endpoint returns HTTP 200. | Ran `curl.exe -i http://127.0.0.1:8000/health` and received `HTTP/1.1 200 OK`. | Verified | None |
| The test suite passes with `pytest`. | Ran the full test suite and received `36 passed`. | Verified | Removed the outdated README statement about a known failing test. |
| The Docker image builds and runs successfully. | Ran `docker build -t task-tracker-api .`, started the container, and verified `/health` returned HTTP 200. | Verified | None |
| CI runs the test suite successfully. | GitHub Actions CI run #2 completed successfully on `final-project`. | Verified | Finalized the dependency installation in `.github/workflows/ci.yml`. |
| README §7 claimed it was "unconfirmed" how CI's `pytest -v` step succeeds because `pytest`/`httpx` aren't in `requirements.txt`. | Read `.github/workflows/ci.yml`: the dependency step explicitly runs `pip install pytest httpx`. | Claim was wrong | Corrected README §7 to describe the actual workflow steps and removed the stale `[VERIFY]` marker. |
| README §8 claimed both `app/models/` and `app/storage/` exist as empty scaffold directories. | Listed the repository: only `app/storage/` (containing `.gitkeep`) exists; `app/models/` is not present. | Claim was wrong | Corrected README §8 to reference only `app/storage/`. |

## Re-verification (2026-08-15, macOS)

All baseline claims were re-verified from a clean checkout of `final-project` on macOS with Python 3.11 (the CI/Docker-pinned version):

- Setup: `python3.11 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`, `pip install pytest httpx`
- Tests: `pytest -v` → `36 passed in 0.15s`
- App: `uvicorn app.main:app --port 8000`; `curl -i http://127.0.0.1:8000/health` → `HTTP/1.1 200 OK`, body `{"status":"ok","timestamp":"2026-08-15T20:38:37.069028+00:00"}`
- Frontend: `GET /frontend/index.html` served by the API → HTTP 200 (39,685 bytes, Kanban board markup present); `POST /tasks` → HTTP 201 and the task appears in `GET /tasks`
- Docker: `docker build -t task-tracker-api .` → image `sha256:4d7281beef8a…`; `docker run -p 8001:8000 task-tracker-api` → `/health` HTTP 200; `docker exec <container> whoami` → `app` (non-root confirmed at runtime); container removed after the check
- Secret scan: no `.env` files tracked in the branch or anywhere in git history (`.env.example` contains only `PORT`/`APP_ENV` defaults); no credential assignments or token/key patterns (`AKIA…`, `ghp_…`, `sk-…`, private-key blocks) found in tracked files