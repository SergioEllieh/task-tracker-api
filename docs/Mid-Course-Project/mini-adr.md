# Mini-ADR

## Overview

This ADR extends the existing Task Tracker with two small, user-facing features that fit the current FastAPI, Pydantic, and in-memory storage architecture: optional due dates with overdue detection, and task comments. Both additions preserve the current application structure while supporting the approved user stories without introducing new frameworks or data storage layers.

## Feature 1 – Due Dates + Overdue Filter

### Context

Users need a lightweight way to attach deadlines to tasks and quickly identify time-sensitive work. The approved stories require optional due dates, create/update/remove support, overdue detection, and a filter for overdue tasks while preserving existing task behavior.

### Decision

Due dates will be represented as an optional date field on the task model and validated with Pydantic so invalid values are rejected with HTTP 422. Overdue status will be calculated by the backend whenever tasks are returned, because the backend already owns task state and can apply the same logic consistently to list and detail responses. The frontend will add a simple due-date field to the create/edit forms and a filter control for requesting only overdue tasks. This keeps the feature small, predictable, and aligned with the existing request/response flow.

### Alternatives Considered

- Keeping due dates only in the frontend: simple at first, but it would duplicate logic and make overdue results inconsistent.
- Adding a separate overdue entity or dedicated scheduling subsystem: more flexible, but unnecessary for the current scope.
- Storing due dates as free-form strings: easier to implement initially, but less reliable and harder to validate.

### Rejected Alternatives

- A full calendar or reminder system was rejected because it would expand scope beyond the approved stories.
- A database-backed redesign was rejected because the current in-memory storage already meets the requirements for this feature.

### Consequences

- Backend: one optional field, small validation rules, and straightforward overdue calculation.
- Frontend: minor form and filter updates with no structural redesign.
- Testing: validation, create/update/remove, and filtering scenarios should be covered.
- Maintainability: the design remains easy to understand and consistent with the current architecture.

## Feature 2 – Task Comments

### Context

Users need a lightweight way to attach task context without introducing broader workflow features. The approved stories require listing comments, adding comments, deleting comments, rejecting blank input, handling missing resources with HTTP 404, and showing comments in the task UI.

### Decision

Comments will be modeled as a small list attached to each task, stored in memory alongside the task. The backend will expose list, add, and delete operations through the existing task routes, with validation rejecting blank or whitespace-only comments and returning HTTP 404 for missing tasks or comments. The frontend will add a comments section in the existing task edit/details area and optionally show a comment count on task cards. This approach keeps comment handling local to the task lifecycle and avoids introducing separate resources or new architectural layers.

### Alternatives Considered

- A separate comments resource with its own endpoint hierarchy: more modular, but heavier than required for this project.
- A richer threaded or user-attributed comment system: useful in larger products, but not supported by the stories and too complex for the current scope.

### Rejected Alternatives

- Authentication or user accounts for comments were rejected because the stories do not require identity or permissions.
- Moving comments into a database or ORM layer was rejected because the current storage approach is sufficient and the feature is intentionally small.

### Consequences

- Backend: small route and validation additions around the existing task model.
- Frontend: lightweight comments UI with empty states and error handling.
- Testing: create, delete, blank input, and 404 scenarios should be covered.
- Maintainability: the feature stays compact, understandable, and consistent with the project’s existing organization.

## My Review

Accepted: Everything
-

Edited:
-

Rejected:
-

Reason:
-
