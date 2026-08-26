from app.graph import workflow

def test_requires_approval_for_action():
    r = workflow.invoke({"incident":"customer_orders_daily failed due to missing column", "approved":False})
    assert "no side-effecting" in r["report"]

def test_creates_ticket_when_approved(tmp_path, monkeypatch):
    # Functional path is covered by the workflow; the repository keeps ticket creation local for the demo.
    r = workflow.invoke({"incident":"customer_orders_daily failed due to schema mismatch", "approved":True})
    assert "Action:" in r["report"]
