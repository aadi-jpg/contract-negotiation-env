# llm_agent.py

import requests
import json

API_URL = "https://aadiv123-contract-env.hf.space"


def get_state():
    """
    Calls /state endpoint and returns current state
    """
    res = requests.get(f"{API_URL}/state")
    data = res.json()
    return data["state"]


def take_action(action):
    """
    Sends action to /step endpoint
    """
    res = requests.post(
        f"{API_URL}/step",
        json={"action": action}
    )
    return res.json()


def llm_decision(state):
    """
    Uses LOCAL LLM via Ollama (lightweight model)
    """

    prompt = f"""
You are a contract negotiation agent.

Your goal is to MAXIMIZE reward.

Rules:
- accept → best if clause matches policy (reward = 1.0)
- propose_edit → for mismatches (reward = 1.0 if correct)
- escalate → only if high risk conflict (reward = 0.6)

IMPORTANT:
- Do NOT escalate unless absolutely necessary
- Prefer propose_edit over escalate

Respond with ONLY ONE WORD:
accept
propose_edit
escalate

Clause: {state['clause']}
Policy: {state['policy']}
Risk: {state['risk_level']}
Importance: {state['vendor_importance']}
"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",  # or "tinyllama"
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()

        text = result.get("response", "").strip().lower()

        print("LLM OUTPUT:", text)

        # 🔥 SAFE FIRST WORD EXTRACTION
        words = text.split()
        first_word = words[0] if len(words) > 0 else ""

        # 🔥 HYBRID DECISION (LLM + RULE CORRECTION)

        # Rule 1: perfect match → always accept
        if state["clause"].lower() == state["policy"].lower():
            return "accept"

        # Rule 2: high risk → avoid blind accept
        if state["risk_level"] == "high":
            if "accept" in first_word:
                return "propose_edit"
            return "escalate"

        # Rule 3: low risk → prefer edit over escalate
        if state["risk_level"] == "low":
            if "escalate" in first_word:
                return "propose_edit"

        # fallback to LLM decision
        if "accept" in first_word:
            return "accept"
        elif "propose" in first_word or "edit" in first_word:
            return "propose_edit"
        else:
            return "escalate"

    except Exception as e:
        print("OLLAMA ERROR:", e)
        return "escalate"

    except Exception as e:
        print("OLLAMA ERROR:", e)
        return "escalate"


def run_episode():
    """
    Runs one full episode
    """

    requests.post(f"{API_URL}/reset")

    total_reward = 0

    while True:
        state = get_state()

        print("\nSTATE:")
        print(json.dumps(state, indent=2))

        action = llm_decision(state)

        print(f"\nACTION: {action}")

        result = take_action(action)

        reward = result["reward"]
        done = result["done"]

        total_reward += reward

        print(f"REWARD: {reward} | DONE: {done}")

        if done:
            break

    print("\nFINAL SCORE:", total_reward)


if __name__ == "__main__":
    run_episode()