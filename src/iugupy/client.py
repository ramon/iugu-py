from __future__ import annotations

from typing import Any, Dict, Mapping, Optional
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

from .config import IuguConfig
from .resources import Plans, Customers, Subscriptions, Invoices


JSON_MIME = "application/json"


class IuguClient:
    """
    Thin HTTP client for the IUGU API using requests.

    Ensures that all requests carry:
      - Basic Auth built from api_token (username) and blank password
      - Accept: application/json
      - Content-Type: application/json (for requests that send a body)
    """

    def __init__(self, config: IuguConfig) -> None:
        self._config = config
        self._session = requests.Session()
        # Basic auth: token as username, blank password
        self._session.auth = HTTPBasicAuth(config.api_token, "")

        # Default headers
        default_headers: Dict[str, str] = {
            "Accept": JSON_MIME,
            "Content-Type": JSON_MIME,
            "User-Agent": config.user_agent,
        }
        if config.extra_headers:
            default_headers.update(config.extra_headers)
        self._session.headers.update(default_headers)

        # Store base url and timeout
        self._base_url = config.base_url.rstrip("/") + "/"
        self._timeout = config.timeout

        # Resources
        self.plans = Plans(self)
        self.customers = Customers(self)
        self.subscriptions = Subscriptions(self)
        self.invoices = Invoices(self)

    @property
    def config(self) -> IuguConfig:
        return self._config

    @property
    def session(self) -> requests.Session:  # exposed for advanced scenarios/testing
        return self._session

    @property
    def base_url(self) -> str:
        return self._base_url

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> requests.Response:
        """
        Perform an HTTP request relative to the configured base_url.
        Ensures JSON headers are present; custom headers can override defaults.
        """
        url = urljoin(self._base_url, path.lstrip("/"))
        # Merge headers if provided; session headers serve as defaults.
        req_headers = dict(self._session.headers)
        if headers:
            req_headers.update(headers)

        resp = self._session.request(
            method=method.upper(),
            url=url,
            params=params,
            json=json,
            headers=req_headers,
            timeout=self._timeout if timeout is None else timeout,
        )
        return resp

    # Convenience HTTP verb helpers
    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)
