from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Task Tracker API",
    description="A simple REST API for managing tasks, built with FastAPI.",
    version="0.1.0",
)

app.include_router(health_router)


@app.get("/")
def read_root() -> dict:
    return {"message": "Task Tracker API is running. Visit /docs for API documentation."}