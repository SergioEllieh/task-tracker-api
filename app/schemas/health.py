from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status of the API", examples=["ok"])
    timestamp: str = Field(
        ...,
        description="Current UTC timestamp in ISO 8601 format",
        examples=["2026-07-01T12:00:00+00:00"],
    )
