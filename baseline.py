# baseline.py

from env import ContractEnv
from grader import compute_score


def agent_policy(state):
    """
    Simple rule-based agent
    """

    clause = state["clause"].lower()
    policy = state["policy"].lower()
    risk = state["risk_level"]
    importance = state["vendor_importance"]

    # HIGH RISK → escalate
    if risk == "high":
        return "escalate"

    # Payment mismatch → edit
    if "payment" in clause and "30 days" in policy:
        if "7 days" in clause or "15 days" in clause or "20 days" in clause:
            return "propose_edit"

    # Liability mismatch → edit
    if "liability" in clause and "shared" in policy:
        if "no liability" in clause or "zero liability" in clause:
            return "propose_edit"

    # Very important vendor → escalate instead of reject
    if importance in ["very_high", "high"] and risk == "medium":
        return "escalate"

    # Default safe action
    return "accept"


def run_env(task="easy"):
    env = ContractEnv(task=task)

    state = env.reset()

    total_reward = 0
    max_reward = len(env.data) * 1.0

    done = False

    print(f"\n--- RUNNING BASELINE AGENT ({task.upper()}) ---")

    while not done:
        action = agent_policy(state)

        state, reward, done, _ = env.step(action)

        total_reward += reward

        print(f"Action: {action} | Reward: {reward}")

    score = compute_score(total_reward, max_reward)

    print("\n--- FINAL RESULTS ---")
    print("Total Reward:", total_reward)
    print("Score (0–1):", score)


if __name__ == "__main__":
    run_env("easy")