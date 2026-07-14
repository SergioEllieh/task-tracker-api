from datetime import date, datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from app.models import CommentCreate, CommentResponse, TaskCreate, TaskResponse, TaskUpdate

_tasks: dict[str, dict[str, Any]] = {}
_comments: dict[str, list[dict[str, Any]]] = {}


def _get_current_utc_date() -> date:
    return datetime.now(timezone.utc).date()


def _is_overdue(due_date: Optional[date], current_date: Optional[date] = None) -> bool:
    if due_date is None:
        return False
    if current_date is None:
        current_date = _get_current_utc_date()
    return due_date < current_date


def _to_response(task_data: dict[str, Any], current_date: Optional[date] = None) -> TaskResponse:
    return TaskResponse(
        id=task_data["id"],
        title=task_data["title"],
        description=task_data["description"],
        status=task_data["status"],
        priority=task_data["priority"],
        assignee=task_data["assignee"],
        due_date=task_data["due_date"],
        overdue=_is_overdue(task_data["due_date"], current_date),
        created_at=task_data["created_at"],
        updated_at=task_data["updated_at"],
    )


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    task_id = str(uuid4())
    task_data = {
        "id": task_id,
        "title": payload.title,
        "description": payload.description or "",
        "status": payload.status,
        "priority": payload.priority,
        "assignee": payload.assignee,
        "due_date": payload.due_date,
        "created_at": now,
        "updated_at": now,
    }
    _tasks[task_id] = task_data
    return _to_response(task_data, now.date())


def get_all_tasks(status=None, priority=None) -> list[TaskResponse]:
    tasks = [_to_response(task_data) for task_data in _tasks.values()]
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    if priority is not None:
        tasks = [t for t in tasks if t.priority == priority]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    task_data = _tasks.get(task_id)
    if task_data is None:
        return None
    return _to_response(task_data)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    task_data = _tasks.get(task_id)
    if task_data is None:
        return None
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return _to_response(task_data)
    updated_task_data = {**task_data, **updates, "updated_at": datetime.now(timezone.utc)}
    _tasks[task_id] = updated_task_data
    return _to_response(updated_task_data)


def delete_task(task_id: str) -> bool:
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False


def add_comment(task_id: str, payload: CommentCreate) -> Optional[CommentResponse]:
    if task_id not in _tasks:
        return None
    comment_data = {
        "id": str(uuid4()),
        "task_id": task_id,
        "text": payload.text,
        "created_at": datetime.now(timezone.utc),
    }
    _comments.setdefault(task_id, []).append(comment_data)
    return CommentResponse(**comment_data)


def get_comments_for_task(task_id: str) -> Optional[list[CommentResponse]]:
    if task_id not in _tasks:
        return None
    return [CommentResponse(**comment_data) for comment_data in _comments.get(task_id, [])]


def delete_comment(task_id: str, comment_id: str) -> bool | None:
    if task_id not in _tasks:
        return None
    task_comments = _comments.get(task_id)
    if task_comments is None:
        return False
    for index, comment_data in enumerate(task_comments):
        if comment_data["id"] == comment_id:
            del task_comments[index]
            if not task_comments:
                del _comments[task_id]
            return True
    return False


def _reset() -> None:
    _tasks.clear()
    _comments.clear()
