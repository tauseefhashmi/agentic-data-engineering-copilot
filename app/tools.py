import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def _pipelines():
    return json.loads((ROOT / "data/pipelines.json").read_text())

def get_status(name):
    p = _pipelines().get(name, {})
    return {"pipeline": name, "status": p.get("status", "unknown"), "last_success": p.get("last_success")}

def get_logs(name):
    return _pipelines().get(name, {}).get("logs", [])

def query_sample(name):
    return {"columns": ["order_id", "customer_id", "amount", "created_at"], "rows": 5} if name == "staging.customer_orders" else {"columns": [], "rows": 0}

def search_runbook(topic):
    text = (ROOT / "data/runbooks.md").read_text()
    return text if topic.lower() in text.lower() else "No matching runbook section found."

def create_ticket(title, description):
    path = ROOT / "data/remediation_tickets.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"title": title, "description": description}) + "\n")
    return {"status": "created", "ticket": title}
