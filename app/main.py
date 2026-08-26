from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import workflow

app = FastAPI(title="Agentic Data Engineering Copilot")

class Incident(BaseModel):
    incident: str
    approved: bool = False

@app.get("/health")
def health(): return {"status": "ok"}

@app.post("/investigate")
def investigate(req: Incident):
    result = workflow.invoke({"incident": req.incident, "approved": req.approved})
    return result
