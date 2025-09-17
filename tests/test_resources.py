import pytest

import iugupy


class FakeResp:
    def __init__(
        self, status_code: int, payload=None, url: str | None = None, method: str | None = None
    ):
        self.status_code = status_code
        self._payload = payload
        self.url = url
        self.request = type("R", (), {"method": method}) if method else None
        self.text = None if payload is None else str(payload)

    def json(self):
        if self._payload is None:
            raise ValueError("no payload")
        return self._payload


def make_client() -> iugupy.IuguClient:
    cfg = iugupy.IuguConfig(api_token="tok", client_id="cid", base_url="https://api.example.com/v1")
    return iugupy.IuguClient(cfg)


def test_plans_basic_crud_paths_and_payload(monkeypatch):
    c = make_client()
    calls: list[tuple] = []

    def fake_request(method, path, **kwargs):
        calls.append((method, path, kwargs))
        return FakeResp(200, {"ok": True})

    monkeypatch.setattr(c, "request", fake_request)

    # list
    res = c.plans.list(page=2)
    assert res == {"ok": True}
    assert calls[-1][0] == "GET" and calls[-1][1] == "plans"
    assert calls[-1][2]["params"] == {"page": 2}

    # create
    res = c.plans.create({"name": "Gold", "interval": 1, "interval_type": "months"})
    assert res == {"ok": True}
    assert calls[-1][0] == "POST" and calls[-1][1] == "plans"
    assert calls[-1][2]["json"] == {"name": "Gold", "interval": 1, "interval_type": "months"}

    # get
    c.plans.get("plan_123")
    assert calls[-1][0] == "GET" and calls[-1][1] == "plans/plan_123"

    # update
    c.plans.update("plan_123", {"name": "Platinum"})
    assert calls[-1][0] == "PUT" and calls[-1][1] == "plans/plan_123"
    assert calls[-1][2]["json"] == {"name": "Platinum"}

    # delete
    c.plans.delete("plan_123")
    assert calls[-1][0] == "DELETE" and calls[-1][1] == "plans/plan_123"


def test_customers_and_subscriptions_and_invoices_paths(monkeypatch):
    c = make_client()
    calls: list[tuple] = []

    def fake_request(method, path, **kwargs):
        calls.append((method, path, kwargs))
        return FakeResp(200, {"ok": True})

    monkeypatch.setattr(c, "request", fake_request)

    # Customers
    c.customers.create({"email": "a@b.com"})
    assert calls[-1][0] == "POST" and calls[-1][1] == "customers"
    c.customers.get("cus_1")
    assert calls[-1][0] == "GET" and calls[-1][1] == "customers/cus_1"
    c.customers.update("cus_1", {"name": "Alice"})
    assert calls[-1][0] == "PUT" and calls[-1][1] == "customers/cus_1"
    c.customers.delete("cus_1")
    assert calls[-1][0] == "DELETE" and calls[-1][1] == "customers/cus_1"

    # Subscriptions
    c.subscriptions.list(limit=10)
    assert calls[-1][0] == "GET" and calls[-1][1] == "subscriptions"
    assert calls[-1][2]["params"] == {"limit": 10}
    c.subscriptions.get("sub_1")
    assert calls[-1][0] == "GET" and calls[-1][1] == "subscriptions/sub_1"

    # Subscriptions actions
    c.subscriptions.activate("sub_1")
    assert calls[-1][0] == "POST" and calls[-1][1] == "subscriptions/sub_1/activate"

    c.subscriptions.suspend("sub_1")
    assert calls[-1][0] == "POST" and calls[-1][1] == "subscriptions/sub_1/suspend"

    c.subscriptions.change_plan("sub_1", "pro")
    assert calls[-1][0] == "POST" and calls[-1][1] == "subscriptions/sub_1/change_plan/pro"

    c.subscriptions.simulate_change_plan("sub_1", "pro")
    assert (
        calls[-1][0] == "POST" and calls[-1][1] == "subscriptions/sub_1/change_plan_simulation/pro"
    )

    # Invoices
    c.invoices.create(
        {
            "email": "a@b.com",
            "due_date": "2025-12-31",
            "items": [{"description": "Service", "quantity": 1, "price_cents": 1000}],
        }
    )
    assert calls[-1][0] == "POST" and calls[-1][1] == "invoices"
    assert calls[-1][2]["json"]["email"] == "a@b.com"
    c.invoices.get("inv_1")
    assert calls[-1][0] == "GET" and calls[-1][1] == "invoices/inv_1"


def test_error_raises_iugu_api_error(monkeypatch):
    c = make_client()

    def fake_request(method, path, **kwargs):
        return FakeResp(
            400,
            {"errors": {"field": "invalid"}},
            url=f"https://api.example.com/{path}",
            method=method,
        )

    monkeypatch.setattr(c, "request", fake_request)

    with pytest.raises(iugupy.IuguAPIError) as exc:
        c.customers.create({"email": "bad"})
    assert exc.value.status_code == 400
    assert "invalid" in exc.value.message
    assert exc.value.url.endswith("/customers")


def test_customer_payment_methods_paths(monkeypatch):
    c = make_client()
    calls: list[tuple] = []

    def fake_request(method, path, **kwargs):
        calls.append((method, path, kwargs))
        return FakeResp(200, {"ok": True})

    monkeypatch.setattr(c, "request", fake_request)

    # list payment methods
    c.customers.list_payment_methods("cus_1", page=3)
    assert calls[-1][0] == "GET" and calls[-1][1] == "customers/cus_1/payment_methods"
    assert calls[-1][2]["params"] == {"page": 3}

    # create payment method with token
    c.customers.create_payment_method("cus_1", {"token": "tok_123", "description": "desc"})
    assert calls[-1][0] == "POST" and calls[-1][1] == "customers/cus_1/payment_methods"
    assert calls[-1][2]["json"] == {"token": "tok_123", "description": "desc"}

    # get payment method
    c.customers.get_payment_method("cus_1", "pm_1")
    assert calls[-1][0] == "GET" and calls[-1][1] == "customers/cus_1/payment_methods/pm_1"

    # delete payment method
    c.customers.delete_payment_method("cus_1", "pm_1")
    assert calls[-1][0] == "DELETE" and calls[-1][1] == "customers/cus_1/payment_methods/pm_1"

    # set default payment method
    c.customers.update_payment_method("cus_1", "pm_1", {"description": "desc"})
    assert calls[-1][0] == "PUT" and calls[-1][1] == "customers/cus_1/payment_methods/pm_1"
    assert calls[-1][2]["json"] == {"description": "desc"}
