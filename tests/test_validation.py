import pytest

import iugupy


class Recorder:
    def __init__(self):
        self.calls = 0

    def __call__(self, *args, **kwargs):  # fake client.request
        self.calls += 1
        raise AssertionError("HTTP request should not be called when validation fails")


def make_client() -> iugupy.IuguClient:
    cfg = iugupy.IuguConfig(api_token="tok", client_id="cid", base_url="https://api.example.com/v1")
    return iugupy.IuguClient(cfg)


def test_plans_create_requires_fields(monkeypatch):
    c = make_client()
    rec = Recorder()
    monkeypatch.setattr(c, "request", rec)

    with pytest.raises(iugupy.IuguValidationError):
        c.plans.create({})
    assert rec.calls == 0

    with pytest.raises(iugupy.IuguValidationError):
        c.plans.create({"name": "Gold", "interval": 1})  # missing interval_type
    assert rec.calls == 0


def test_plans_id_required(monkeypatch):
    c = make_client()
    rec = Recorder()
    monkeypatch.setattr(c, "request", rec)

    with pytest.raises(iugupy.IuguValidationError):
        c.plans.get("")
    with pytest.raises(iugupy.IuguValidationError):
        c.plans.update(" ", {"name": "n"})
    with pytest.raises(iugupy.IuguValidationError):
        c.plans.delete("")
    assert rec.calls == 0


def test_customers_create_requires_email(monkeypatch):
    c = make_client()
    rec = Recorder()
    monkeypatch.setattr(c, "request", rec)

    with pytest.raises(iugupy.IuguValidationError):
        c.customers.create({})
    assert rec.calls == 0


def test_customers_update_requires_payload_and_id(monkeypatch):
    c = make_client()
    rec = Recorder()
    monkeypatch.setattr(c, "request", rec)

    with pytest.raises(iugupy.IuguValidationError):
        c.customers.update(" ", {"name": "a"})
    with pytest.raises(iugupy.IuguValidationError):
        c.customers.update("cus_1", {})
    assert rec.calls == 0


def test_subscriptions_create_requires_fields(monkeypatch):
    c = make_client()
    rec = Recorder()
    monkeypatch.setattr(c, "request", rec)

    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.create({})
    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.create({"plan_identifier": "gold"})  # missing customer_id
    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.create({"customer_id": "cus_1"})  # missing plan_identifier
    assert rec.calls == 0


def test_invoices_create_requires_due_date_items_and_recipient(monkeypatch):
    c = make_client()
    rec = Recorder()
    monkeypatch.setattr(c, "request", rec)

    with pytest.raises(iugupy.IuguValidationError):
        c.invoices.create({})
    with pytest.raises(iugupy.IuguValidationError):
        c.invoices.create({"due_date": "2025-12-31"})  # missing items and recipient
    with pytest.raises(iugupy.IuguValidationError):
        c.invoices.create({"due_date": "2025-12-31", "items": []})  # items empty
    with pytest.raises(iugupy.IuguValidationError):
        c.invoices.create({"due_date": "2025-12-31", "items": [{}]})  # no recipient
    with pytest.raises(iugupy.IuguValidationError):
        c.invoices.create({"due_date": "2025-12-31", "email": "a@b.com", "items": []})
    assert rec.calls == 0


def test_updates_require_payload(monkeypatch):
    c = make_client()
    rec = Recorder()
    monkeypatch.setattr(c, "request", rec)

    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.update("sub_1", {})
    with pytest.raises(iugupy.IuguValidationError):
        c.invoices.update("inv_1", {})
    with pytest.raises(iugupy.IuguValidationError):
        c.plans.update("plan_1", {})
    with pytest.raises(iugupy.IuguValidationError):
        c.customers.update("cus_1", {})
    assert rec.calls == 0


def test_subscription_actions_validation(monkeypatch):
    c = make_client()
    rec = Recorder()
    monkeypatch.setattr(c, "request", rec)

    # ID validation for actions
    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.activate("")
    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.suspend("  ")
    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.change_plan("", {"plan_identifier": "pro"})
    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.simulate_change_plan("", {"plan_identifier": "pro"})

    # Required payload for change_plan/simulate_change_plan
    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.change_plan("sub_1", {})
    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.simulate_change_plan("sub_1", {})

    # plan_identifier must be non-empty string
    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.change_plan("sub_1", {"plan_identifier": " "})
    with pytest.raises(iugupy.IuguValidationError):
        c.subscriptions.simulate_change_plan("sub_1", {"plan_identifier": ""})

    assert rec.calls == 0


def test_customer_payment_methods_validation(monkeypatch):
    c = make_client()
    rec = Recorder()
    monkeypatch.setattr(c, "request", rec)

    # list requires customer_id
    with pytest.raises(iugupy.IuguValidationError):
        c.customers.list_payment_methods("")

    # create requires customer_id and non-empty payload with either token or data
    with pytest.raises(iugupy.IuguValidationError):
        c.customers.create_payment_method("", {"token": "tok"})
    with pytest.raises(iugupy.IuguValidationError):
        c.customers.create_payment_method("cus_1", {})
    with pytest.raises(iugupy.IuguValidationError):
        c.customers.create_payment_method("cus_1", {"data": {}})  # empty card data

    # get/delete/set_default require both IDs
    with pytest.raises(iugupy.IuguValidationError):
        c.customers.get_payment_method("", "pm_1")
    with pytest.raises(iugupy.IuguValidationError):
        c.customers.get_payment_method("cus_1", "")

    with pytest.raises(iugupy.IuguValidationError):
        c.customers.delete_payment_method("", "pm_1")
    with pytest.raises(iugupy.IuguValidationError):
        c.customers.delete_payment_method("cus_1", " ")

    with pytest.raises(iugupy.IuguValidationError):
        c.customers.update_payment_method("", "pm_1", {})
    with pytest.raises(iugupy.IuguValidationError):
        c.customers.update_payment_method("cus_1", "", {})

    assert rec.calls == 0
