# Prompt Log

This document records the most significant AI prompts used during the implementation of Feature 1 (Due Dates + Overdue Filter). For each prompt, it includes the prompt, a summary of the AI response, and my review of what was accepted, edited, or rejected.

---

# Feature 1 – Due Dates + Overdue Filter

## Prompt 1 – Generate Reviewed User Stories

### Prompt

Generate user stories for the Due Dates + Overdue Filter feature.

- Backend: Python + FastAPI
- Validation: Pydantic v2
- Existing in-memory storage
- Existing frontend implementation
- Existing task fields:
  - id
  - title
  - description
  - status
  - priority
  - assignee
  - created_at
  - updated_at

New Feature:
- Add an optional due_date to tasks.
- Support creating tasks with a due date.
- Support updating or removing an existing due date.
- Allow users to identify overdue tasks.
- Allow users to filter overdue tasks.

Constraints:
- Generate exactly 3–5 user stories.
- Use "team member" as the user role.
- Include clear acceptance criteria.
- Include at least one failure case.
- Include AI assumptions.
- Wait for my review before generating implementation prompts.

Prompt refinements:

- Added frontend due-date field and HTTP 422 validation to the create story.
- Added edit modal behavior and HTTP 422 validation to the update story.
- Added frontend overdue-filter control to the filtering story.

### AI Response Summary

Generated four user stories covering task creation, updating/removing due dates, overdue detection, and overdue filtering, including acceptance criteria and AI assumptions.

### My Review

**Accepted**

- Story structure.
- Acceptance criteria.
- AI assumptions.

**Edited**

- Refined the stories by adding frontend requirements and HTTP 422 validation.

**Rejected**

- None.

---

## Prompt 2 – Add Backend Tests for Due Dates and Overdue Filtering

### Prompt

Add focused pytest coverage for Feature 1.

Requirements:

- Create task with valid due date.
- Create task without due date.
- Invalid due date returns HTTP 422.
- Update, change, and remove due dates.
- Verify overdue rules.
- Verify overdue filtering.
- Preserve existing tests.
- Modify only `tests/test_tasks.py`.

### AI Response Summary

Generated backend tests covering due-date creation, validation, updates, overdue calculation, and overdue filtering while preserving the existing test suite.

### My Review

**Accepted**

- Test coverage.
- Existing fixtures.
- Relative-date approach.

**Edited**

- None.

**Rejected**

- None.

---

## Prompt 3 – Add Due-Date Input to the Create/Edit Modal

### Prompt

Modify only `frontend/index.html` to:

- Add an optional date input.
- Support create and edit flows.
- Populate existing due dates.
- Allow clearing due dates.
- Preserve existing task behavior.
- Do not add overdue badge or filter yet.
- Update `docs/prompt-log.md`.

### AI Response Summary

Added an optional due-date field to the modal, integrated it into the create/edit workflows, and preserved the existing Kanban behavior.

### My Review

**Accepted**

- Optional date input.
- Payload handling.
- Modal reset.

**Edited**

- Moved the due date display to appear between the description and priority.

**Rejected**

- None.

---

## Prompt 4 – Add the Overdue Filter Control

### Prompt

Modify only `frontend/index.html` to:

- Add a "Show overdue tasks only" filter.
- Use `GET /tasks?overdue=true`.
- Preserve loading, retry, drag-and-drop, board rendering, due-date display, and overdue badges.
- Update `docs/prompt-log.md` and `docs/verification.md`.

### AI Response Summary

Added an overdue-filter control that uses the backend filtering endpoint while preserving the existing board behavior and task rendering.

### My Review

**Accepted**

- Backend-driven filtering.
- Existing board behavior.
- State preservation.

**Edited**

- None.

**Rejected**

- None.

# Feature 2 – Task Comments

## Prompt 1 – Generate Reviewed User Stories for Task Comments

### Prompt

