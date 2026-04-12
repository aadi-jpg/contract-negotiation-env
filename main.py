from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, Any
from env import ContractEnv
from models import StepRequest, StepResponse

app = FastAPI(version="0.1.0")

envs = {
    "easy": ContractEnv(task="easy"),
    "medium": ContractEnv(task="medium"),
    "hard": ContractEnv(task="hard"),
}
session = {"task": "easy"}

def get_env():
    return envs[session["task"]]

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

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metadata")
def metadata():
    return {
        "name": "contract-negotiation-env",
        "description": "An environment that simulates contract clause evaluation. Agents must decide whether to accept, propose edits, or escalate based on company policy and risk.",
        "version": "0.1.0"
    }

@app.get("/schema")
def schema():
    return {
        "action": {"type": "string", "enum": ["accept", "propose_edit", "escalate"]},
        "observation": {"clause": "string", "policy": "string", "risk_level": "string", "vendor_importance": "string"},
        "state": {"clause": "string", "policy": "string", "risk_level": "string", "vendor_importance": "string"}
    }

@app.post("/mcp")
async def mcp(request: Request):
    try:
        body = await request.json()
    except:
        body = {}
    return {"jsonrpc": "2.0", "id": body.get("id", 1), "result": {}}

@app.post("/reset")
async def reset(request: Request):
    try:
        body = await request.json()
    except:
        body = {}
    task = body.get("task") or body.get("task_id") or "easy"
    if task not in envs:
        task = "easy"
    session["task"] = task
    state = envs[task].reset()
    return {"state": state, "task": task}

@app.get("/state")
def get_state():
    return {"state": get_env().state()}

@app.post("/step", response_model=StepResponse)
async def step(request: Request):
    try:
        body = await request.json()
        action = body.get("action", "accept")
    except:
        action = "accept"
    if action not in ["accept", "propose_edit", "escalate"]:
        return StepResponse(state=None, reward=0.01, done=True)
    next_state, reward, done, _ = get_env().step(action)
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
