from fastapi import FastAPI
from env import ContractEnv
from models import StepRequest, StepResponse
import uvicorn

app = FastAPI()
env = ContractEnv(task="easy")

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

@app.get("/health")
def health():
    return {"status": "ok"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
