# inference.py
from fastapi import FastAPI
from pydantic import BaseModel
from main import app, act
app = FastAPI()

class State(BaseModel):
    clause: str = ""
    policy: str = ""
    risk_level: str = ""
    vendor_importance: str = ""

def act(state: dict):
    clause = state.get("clause", "").lower()
    policy = state.get("policy", "").lower()
    risk = state.get("risk_level", "")
    importance = state.get("vendor_importance", "")

    if clause == policy:
        return "accept"
    if risk == "high":
        if importance == "high":
            return "propose_edit"
        return "escalate"
    if risk == "low":
        return "propose_edit"
    return "accept"

@app.post("/act")
def act_endpoint(state: State):
    action = act(state.dict())
    return {"action": action}

@app.get("/health")
def health():
    return {"status": "ok"}