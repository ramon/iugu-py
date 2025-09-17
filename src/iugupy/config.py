from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Mapping


DEFAULT_BASE_URL = "https://api.iugu.com/v1"
DEFAULT_TIMEOUT = 30.0  # seconds
DEFAULT_USER_AGENT = "iugupy/0.1.0 (+https://github.com/ramongsoares/iugu-py)"


@dataclass(frozen=True)
class IuguConfig:
    """
    Configuration for the Iugu API client.

    Required:
      - api_token: The API token provided by IUGU.
      - client_id: An identifier for your application/integration (not sent as auth).
      - base_url: Base URL for the API (default: https://api.iugu.com/v1).

    Optional:
      - timeout: Default request timeout in seconds (float). Defaults to 30s.
      - user_agent: Value for the User-Agent header.
      - extra_headers: Additional headers to add to every request (merged with defaults).
    """

    api_token: str
    client_id: str
    base_url: str = DEFAULT_BASE_URL
    timeout: float = DEFAULT_TIMEOUT
    user_agent: str = DEFAULT_USER_AGENT
    extra_headers: Optional[Mapping[str, str]] = field(default=None)
