import requests
import json

API_URL = "https://aadiv123-contract-env.hf.space"


def get_state():
    res = requests.get(f"{API_URL}/state")
    return res.json()["state"]


def take_action(action):
    res = requests.post(f"{API_URL}/step", json={"action": action})
    return res.json()


# 🔹 Rule-based agent
def rule_agent(state):
    clause = state["clause"].lower()
    policy = state["policy"].lower()

    if clause == policy:
        return "accept"

    if state["risk_level"] == "high":
        return "escalate"

    return "propose_edit"


# 🔹 LLM + HYBRID agent (FIXED)
def llm_agent(state):
    prompt = f"""
Clause: {state['clause']}
Policy: {state['policy']}
Risk: {state['risk_level']}
Importance: {state['vendor_importance']}

Respond with ONE WORD:
accept
propose_edit
escalate
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
        )

        text = response.json().get("response", "").strip().lower()

        # 🔥 SAFE PARSE
        words = text.split()
        first_word = words[0] if len(words) > 0 else ""

        # 🔥 HYBRID OPTIMAL LOGIC

        clause = state["clause"].lower()
        policy = state["policy"].lower()
        risk = state["risk_level"]
        importance = state["vendor_importance"]

        # perfect match → accept
        if clause == policy:
            return "accept"

        # high risk → controlled decision
        if risk == "high":
            if importance == "high":
                return "propose_edit"
            return "escalate"

        # low risk → prefer edit
        if risk == "low":
            return "propose_edit"

        # fallback to LLM signal
        if "accept" in first_word:
            return "accept"
        elif "propose" in first_word:
            return "propose_edit"
        else:
            return "escalate"

    except:
        return "escalate"


def run_episode(agent_func):
    requests.post(f"{API_URL}/reset")

    total_reward = 0

    while True:
        state = get_state()
        action = agent_func(state)

        result = take_action(action)

        total_reward += result["reward"]

        if result["done"]:
            break

    return total_reward


def evaluate(agent_func, name, episodes=5):
    scores = []

    for _ in range(episodes):
        score = run_episode(agent_func)
        scores.append(score)

    avg = sum(scores) / len(scores)

    print(f"\n{name} RESULTS")
    print("Scores:", scores)
    print("Average:", avg)


if __name__ == "__main__":
    evaluate(rule_agent, "Rule Agent")
    evaluate(llm_agent, "LLM Agent")