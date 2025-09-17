from __future__ import annotations

from typing import Any, Mapping

from .base import BaseResource


class Invoices(BaseResource):
    def __init__(self, client) -> None:  # type: ignore[no-untyped-def]
        super().__init__(client, "invoices")

    def list(self, **params: Any) -> Any:
        return self._request("GET", params=params)

    def create(self, data: Mapping[str, Any]) -> Any:
        # Required by IUGU: due_date, items (non-empty list), and one of email or customer_id
        self._require_non_empty_payload(data)
        self._require_fields(data, ("due_date",))
        self._require_list_non_empty(data, "items")
        self._require_any_of(data, ("email", "customer_id"))
        return self._request("POST", json=data)

    def get(self, invoice_id: str) -> Any:
        self._require_id(invoice_id, name="invoice_id")
        return self._request("GET", invoice_id)

    def update(self, invoice_id: str, data: Mapping[str, Any]) -> Any:
        self._require_id(invoice_id, name="invoice_id")
        self._require_non_empty_payload(data)
        return self._request("PUT", invoice_id, json=data)

    def delete(self, invoice_id: str) -> Any:
        self._require_id(invoice_id, name="invoice_id")
        return self._request("DELETE", invoice_id)
