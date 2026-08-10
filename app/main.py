from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import storage
from app.api.routes.health import router as health_router
from app.business_rules import validate_status_transition
from app.core.config import get_settings
from app.models import CommentCreate, CommentResponse, TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

settings = get_settings()

app = FastAPI(
    title="Task Tracker API",
    description="A simple REST API for managing tasks, built with FastAPI.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.include_router(health_router)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload: Task creation data (title, description, status, priority,
            assignee, due_date).

    Returns:
        The newly created task, including its generated id, computed
        `overdue` flag, and `created_at`/`updated_at` timestamps.

    Example:
        POST /tasks {"title": "Write docs", "priority": "High"}
    """
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by status, priority, and overdue state.

    Args:
        status: If provided, only tasks with this status are returned.
        priority: If provided, only tasks with this priority are returned.
        overdue: If provided, only tasks whose computed `overdue` flag
            matches this value are returned.

    Returns:
        Tasks matching all provided filters (filters combine with AND).

    Example:
        GET /tasks?status=ToDo&priority=High&overdue=true
    """
    tasks = storage.get_all_tasks(status=status, priority=priority)
    if overdue is not None:
        tasks = [task for task in tasks if task.overdue is overdue]
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by id.

    Args:
        task_id: The unique identifier of the task.

    Returns:
        The matching task.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.

    Example:
        GET /tasks/{task_id}
    """
    task = storage.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Partially update a task.

    Only fields present in `payload` are changed. If `payload.status` is
    set, the transition from the task's current status is validated via
    `validate_status_transition` before the update is applied.

    Args:
        task_id: The unique identifier of the task to update.
        payload: The fields to update; unset fields are left unchanged.

    Returns:
        The updated task.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.
        HTTPException: 422 if `payload.status` is not a valid transition
            from the task's current status.

    Example:
        PATCH /tasks/{task_id} {"status": "InProgress"}
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task with id {task_id} not found",
            )
        validate_status_transition(existing.status, payload.status)

    task = storage.update_task(task_id, payload)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Delete a task by id.

    Args:
        task_id: The unique identifier of the task to delete.

    Returns:
        None. Responds with 204 No Content on success.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.

    Example:
        DELETE /tasks/{task_id}
    """
    deleted = storage.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )


@app.get("/tasks/{task_id}/comments", response_model=list[CommentResponse], tags=["tasks"])
def list_comments(task_id: str) -> list[CommentResponse]:
    """List all comments for a task.

    Args:
        task_id: The unique identifier of the parent task.

    Returns:
        The list of comments for the task (empty list if none exist).

    Raises:
        HTTPException: 404 if no task with `task_id` exists.

    Example:
        GET /tasks/{task_id}/comments
    """
    comments = storage.get_comments_for_task(task_id)

    if comments is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return comments


@app.post("/tasks/{task_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def add_comment(task_id: str, payload: CommentCreate) -> CommentResponse:
    """Add a comment to a task.

    Args:
        task_id: The unique identifier of the parent task.
        payload: The comment data (`text`).

    Returns:
        The newly created comment.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.

    Example:
        POST /tasks/{task_id}/comments {"text": "Looks good"}
    """
    comment = storage.add_comment(task_id, payload)

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return comment


@app.delete("/tasks/{task_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_comment(task_id: str, comment_id: str) -> None:
    """Delete a comment from a task.

    Args:
        task_id: The unique identifier of the parent task.
        comment_id: The unique identifier of the comment to delete.

    Returns:
        None. Responds with 204 No Content on success.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.
        HTTPException: 404 if no comment with `comment_id` exists for the task.

    Example:
        DELETE /tasks/{task_id}/comments/{comment_id}
    """
    deleted = storage.delete_comment(task_id, comment_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Comment with id {comment_id} not found for task {task_id}",
        )


@app.get("/")
def read_root() -> dict:
    """Root endpoint.

    Returns:
        A short status message pointing to the API docs.

    Example:
        GET /
    """
    return {"message": "Task Tracker API is running. Visit /docs for API documentation."}