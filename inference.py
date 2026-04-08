# inference.py

def act(state):
    """
    OpenEnv-compatible inference function
    """

    clause = state.get("clause", "").lower()
    policy = state.get("policy", "").lower()
    risk = state.get("risk_level", "")
    importance = state.get("vendor_importance", "")

    # exact match → accept
    if clause == policy:
        return "accept"

    # high risk → escalate or edit
    if risk == "high":
        if importance == "high":
            return "propose_edit"
        return "escalate"

    # low risk → edit
    if risk == "low":
        return "propose_edit"

    # fallback
    return "accept"