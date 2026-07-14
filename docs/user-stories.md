> Due Dates + Overdue Filter User Stories
Story 1:
As a team member, I want to create a task with an optional due date so that I
can record deadlines when needed.
Acceptance Criteria:
- The create-task modal includes an optional due-date field that can be left empty or filled in when creating a task.
- A task can be created successfully with a valid due date and the stored task returns that due date.
- A task can be created successfully without a due date and the task is still created successfully.
- An invalid due-date value returns HTTP 422 and the task is not created.
- The existing task fields remain available and unchanged when due date support is added.


Story 2:
As a team member, I want to update or remove a task’s due date so that I can
keep deadlines accurate as requirements change.
Acceptance Criteria:
- The edit modal displays the task’s current due date when one exists.
- An existing task can be updated to set a due date when it previously had none.
- An existing task can be updated to change its due date to a different date.
- An existing task can be updated to remove its due date and the stored task no longer has a due date value.
- If an invalid due date is submitted, the update returns HTTP 422 and the stored task remains unchanged.


Story 3:
As a team member, I want to identify overdue tasks so that I can quickly see
which tasks need attention.
Acceptance Criteria:
- A task with a due date earlier than the current date is identified as overdue.
- A task with a due date later than the current date is not identified as overdue.
- A task without a due date is not identified as overdue.
- Overdue status is visible through the existing task retrieval flow.


Story 4:
As a team member, I want to filter the task list to show only overdue tasks so
that I can focus on time-sensitive work.
Acceptance Criteria:
- The frontend includes an overdue-filter control that allows a user to request only overdue tasks.
- When the overdue filter is applied, only tasks with due dates earlier than the current date are returned.
- Tasks due today, future tasks, and tasks without due dates are excluded from the filtered results.
- When the overdue filter is not applied, the existing task list behavior remains unchanged.

> Task Comments User Stories

Story 1:
As a team member, I want to view comments associated with a task so that I can review task context without leaving the task details view.
Acceptance Criteria:
- When I open an existing task, the task details area or edit modal shows a comments section that lists all comments currently attached to that task.
- If a task has no comments, the comments section displays an empty state such as “No comments yet” and the task remains accessible.
- The task card optionally displays the number of comments associated with the task.
- The new comments section does not change the existing task fields, task list behavior, or task update flow for tasks without comments.

Story 2:
As a team member, I want to add a comment to a task so that I can record additional context for the task.
Acceptance Criteria:
- When I enter a non-blank comment in the comments section and submit it, the comment is saved to the task and appears in the comments list immediately.
- When I submit a comment containing only whitespace or an empty value, the API returns HTTP 422 and the UI displays an appropriate validation message.
- The comment is associated with the correct task and does not affect other tasks in the list.

Story 3:
As a team member, I want to delete a comment from a task so that I can remove outdated or incorrect notes.
Acceptance Criteria:
- When I delete an existing comment from the comments list, the comment is removed from the task and no longer appears in the UI.
- When I attempt to delete a comment for a task that does not exist, the system returns HTTP 404 and the UI shows an appropriate error state.
- When I attempt to delete a comment that does not exist for a valid task, the system returns HTTP 404 and the comment list remains unchanged.

Story 4:
As a team member, I want comments to remain available whenever I view a task so that I have a consistent experience regardless of whether the task contains comments.
Acceptance Criteria:
- Tasks with comments behave correctly.
- Tasks without comments continue to work normally.
- Existing task operations remain unchanged.
- Comment operations return the expected responses.


In feature 1, I edited stories 1, 2 and 4

In feature 2, I edited stories 1, 2 and 4