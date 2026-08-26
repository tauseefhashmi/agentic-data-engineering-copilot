# Agentic Data Engineering Copilot

A multi-agent **DataOps Incident Commander** inspired by the **AI Engineer Agentic Track: The Complete Agent & MCP Course**.

The system receives a failed pipeline incident and coordinates specialized agents to investigate it, retrieve runbook knowledge, identify likely root causes, propose a safe remediation and produce an incident report.

## What it demonstrates

- Agent loop: LLM + tools + iterative decisions
- Multi-agent orchestration with LangGraph
- MCP server exposing operational tools
- Structured tool inputs/outputs
- Memory/checkpoint-ready graph design
- Human approval gate before remediation
- Separation of investigation from action
- Dockerized service layout

## Architecture

```text
Incident -> Supervisor
              |
        +-----+------+----------------+
        |            |                |
        v            v                v
   SQL Agent    Runbook Agent   Pipeline Agent
        |            |                |
        +------------+----------------+
                     v
              RCA / Remediation Agent
                     |
               Human approval
                     |
                Action tool
                     |
                Incident report

MCP Server exposes tools:
- get_pipeline_status
- get_pipeline_logs
- query_table_sample
- search_runbook
- create_remediation_ticket
```

## Quick start

```powershell
uv venv
uv pip install -r requirements.txt
uv run python -m mcp_server.server
```

For the full API/UI layer:

```powershell
docker compose up --build
```

## Example incident

> `customer_orders_daily` failed at 03:17 UTC after a schema change. Investigate and propose a remediation, but do not execute changes without approval.

Expected behavior:

1. Supervisor decomposes the incident.
2. Pipeline agent checks run status/logs.
3. SQL agent inspects table metadata/sample rows.
4. Runbook agent retrieves matching operational guidance.
5. RCA agent synthesizes evidence and confidence.
6. Human approval is required.
7. Only then can the remediation-ticket tool be called.

## Portfolio talking points

- Why use MCP instead of hard-wiring every API into the agent?
- Which tools are read-only versus side-effecting?
- Why is the action tool behind human approval?
- What should be logged for agent observability?
- How would you replace the mock tools with Airflow, Snowflake and Jira APIs?