```text
You are a Product Owner writing user stories for an existing software project.

Context

I am extending my existing Task Tracker project developed throughout Module 1, Module 2, and Module 3 of an AI-Assisted Coding course.

Current project:
- Backend: Python + FastAPI
- Validation: Pydantic v2
- Existing in-memory storage
- Existing frontend implementation
- Existing task fields:
  id
  title
  description
  status
  priority
  assignee
  created_at
  updated_at

Status values:
- ToDo
- InProgress
- Done

Priority values:
- Low
- Medium
- High

New Feature:
Task Comments

Feature requirements:
- Add a comment model or a task comment list.
- Support listing comments for a task.
- Support adding comments.
- Support deleting comments.
- Reject blank comments.
- Return HTTP 404 when the task or comment does not exist.
- Add a comments section in the existing edit modal or a small task details area.
- Optionally display the comment count on task cards.
- Keep the implementation small and consistent with the existing Task Tracker architecture.

Task

Generate user stories for Feature 2.

Constraints

- Generate exactly 3–5 user stories.
- Use "team member" as the user role.
- Every story must include clear, specific, and testable acceptance criteria.
- Acceptance criteria must be verifiable manually or through automated tests.
- Include at least one failure case across the generated stories.
- Ensure the stories cover both backend behavior and the required frontend behavior.
- Preserve the existing Task Tracker behavior unless a change is required for this feature.
- Do not introduce authentication, user accounts, notifications, real-time updates, databases, ORMs, Docker, background jobs, mobile applications, or unrelated features.
- Do not assume functionality that is not described above.
- If you make assumptions, list them explicitly.

Output format

For each story use exactly this format:

Story:
As a team member, I want ...

Acceptance Criteria:
- ...
- ...
- ...

After all stories, include a section titled:

AI Assumptions

List every assumption you made while generating the stories.

Wait for my review before generating the Mini-ADR.
```

### AI Response Summary

The AI generated four user stories covering viewing comments, adding comments, deleting comments, and consistent comment behavior across the application. It included testable acceptance criteria, frontend and backend behavior, failure cases, and a list of assumptions.

### My Review

**Accepted**
- The stories for viewing, adding, and deleting comments.
- The empty-state behavior.
- HTTP 404 handling for missing tasks and comments.
- The AI assumptions about in-memory storage and using the existing edit modal.

**Edited**
- Added that the API returns HTTP 422 when blank comment text is submitted.
- Reworded the API-focused story to be written from the team member’s perspective.
- Clarified that existing task behavior must remain unchanged.

**Rejected**
- The optional comment-count requirement was not implemented because it was not necessary for the required feature.

---

## Prompt 2 – Add In-Memory Comment Storage

### Prompt

```text
You are a senior Python/FastAPI backend engineer making one focused storage change to an existing Task Tracker project.

Context

I am implementing Feature 2:
Task Comments

Completed:
- CommentCreate and CommentResponse models exist in app/models.py.
- Feature 1 is complete and must remain unchanged.

Relevant files:
#app/storage.py
#app/models.py
#docs/user-stories.md
#docs/mini-adr.md
#docs/prompt-log.md

Task

Modify only app/storage.py to add in-memory comment storage and helper functions.

Required behavior

- Store comments in memory.
- Each comment must include:
  - id
  - task_id
  - text
  - created_at
- Add exactly these functions:
  - add_comment(task_id: str, payload: CommentCreate) -> Optional[CommentResponse]
  - get_comments_for_task(task_id: str) -> Optional[list[CommentResponse]]
  - delete_comment(task_id: str, comment_id: str) -> bool | None
- add_comment returns None if the task does not exist.
- get_comments_for_task returns None if the task does not exist.
- delete_comment returns:
  - None if the task does not exist
  - False if the task exists but the comment does not
  - True when the comment is deleted
- Preserve comment order from oldest to newest.
- Preserve all existing task storage behavior.
- _reset() must also clear comments.

Constraints

- Modify only app/storage.py.
- Do not add routes, tests, or frontend code.
- Do not change existing task function names or behavior.
- Use the existing in-memory approach.
- Do not add a database, ORM, classes, logging, or unrelated abstractions.

Output format

First provide:

## Storage Inspection Summary

Then return the full updated app/storage.py.

After the code, provide:

## Inspection Checklist

- Existing task storage preserved
- Comments stored in memory
- Missing task behavior is correct
- Missing comment behavior is correct
- Comment order preserved
- _reset() clears tasks and comments
- No route, test, or frontend changes

## Verification Commands

Provide small Python commands to verify:
1. Add comment to an existing task
2. Reject missing task
3. List comments
4. Delete existing comment
5. Delete missing comment
6. _reset() clears comments

Documentation Requirement

After completing this task:

1. Append a new section to docs/prompt-log.md.
2. Do not overwrite existing content.

The entry must include:

# F2.4 — Add In-Memory Comment Storage

## Objective
Summarize the purpose.

## Prompt
Paste the complete prompt.

## AI Response Summary
Summarize the storage changes.

## My Review

Accepted:
-everything

Edited:
-none

Rejected:
-none

Do not complete My Review.

Stop after updating app/storage.py and docs/prompt-log.md.
Do not proceed to routes, tests, or frontend work.
```

### AI Response Summary

The AI added in-memory comment storage and implemented helpers for adding, listing, and deleting comments. It preserved comment order, handled missing tasks and comments through the required return values, and updated `_reset()` to clear comment data.

### My Review

**Accepted**
- The in-memory comment storage design.
- The three requested storage functions.
- Missing-task and missing-comment return behavior.
- Oldest-to-newest comment ordering.
- Clearing comments inside `_reset()`.

