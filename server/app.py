from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
try:
    from ..env import ContractEnv
    from ..models import StepRequest, StepResponse
except ImportError:
    from env import ContractEnv
    from models import StepRequest, StepResponse
import uvicorn

app = FastAPI()
env = ContractEnv(task="easy")

class GraderRequest(BaseModel):
    task: str
    state: dict
    action: str

def _score(action, state):
    clause = state.get("clause", "").lower()
    policy = state.get("policy", "").lower()
    risk = state.get("risk_level", "")
    importance = state.get("vendor_importance", "")
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
    return 0.01

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
def grader(request: GraderRequest):
    score = _score(request.action, request.state)
    return {"score": score, "task": request.task}

@app.get("/tasks")
def tasks():
    return {"tasks": ["easy", "medium", "hard"]}

@app.get("/health")
def health():
    return {"status": "ok"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
