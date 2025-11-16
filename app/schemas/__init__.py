"""Pydantic schemas for request/response validation."""

from app.schemas.prime import (
    PrimeCheckRequest,
    PrimeCheckResponse,
    PrimeCheckHistoryResponse
)

__all__ = [
    "PrimeCheckRequest",
    "PrimeCheckResponse",
    "PrimeCheckHistoryResponse"
]

