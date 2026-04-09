# grader.py

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

def grade_action(state, action):
    return _score(action, state)

def easy(state, action):
    return _score(action, state)

def medium(state, action):
    return _score(action, state)

def hard(state, action):
    return _score(action, state)
