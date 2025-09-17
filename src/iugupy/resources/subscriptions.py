from __future__ import annotations

from typing import Any, Mapping

from .base import BaseResource


class Subscriptions(BaseResource):
    def __init__(self, client) -> None:  # type: ignore[no-untyped-def]
        super().__init__(client, "subscriptions")

    def list(self, **params: Any) -> Any:
        return self._request("GET", params=params)

    def create(self, data: Mapping[str, Any]) -> Any:
        # Required by IUGU: plan_identifier and customer_id (simplified rule)
        self._require_non_empty_payload(data)
        self._require_fields(data, ("plan_identifier", "customer_id"))
        return self._request("POST", json=data)

    def get(self, subscription_id: str) -> Any:
        self._require_id(subscription_id, name="subscription_id")
        return self._request("GET", subscription_id)

    def update(self, subscription_id: str, data: Mapping[str, Any]) -> Any:
        self._require_id(subscription_id, name="subscription_id")
        self._require_non_empty_payload(data)
        return self._request("PUT", subscription_id, json=data)

    def delete(self, subscription_id: str) -> Any:
        self._require_id(subscription_id, name="subscription_id")
        return self._request("DELETE", subscription_id)

    # Actions
    def activate(self, subscription_id: str) -> Any:
        """Activate a suspended subscription."""
        self._require_id(subscription_id, name="subscription_id")
        return self._request("POST", f"{subscription_id}/activate")

    def suspend(self, subscription_id: str) -> Any:
        """Suspend an active subscription."""
        self._require_id(subscription_id, name="subscription_id")
        return self._request("POST", f"{subscription_id}/suspend")

    def change_plan(self, subscription_id: str, plan_identifier: str) -> Any:
        """Change the plan of a subscription."""
        self._require_id(subscription_id, name="subscription_id")
        self._require_id(plan_identifier, name="plan_identifier")
        return self._request("POST", f"{subscription_id}/change_plan/{plan_identifier}")

    def simulate_change_plan(self, subscription_id: str, plan_identifier: str) -> Any:
        """Simulate changing the plan of a subscription. Requires 'plan_identifier' in payload."""
        self._require_id(subscription_id, name="subscription_id")
        self._require_id(plan_identifier, name="plan_identifier")
        return self._request("POST", f"{subscription_id}/change_plan_simulation/{plan_identifier}")
