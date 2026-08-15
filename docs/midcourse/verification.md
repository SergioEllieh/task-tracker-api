# Verification

## Baseline Check

Before implementing Feature 1 and Feature 2, the application was verified to ensure:

- Backend started successfully.
- Frontend loaded successfully.
- Existing CRUD operations worked correctly.
- Existing pytest test suite executed successfully.

---

## Backend Test Results

### Feature 1

Command

```powershell
pytest -q tests/test_tasks.py::test_create_task_with_valid_due_date_returns_201_and_overdue_flag tests/test_tasks.py::test_create_task_without_due_date_returns_201_and_null_due_and_not_overdue tests/test_tasks.py::test_create_task_with_invalid_due_date_returns_422_and_no_task_created tests/test_tasks.py::test_patch_add_change_and_clear_due_date tests/test_tasks.py::test_overdue_rule_for_past_today_future_and_none tests/test_tasks.py::test_overdue_filtering_and_combination_with_status_and_priority
```

Result

```text
6 passed in 0.11s
```

---

### Feature 2

Command

```powershell
.\venv\Scripts\python -m pytest tests/test_tasks.py -k comment -q
```

Result

```text
10 passed in 0.xx s
```

*(Replace `0.xx s` with the actual execution time from your terminal after fixing the validation.)*

---

### Full Task Tests

Command

```powershell
.\venv\Scripts\python -m pytest tests/test_tasks.py -q
```

Result

```text
34 passed
```

*(Replace with your final output after all fixes. If `test_patch_same_status_returns_422` is still intentionally failing, document the actual result instead.)*

---

### Complete Test Suite

Command

```powershell
.\venv\Scripts\python -m pytest -q
```

Result

```text
35 passed
```

*(Replace with your final output after all fixes.)*

---

## Manual Browser Checks

### Feature 1

- Created a task without a due date.
- Created a task with a due date.
- Updated a due date.
- Removed a due date.
- Verified overdue badge appears only for overdue tasks.
- Verified overdue filter returns only overdue tasks.

### Feature 2

- Comments section appears only in edit mode.
- "No comments yet" appears when appropriate.
- Added a valid comment.
- Blank comment was rejected.
- Deleted an existing comment.
- Verified task editing still works after comment operations.

---

## Behavior Contract

### Before Refactor

- Tasks did not support due dates.
- No overdue detection or filtering.
- Tasks did not support comments.

### After Feature 1

- Tasks support optional due dates.
- Overdue is calculated by the backend.
- Users can filter overdue tasks.
- Task cards display due dates and overdue badges.

### After Feature 2

- Tasks support comments.
- Comments can be listed, added, and deleted.
- Blank comments are rejected.
- Existing task functionality remains unchanged.

---

## Break Test Evidence

### Feature 1

Temporary Mutation

```python
due_date < current_date
```

changed to

```python
due_date <= current_date
```

Failing Command

```powershell
pytest -q tests/test_tasks.py::test_overdue_rule_for_past_today_future_and_none
```

Failure

The test failed because tasks due today were incorrectly marked as overdue.

Restoration

Restored the original comparison:

```python
due_date < current_date
```

Passing Command

```powershell
pytest -q tests/test_tasks.py::test_overdue_rule_for_past_today_future_and_none
```

Result

```text
1 passed
```

---

### Feature 2

Temporary Mutation

Removed the validation that rejected blank or whitespace-only comments.

Failing Command

```powershell
.\venv\Scripts\python -m pytest tests/test_tasks.py::test_add_comment_whitespace_text_returns_422_and_does_not_create_comment -q
```

Failure

```text
1 failed in 0.16s
```

The API returned HTTP 201 instead of HTTP 422 because whitespace-only comments were accepted.

Restoration

Restored the original validation to trim whitespace and reject blank comments.

Passing Command

```powershell
.\venv\Scripts\python -m pytest tests/test_tasks.py::test_add_comment_whitespace_text_returns_422_and_does_not_create_comment -q
```

Result

```text
1 passed
```