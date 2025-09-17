from __future__ import annotations

from typing import Any, Mapping

from .base import BaseResource


class Customers(BaseResource):
    def __init__(self, client) -> None:  # type: ignore[no-untyped-def]
        super().__init__(client, "customers")

    def list(self, **params: Any) -> Any:
        return self._request("GET", params=params)

    def create(self, data: Mapping[str, Any]) -> Any:
        self._require_non_empty_payload(data)
        self._require_fields(data, ("email",))
        return self._request("POST", json=data)

    def get(self, customer_id: str) -> Any:
        self._require_id(customer_id, name="customer_id")
        return self._request("GET", customer_id)

    def update(self, customer_id: str, data: Mapping[str, Any]) -> Any:
        self._require_id(customer_id, name="customer_id")
        self._require_non_empty_payload(data)
        return self._request("PUT", customer_id, json=data)

    def delete(self, customer_id: str) -> Any:
        self._require_id(customer_id, name="customer_id")
        return self._request("DELETE", customer_id)

    # ---- Payment Methods ----
    def list_payment_methods(self, customer_id: str, **params: Any) -> Any:
        self._require_id(customer_id, name="customer_id")
        return self._request("GET", f"{customer_id}/payment_methods", params=params)

    def create_payment_method(self, customer_id: str, data: Mapping[str, Any]) -> Any:
        self._require_id(customer_id, name="customer_id")
        self._require_non_empty_payload(data)
        self._require_fields(data, ("token", "description"))
        return self._request("POST", f"{customer_id}/payment_methods", json=data)

    def get_payment_method(self, customer_id: str, payment_method_id: str) -> Any:
        self._require_id(customer_id, name="customer_id")
        self._require_id(payment_method_id, name="payment_method_id")
        return self._request("GET", f"{customer_id}/payment_methods/{payment_method_id}")

    def delete_payment_method(self, customer_id: str, payment_method_id: str) -> Any:
        self._require_id(customer_id, name="customer_id")
        self._require_id(payment_method_id, name="payment_method_id")
        return self._request("DELETE", f"{customer_id}/payment_methods/{payment_method_id}")

    def update_payment_method(
        self, customer_id: str, payment_method_id: str, data: Mapping[str, Any]
    ) -> Any:
        """Update customer's payment method."""
        self._require_id(customer_id, name="customer_id")
        self._require_id(payment_method_id, name="payment_method_id")
        self._require_non_empty_payload(data)
        self._require_any_of(data, ("description", "set_as_default"))
        return self._request("PUT", f"{customer_id}/payment_methods/{payment_method_id}", json=data)
