from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.tools import get_status, get_logs, search_runbook, query_sample, create_ticket

class State(TypedDict, total=False):
    incident: str
    evidence: dict
    rca: str
    remediation: str
    approved: bool
    report: str


def investigate(state: State):
    incident = state["incident"]
    pipeline = "customer_orders_daily" if "customer_orders_daily" in incident else "customer_orders_daily"
    evidence = {
        "status": get_status(pipeline),
        "logs": get_logs(pipeline),
        "table": query_sample("staging.customer_orders"),
        "runbook": search_runbook("schema mismatch"),
    }
    return {"evidence": evidence}


def synthesize(state: State):
    e = state["evidence"]
    missing = "customer_segment" in " ".join(e["logs"]) and "customer_segment" not in e["table"]["columns"]
    if missing:
        rca = "Likely root cause: downstream transformation expects customer_segment in staging.customer_orders, but the inspected schema does not contain that column."
        remediation = "Validate whether the upstream schema change was intentional. Update the data contract/model if intentional; otherwise stop publication and restore compatibility before rerunning."
    else:
        rca = "Insufficient evidence for a confident root cause."
        remediation = "Collect upstream schema and recent deployment information before taking action."
    return {"rca": rca, "remediation": remediation}


def gate(state: State):
    return {}


def act(state: State):
    if not state.get("approved"):
        return {"report": "Approval not granted; no side-effecting tool was called."}
    ticket = create_ticket("Schema mismatch - customer_orders_daily", state["remediation"])
    return {"report": f"RCA: {state['rca']}\nRemediation: {state['remediation']}\nAction: {ticket}"}


g = StateGraph(State)
g.add_node("investigate", investigate)
g.add_node("synthesize", synthesize)
g.add_node("gate", gate)
g.add_node("act", act)
g.set_entry_point("investigate")
g.add_edge("investigate", "synthesize")
g.add_edge("synthesize", "gate")
g.add_edge("gate", "act")
g.add_edge("act", END)
workflow = g.compile()