**Edited**
- None.

**Rejected**
- None.

---

## Prompt 3 – Add Comment API Routes

### Prompt

```text
You are a senior Python/FastAPI backend engineer making one focused API change to an existing Task Tracker project.

Context

I am implementing Feature 2:
Task Comments

Completed:
- CommentCreate and CommentResponse models exist.
- In-memory comment storage functions exist.
- Feature 1 is complete and must remain unchanged.

Relevant files:
#app/main.py
#app/models.py
#app/storage.py
#docs/user-stories.md
#docs/mini-adr.md
#docs/prompt-log.md

Task

Modify only app/main.py to add comment API routes.

Required routes

1. List comments

GET /tasks/{task_id}/comments

Behavior:
- Return list[CommentResponse].
- Return HTTP 404 if the task does not exist.
- Return an empty list when the task exists but has no comments.

2. Add comment

POST /tasks/{task_id}/comments

Behavior:
- Accept CommentCreate.
- Return CommentResponse.
- Return HTTP 201 when created.
- Return HTTP 404 if the task does not exist.
- Blank or whitespace-only text must return HTTP 422 through Pydantic validation.

3. Delete comment

DELETE /tasks/{task_id}/comments/{comment_id}

Behavior:
- Return HTTP 204 when deleted.
- Return HTTP 404 if the task does not exist.
- Return HTTP 404 if the comment does not exist for that task.
- Return no response body on success.

Constraints

- Modify only app/main.py.
- Preserve all existing task routes and Feature 1 behavior.
- Use the existing storage functions.
- Do not duplicate comment validation in the route.
- Do not add comment update routes.
- Do not add author or authentication behavior.
- Do not modify models, storage, tests, or frontend files.
- Do not introduce routers, databases, ORMs, service layers, logging, or unrelated code.

Output format

First provide:

## API Inspection Summary

Include:
- Existing route structure
- Exact routes to add
- Required status codes
- Missing-task and missing-comment handling

Then return the full updated app/main.py.

After the code, provide:

## Inspection Checklist

- GET comments returns a list
- Existing task with no comments returns []
- Missing task returns 404
- POST comment returns 201
- Blank comment returns 422
- DELETE existing comment returns 204
- Missing task returns 404
- Missing comment returns 404
- Existing task routes remain unchanged
- No model, storage, test, or frontend changes

## Verification Commands

Provide curl or PowerShell commands to verify:

1. Create a task
2. List comments for that task
3. Add a valid comment
4. Reject a blank comment
5. Delete the comment
6. Return 404 for missing task
7. Return 404 for missing comment

Documentation Requirement

After completing this task:

1. Append a new section to docs/prompt-log.md.
2. Do not overwrite existing content.
3. Preserve Markdown formatting.

The entry must include:

# F2.5 — Add Comment API Routes

## Objective
Summarize the purpose.

## Prompt
Paste the complete prompt.

## AI Response Summary
Summarize the API routes added.

## My Review

Accepted:
-everything

Edited:
-none

Rejected:
-none

Do not complete My Review.

Stop after updating app/main.py and docs/prompt-log.md.
Do not proceed to tests or frontend work.
```

### AI Response Summary

The AI added endpoints for listing, creating, and deleting task comments. The routes used the existing Pydantic models and storage helpers, returned the required HTTP 201, 204, 404, and 422 responses, and preserved the existing task routes.

### My Review

**Accepted**
- The three comment endpoints.
- HTTP 201 for comment creation.
- HTTP 204 with no body for successful deletion.
- HTTP 404 handling for missing tasks and comments.
- Pydantic-driven HTTP 422 validation.

**Edited**
- None.

**Rejected**
- No comment update route was added because comment editing was outside the approved scope.

---

## Prompt 4 – Add Comments Section to the Edit Modal

### Prompt

