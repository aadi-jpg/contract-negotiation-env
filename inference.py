# inference.py

def act(state):
    """
    OpenEnv-compatible inference function
    """

    # safe extraction
    clause = state.get("clause", "").lower()
    policy = state.get("policy", "").lower()
    risk = state.get("risk_level", "")
    importance = state.get("vendor_importance", "")

    # logic
    if clause == policy:
        return "accept"

    if risk == "high":
        if importance == "high":
            return "propose_edit"
        return "escalate"

    if risk == "low":
        return "propose_edit"

    return "accept"