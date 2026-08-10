# Personal AI Playbook

## When I Reach for AI First

I use AI first when I need help understanding an error, reviewing code, improving documentation, or checking configuration files. During this course, AI was especially useful for reviewing FastAPI code, writing and checking tests, troubleshooting errors, reviewing CI and Docker configuration, and organizing project documentation. I also use AI to suggest possible solutions when I am stuck, but I treat those suggestions as a starting point rather than the final answer.

## When I Do Not Reach for AI First

I do not rely on AI first when I need to understand an important concept myself or when the task involves sensitive information. I also avoid asking AI to make large changes without first understanding the existing code and project requirements. If AI does not have enough context about the repository, I prefer to inspect the relevant files before accepting its recommendations.

## My Non-Negotiables

- Never give AI passwords, API keys, tokens, `.env` values, credentials, or personal/customer data.
- Never accept AI-generated code or configuration without reviewing it.
- Verify important changes with tests, commands, runtime checks, or manual inspection.
- Do not allow AI to introduce features outside the requested project scope.
- I must be able to explain the work I submit, even when AI helped create or review it.

## My Review Rules

When AI suggests a change, I first compare it with the existing code and project requirements. I inspect the diff and make sure unrelated files or behavior were not changed. I run relevant commands such as `pytest`, runtime checks such as `/health`, and CI checks when appropriate. For AI review findings, I decide whether they are useful, noise, wrong, valid, or false positives instead of assuming every finding is correct. If a suggestion is incorrect, unnecessary, or outside the project scope, I reject or correct it.

## What I Am Still Figuring Out

I am still learning when AI should generate a solution and when it is better to use it only as a reviewer. I also want to improve how I provide repository context so AI suggestions are more accurate without giving it unnecessary or sensitive information. In a team environment, I would also want clear rules about how AI-generated changes should be documented and reviewed.

## Decision Card

| Situation | My Rule |
|---|---|
| New feature | Understand the requirement and existing code first, then use AI for focused assistance. |
| Code review | Let AI identify possible problems, but verify each finding myself. |
| Debugging | Give AI the error and relevant code, then test the proposed fix myself. |
| Infrastructure | Review AI-generated CI/Docker configuration carefully and verify it with real commands. |
| Never paste | Secrets, tokens, passwords, `.env` values, credentials, or personal/customer data. |
| One rule | If I cannot explain and verify an AI-generated change, I do not submit it. |