```text
You are a senior frontend engineer making one focused UI change to an existing Task Tracker Kanban board.

Context

I am implementing Feature 2:
Task Comments

Completed backend work:
- CommentCreate and CommentResponse models exist.
- Comment storage exists.
- Comment API routes exist:
  - GET /tasks/{task_id}/comments
  - POST /tasks/{task_id}/comments
  - DELETE /tasks/{task_id}/comments/{comment_id}
- Feature 2 backend tests and Break Test are complete.
- Feature 1 must remain unchanged.

Current frontend:
- frontend/index.html
- Vanilla HTML, CSS, and JavaScript
- Existing create/edit modal
- Existing task form and API base URL
- Existing error-handling patterns

Relevant files:
#frontend/index.html
#app/main.py
#docs/user-stories.md
#docs/mini-adr.md
#docs/verification.md
#docs/prompt-log.md

Task

Modify only frontend/index.html to add a comments section to the existing edit modal.

Required behavior

1. Edit mode only
- Show the comments section only when editing an existing task.
- Do not show comments in create mode because no task ID exists yet.

2. List comments
- When the edit modal opens, fetch:
  GET /tasks/{task_id}/comments
- Display comments from oldest to newest.
- Each comment must show:
  - comment text
  - created_at in a readable format
  - Delete button
- Escape comment text before inserting it into the DOM.

3. Empty, loading, and error states
- Show a loading message while comments are being fetched.
- If the task has no comments, show:
  No comments yet
- If loading fails, show a comments-specific error message.
- Do not break the task-edit form when comment loading fails.

4. Add comment
- Add a textarea or text input and an Add Comment button.
- Submit to:
  POST /tasks/{task_id}/comments
- Trim the input before submitting.
- Do not submit an empty or whitespace-only comment.
- If the backend returns HTTP 422, show a clear validation message.
- After success:
  - clear the input,
  - refresh the comment list,
  - keep the edit modal open.

5. Delete comment
- Delete using:
  DELETE /tasks/{task_id}/comments/{comment_id}
- After HTTP 204, refresh the comment list.
- If deletion fails, show an appropriate comments-specific error.
- Keep the modal open.

6. Existing behavior
- Preserve the existing task update form.
- Preserve due date behavior.
- Preserve overdue filtering and badge behavior.
- Preserve modal open/close behavior.
- Preserve drag-and-drop and board rendering.

Constraints

- Modify only frontend/index.html.
- Do not modify backend files or tests.
- Do not add comment editing.
- Do not add authors, users, reactions, attachments, replies, or comment count yet.
- Do not introduce a framework, package, build tool, or new frontend file.
- Do not rewrite unrelated code.
- Reuse the existing API base URL and error-handling style.
- Keep comment logic separate enough that a comment failure does not block task editing.

Output format

First provide:

## Comments UI Inspection Summary

Include:
- Current modal structure
- Current edit-mode flow
- Exact locations that require changes
- How the active task ID will be reused
- Regression risks

Then apply the focused changes to frontend/index.html.

After the change, provide:

## Inspection Checklist

- Comments section appears only in edit mode
- GET comments runs when edit modal opens
- Loading state appears
- Empty state says “No comments yet”
- Comments display oldest to newest
- Comment text is escaped
- Valid comment can be added
- Blank comment is blocked
- HTTP 422 shows validation feedback
- Existing comment can be deleted
- Modal remains open after add/delete
- Task edit form still works
- Feature 1 behavior remains unchanged
- No backend or test files changed

## Manual Verification

1. Open the create modal and confirm comments are hidden.
2. Open an existing task with no comments.
3. Confirm “No comments yet” appears.
4. Add a valid comment.
5. Confirm it appears immediately.
6. Add a second comment and confirm oldest-to-newest order.
7. Submit blank or whitespace-only text.
8. Confirm no comment is created and validation is shown.
9. Delete one comment.
10. Confirm it disappears.
11. Edit and save the task itself.
12. Confirm due dates, overdue badges, filtering, and drag-and-drop still work.

Documentation Requirement

After completing this task:

1. Open docs/prompt-log.md.
2. Append a new section for this prompt.
3. Do not overwrite existing content.
4. Preserve valid Markdown formatting.

The new entry must include:

# F2.8 — Add Comments Section to the Edit Modal

## Objective
Summarize the purpose of this prompt.

## Prompt
Paste the complete prompt exactly as provided.

## AI Response Summary
Summarize the comments UI implementation.

## My Review

Accepted:
-

Edited:
-

Rejected:
-

Do not complete the My Review section.

After manual verification:

1. Open docs/verification.md.
2. Update Feature 2 Frontend Verification with:
   - comments section visibility,
   - loading state,
   - empty state,
   - add comment,
   - blank validation,
   - delete comment,
   - task-edit regression check.

Stop after updating frontend/index.html and docs/prompt-log.md.
Do not add comment count yet.
```

### AI Response Summary

The AI added an edit-only comments section to the existing task modal. It implemented comment loading, empty and error states, adding and deleting comments, whitespace validation, readable timestamps, and safe text rendering while preserving Feature 1 and the existing task form.

### My Review

**Accepted**
- The comments section inside the edit modal.
- Loading, empty, and error states.
- Adding and deleting comments.
- Safe rendering using text content.
- Preserving task editing and Feature 1 behavior.

**Edited**
- Fixed the modal integration because the comments section did not initially appear when editing a task.

**Rejected**
- Comment editing, authors, attachments, replies, reactions, and comment counts were not added because they were outside the selected feature scope.