from pydantic import BaseModel
from typing import Optional


class State(BaseModel):
    clause: str
    policy: str
    risk_level: str
    vendor_importance: str


class StepRequest(BaseModel):
    action: str


class StepResponse(BaseModel):
    state: Optional[dict]  # allows None
    reward: float
    done: bool