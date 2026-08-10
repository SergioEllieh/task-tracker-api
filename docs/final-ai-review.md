# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log

Reviewed file: `.github/workflows/ci.yml`

| AI comment | Grade | Reason | Verification or decision |
|---|---|---|---|
| The workflow correctly runs on both `push` and `pull_request`. | Useful | This is required by the final project and ensures CI runs for direct pushes and pull requests. | Verified in `.github/workflows/ci.yml`. |
| Python is pinned to version `3.11` instead of using a vague version such as `3.x`. | Useful | A specific Python version makes CI more reproducible and satisfies the assignment's shortcut check. | Verified `python-version: "3.11"`. |
| `pytest` and `httpx` are installed separately from `requirements.txt`, which duplicates dependency management. | Useful | These packages are needed for the tests but are not currently pinned in `requirements.txt`, so the CI installation is necessary for the current repository even though centralizing test dependencies could be cleaner. | Kept the explicit installation so the CI workflow can run the test suite reliably. |


## AI security mini-review

| Finding | File evidence | Grade | Reason | Next action |
|---|---|---|---|---|
| The Docker container is configured to run as a non-root user. | `Dockerfile` creates the `app` user and uses `USER app`. | Valid | Running as a non-root user reduces container privileges. | Keep the non-root configuration. |
| Environment files are excluded from the Docker build context. | `.dockerignore` contains `.env` and `.env.*`. | Valid | This helps prevent environment values or secrets from being accidentally included in the Docker image. | Keep these exclusions and never commit real secrets. |
| CORS configuration is permissive for the course frontend. | `app/main.py` includes `"null"` as an allowed origin and uses `allow_methods=["*"]` and `allow_headers=["*"]`. | Valid | This is intentionally permissive because the frontend can be opened directly from `frontend/index.html`, but it would need reconsideration for production. | Keep it for the current course project; review before any production deployment. |
| Task and comment endpoints do not require authentication. | `app/main.py` exposes task/comment routes without authentication dependencies. | False Positive | Authentication is intentionally outside the scope of this course project, so adding it now would violate the final-project scope. | Do not add authentication. |


## Manual security check

I manually reviewed the repository for `.env` files, hard-coded passwords, API keys, tokens, credentials, and personal/customer data. I did not find any real secrets or personal/customer data in the reviewed repository files. I also confirmed that `.dockerignore` excludes `.env` and `.env.*` from the Docker build context.


## One AI output I rejected or corrected

During the Docker review, AI-generated/reviewed Docker configuration contained escaped colons such as `--chown=app\:app` and `app.main\:app`. I did not accept this output as-is because the Dockerfile should use normal colons in these values. I corrected them to `--chown=app:app` and `app.main:app` before treating the Dockerfile as final. This reinforced my rule that AI-generated configuration must be checked against the actual syntax before it is accepted.


## Three AI Usage Rules

1. **Never paste:** I will never paste real passwords, API keys, tokens, `.env` values, credentials, production logs, or personal/customer data into AI tools.

2. **Always verify:** I will review AI-generated code and configuration before accepting it and verify important changes using tests, commands, runtime checks, or manual inspection.

3. **Record AI contributions by:** I will document where AI was used, what it suggested, how I verified the suggestion, and whether I accepted, corrected, downgraded, or rejected it.


## Ownership Statement

I am comfortable submitting this repository as my own work because I reviewed and verified the final changes instead of accepting AI output blindly. I ran the application, checked the `/health` endpoint, ran the full test suite, and reviewed the CI and project configuration. When AI suggestions were incorrect or unnecessary, I corrected or rejected them rather than applying them automatically. I understand the main code, commands, configuration choices, and documentation included in this final submission.