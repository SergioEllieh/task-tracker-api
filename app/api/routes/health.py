from datetime import datetime, timezone

from fastapi import APIRouter

from app.models.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse, status_code=200)
def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns a simple status payload confirming the API is running,
    along with the current UTC timestamp in ISO 8601 format.
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )