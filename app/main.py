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
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    tasks = storage.get_all_tasks(status=status, priority=priority)
    if overdue is not None:
        tasks = [task for task in tasks if task.overdue is overdue]
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
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
    deleted = storage.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )


@app.get("/tasks/{task_id}/comments", response_model=list[CommentResponse], tags=["tasks"])
def list_comments(task_id: str) -> list[CommentResponse]:
    comments = storage.get_comments_for_task(task_id)

    if comments is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return comments


@app.post("/tasks/{task_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def add_comment(task_id: str, payload: CommentCreate) -> CommentResponse:
    comment = storage.add_comment(task_id, payload)

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return comment


@app.delete("/tasks/{task_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_comment(task_id: str, comment_id: str) -> None:
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
    return {"message": "Task Tracker API is running. Visit /docs for API documentation."}