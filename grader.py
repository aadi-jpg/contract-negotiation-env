# grader.py
from openenv.core.rubrics import Rubric

def _compute(action, state):
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
    return 0.01

class EasyRubric(Rubric):
    def forward(self, action, observation) -> float:
        return _compute(action, observation)

class MediumRubric(Rubric):
    def forward(self, action, observation) -> float:
        return _compute(action, observation)

class HardRubric(Rubric):
    def forward(self, action, observation) -> float:
        return _compute(action, observation)

easy = EasyRubric()
medium = MediumRubric()
hard = HardRubric()

def grade_action(state, action):
    return _compute(action, state)
