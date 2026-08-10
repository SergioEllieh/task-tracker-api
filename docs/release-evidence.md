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
- Run command: `docker run -p 8000:8000 task-tracker-api`
- /health check: `curl.exe -i http://127.0.0.1:8000/health` returned `HTTP/1.1 200 OK`.
- Non-root check: Verified from `Dockerfile`; the runtime uses `USER app`.
- No-baked-secrets check: Verified from `.dockerignore`; `.env` and `.env.*` are excluded, and the runtime stage copies only `app/` and `frontend/`.
- Runtime command check: `uvicorn app.main:app --host 0.0.0.0 --port 8000` is explicitly defined in the Dockerfile.