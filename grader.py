# grader.py
def grade_action(state, action):
    """
    Returns reward based on correctness of action
    """
    clause = state.get("clause", "").lower()
    policy = state.get("policy", "").lower()
    risk = state.get("risk_level", "")
    importance = state.get("vendor_importance", "")

    # Case 1: perfect match → accept
    if clause == policy:
        if action == "accept":
            return 0.99
        else:
            return 0.01

    # Case 2: high risk conflicts
    if risk == "high":
        if importance == "high":
            if action == "propose_edit":
                return 0.99
            elif action == "escalate":
                return 0.6
            else:
                return 0.01
        else:
            if action == "escalate":
                return 0.6
            elif action == "propose_edit":
                return 0.8
            else:
                return 0.01

    # Case 3: low risk → prefer edit
    if risk == "low":
        if action == "propose_edit":
            return 0.99
        elif action == "accept":
            return 0.8
        else:
            return 0.01

    # fallback
    return 0.01