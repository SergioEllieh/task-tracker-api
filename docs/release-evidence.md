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