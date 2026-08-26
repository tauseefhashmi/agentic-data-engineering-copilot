import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parents[1]
mcp = FastMCP("dataops-mcp")

@mcp.tool()
def get_pipeline_status(pipeline_name: str) -> dict:
    data = json.loads((ROOT / "data/pipelines.json").read_text())
    p = data.get(pipeline_name)
    return {"pipeline": pipeline_name, "status": p.get("status") if p else "unknown", "last_success": p.get("last_success") if p else None}

@mcp.tool()
def get_pipeline_logs(pipeline_name: str) -> list[str]:
    data = json.loads((ROOT / "data/pipelines.json").read_text())
    return data.get(pipeline_name, {}).get("logs", [])

@mcp.tool()
def query_table_sample(table_name: str) -> dict:
    samples = {
        "staging.customer_orders": {"columns": ["order_id", "customer_id", "amount", "created_at"], "rows": 5},
        "dim_customer": {"columns": ["customer_id", "customer_segment", "country"], "rows": 5},
    }
    return samples.get(table_name, {"columns": [], "rows": 0})

@mcp.tool()
def search_runbook(topic: str) -> str:
    text = (ROOT / "data/runbooks.md").read_text()
    return text if topic.lower() in text.lower() else "No matching runbook section found."

@mcp.tool()
def create_remediation_ticket(title: str, description: str) -> dict:
    path = ROOT / "data" / "remediation_tickets.jsonl"
    record = {"title": title, "description": description}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return {"status": "created", "ticket": title}

if __name__ == "__main__":
    mcp.run()
