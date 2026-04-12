from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, Any
from env import ContractEnv
from models import StepRequest, StepResponse

app = FastAPI()
env = ContractEnv(task="easy")

def _score(action, state):
    if isinstance(state, dict):
        clause = state.get("clause", "").lower()
        policy = state.get("policy", "").lower()
        risk = state.get("risk_level", "")
        importance = state.get("vendor_importance", "")
    else:
        clause = getattr(state, "clause", "").lower()
        policy = getattr(state, "policy", "").lower()
        risk = getattr(state, "risk_level", "")
        importance = getattr(state, "vendor_importance", "")
    if clause == policy:
        return 0.99 if action == "accept" else 0.01
    if risk == "high":
        if importance == "high":
            if action == "propose_edit": return 0.99
            elif action == "escalate": return 0.6
            else: return 0.01
        else:
            if action == "escalate": return 0.6
            elif action == "propose_edit": return 0.8
            else: return 0.01
    if risk == "low":
        if action == "propose_edit": return 0.99
        elif action == "accept": return 0.8
        else: return 0.01
    return 0.5

@app.get("/")
def home():
    return {"message": "Contract Negotiation Environment API"}

@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": state}

@app.get("/state")
def get_state():
    return {"state": env.state()}

@app.post("/step", response_model=StepResponse)
def step(request: StepRequest):
    if request.action not in ["accept", "propose_edit", "escalate"]:
        return {"state": None, "reward": -1.0, "done": True}
    next_state, reward, done, _ = env.step(request.action)
    return StepResponse(state=next_state, reward=reward, done=done)

@app.post("/grader")
async def grader(request: Request):
    try:
        body = await request.json()
    except:
        body = {}
    task = body.get("task", "easy")
    state = body.get("state", body.get("observation", {}))
    action = body.get("action", "accept")
    score = _score(action, state)
    return {"score": score, "task": task, "reward": score}

@app.get("/tasks")
def tasks():
    return {"tasks": ["easy", "medium", "hard"]}

@app.get("/health")
def health():
    return {"status": "ok"}
