"""Pydantic request/response models for API."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class URLRequest(BaseModel):
    url: str = Field(..., min_length=3, max_length=2048)


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    context: Optional[dict[str, Any]] = None


class PredictionResponse(BaseModel):
    success: bool = True
    data: dict[str, Any]
    explainability: Optional[dict[str, Any]] = None
