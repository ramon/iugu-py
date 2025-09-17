from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional

from typing import TYPE_CHECKING

from ..errors import IuguAPIError, IuguValidationError

if TYPE_CHECKING:
    from ..client import IuguClient


class BaseResource:
    def __init__(self, client: IuguClient, resource_path: str) -> None:
        self._client = client
        self._resource_path = resource_path.strip("/")

    @property
    def client(self) -> IuguClient:
        return self._client

    # ---- Validation helpers ----
    @staticmethod
    def _require_non_empty_payload(data: Optional[Mapping[str, Any]], *, where: str = "payload") -> Mapping[str, Any]:
        if not data or not isinstance(data, Mapping) or len(data) == 0:
            raise IuguValidationError(f"{where} must be a non-empty mapping")
        return data

    @staticmethod
    def _require_fields(data: Mapping[str, Any], fields: Iterable[str], *, where: str = "payload") -> None:
        missing: list[str] = []
        for f in fields:
            if f not in data or data[f] is None or (isinstance(data[f], str) and data[f].strip() == ""):
                missing.append(f)
        if missing:
            raise IuguValidationError(f"missing required field(s) in {where}: {', '.join(missing)}")

    @staticmethod
    def _require_any_of(data: Mapping[str, Any], fields: Iterable[str], *, where: str = "payload") -> None:
        if not any((f in data and data[f] not in (None, "")) for f in fields):
            raise IuguValidationError(f"at least one of ({', '.join(fields)}) is required in {where}")

    @staticmethod
    def _require_list_non_empty(data: Mapping[str, Any], key: str, *, where: str = "payload") -> None:
        value = data.get(key)
        if not isinstance(value, list) or len(value) == 0:
            raise IuguValidationError(f"'{key}' must be a non-empty list in {where}")

    @staticmethod
    def _require_id(identifier: str, *, name: str = "id") -> str:
        if not isinstance(identifier, str) or identifier.strip() == "":
            raise IuguValidationError(f"{name} must be a non-empty string")
        return identifier

    # ---- Request wrapper ----
    def _request(
        self,
        method: str,
        path: str = "",
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Any] = None,
    ) -> Any:
        rel = "/".join([p for p in (self._resource_path, path.strip("/")) if p])
        resp = self._client.request(method, rel, params=params, json=json)
        return self._handle_response(resp, method)

    @staticmethod
    def _handle_response(resp: Any, method: str) -> Any:
        # Success
        if 200 <= resp.status_code < 300:
            # Some endpoints may return 204 No Content
            try:
                return resp.json()
            except Exception:
                return None
        # Error path: build message from payload if possible
        payload = None
        message = "HTTP error"
        try:
            payload = resp.json()
            # IUGU commonly returns {'errors': {...}} or {'message': '...'}
            if isinstance(payload, dict):
                if "message" in payload and isinstance(payload["message"], str):
                    message = payload["message"]
                elif "errors" in payload:
                    message = str(payload["errors"])  # keep simple representation
        except Exception:
            # Fallback to text content
            try:
                message = getattr(resp, "text", message)
            except Exception:
                pass
        # Gather URL/method context if available
        url = getattr(resp, "url", None)
        req = getattr(resp, "request", None)
        req_method = getattr(req, "method", method)
        raise IuguAPIError(resp.status_code, message, payload=payload, url=url, method=req_method)
