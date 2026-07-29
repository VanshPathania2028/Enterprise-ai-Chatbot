from typing import Any, List
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The user's chat message"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(
        ...,
        description="The AI assistant's response"
    )


class ValidationErrorDetail(BaseModel):
    """Detail of a validation error."""
    loc: List[str | int] = Field(
        ...,
        description="Location of the validation error"
    )
    msg: str = Field(
        ...,
        description="Error message"
    )
    type: str = Field(
        ...,
        description="Error type"
    )
    input: Any = Field(
        default=None,
        description="Input that caused the error"
    )
    ctx: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context about the error"
    )


class HTTPValidationError(BaseModel):
    """Standard HTTP validation error response."""
    detail: List[ValidationErrorDetail] = Field(
        ...,
        description="List of validation error details"
    )

