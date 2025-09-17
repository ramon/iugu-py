from __future__ import annotations

from typing import Any, Mapping

from .base import BaseResource


class Plans(BaseResource):
    def __init__(self, client) -> None:  # type: ignore[no-untyped-def]
        super().__init__(client, "plans")

    # CRUD
    def list(self, **params: Any) -> Any:
        return self._request("GET", params=params)

    def create(self, data: Mapping[str, Any]) -> Any:
        # Required by IUGU: name, interval, interval_type
        self._require_non_empty_payload(data)
        self._require_fields(data, ("name", "interval", "interval_type"))
        return self._request("POST", json=data)

    def get(self, plan_id: str) -> Any:
        self._require_id(plan_id, name="plan_id")
        return self._request("GET", plan_id)

    def update(self, plan_id: str, data: Mapping[str, Any]) -> Any:
        self._require_id(plan_id, name="plan_id")
        self._require_non_empty_payload(data)
        return self._request("PUT", plan_id, json=data)

    def delete(self, plan_id: str) -> Any:
        self._require_id(plan_id, name="plan_id")
        return self._request("DELETE", plan_id)
