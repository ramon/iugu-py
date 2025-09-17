from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class IuguAPIError(Exception):
    """Represents an error response from the IUGU API.

    Attributes:
        status_code: HTTP status code.
        message: A human-readable message, if available.
        payload: Parsed JSON payload from the response (if any), useful for debugging.
        url: The requested URL that caused the error.
        method: The HTTP method used.
    """

    status_code: int
    message: str
    payload: Optional[Dict[str, Any]] = None
    url: Optional[str] = None
    method: Optional[str] = None

    def __str__(self) -> str:  # pragma: no cover - simple formatting
        base = f"IUGU API Error {self.status_code}: {self.message}"
        if self.method and self.url:
            base += f" ({self.method} {self.url})"
        return base


@dataclass
class IuguValidationError(Exception):
    """Raised when required fields are missing or invalid before making a request."""

    message: str

    def __str__(self) -> str:  # pragma: no cover - simple formatting
        return f"IUGU Validation Error: {self.message}"
