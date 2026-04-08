
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class State(BaseModel):
    clause: str = ""
    policy: str = ""
    risk_level: str = ""
    vendor_importance: str = ""

@app.post("/act")
def act(state: State):
    clause = state.clause.lower()
    policy = state.policy.lower()
    risk = state.risk_level
    importance = state.vendor_importance

    if clause == policy:
        return {"action": "accept"}
    if risk == "high":
        if importance == "high":
            return {"action": "propose_edit"}
        return {"action": "escalate"}
    if risk == "low":
        return {"action": "propose_edit"}
    return {"action": "accept"}

@app.get("/health")
def health():
    return {"status": "ok"}
