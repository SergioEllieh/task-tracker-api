# AGENTS.md

## Project Stack

- Backend: FastAPI
- Validation: Pydantic v2
- Storage: In-memory storage
- Frontend: Static HTML/CSS/JavaScript in `frontend/index.html`
- Tests: pytest + FastAPI TestClient
- CI: GitHub Actions
- Runtime: Uvicorn
- Containerization: Docker

## Run Commands

Start the API:

```powershell
uvicorn app.main:app --reload
```

Health check:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Run tests:

```powershell
pytest
```

Docker:

```powershell
docker build -t task-tracker-api .
docker run -p 8000:8000 task-tracker-api
```

## Project Rules

- Do not add new product features during the final project.
- Do not add authentication, a production database, notifications, or unrelated UI changes.
- Only change `app/` or `frontend/` for a small bug fix, security fix, or documentation-supported correction.
- Explain any final-project change to `app/` or `frontend/` in `docs/final-ai-review.md`.
- Do not add real secrets, tokens, `.env` values, credentials, production logs, or personal/customer data.

## Docs-First / Read-First Guardrails

- Read the relevant existing file before suggesting or making changes.
- Read `README.md` and relevant files in `docs/` before changing documented behavior.
- Inspect existing tests before changing application behavior.
- Do not rewrite unrelated files or sections.
- Prefer correcting documentation when the problem is documentation rather than changing working application code.

## Verification Rules

- Review AI-generated changes before accepting them.
- Run `pytest` after relevant changes.
- Verify `/health` when checking runtime behavior.
- Check GitHub Actions after CI changes.
- Reject AI suggestions that are incorrect, unnecessary, unsafe, or outside the project scope.

## Ownership Rule

Do not submit a code change, command, configuration choice, or AI suggestion that I cannot explain and defend.