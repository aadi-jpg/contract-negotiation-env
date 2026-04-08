import os
from openai import OpenAI
from env import ContractEnv

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
TASK_NAME = os.getenv("TASK_NAME", "easy")
BENCHMARK = "contract-negotiation-env"
MAX_STEPS = 10

SYSTEM_PROMPT = """
You are a contract negotiation agent. Given a contract clause, policy, risk level,
and vendor importance, decide the best action.
Reply with exactly one word only: accept, propose_edit, or escalate.
"""

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def get_action(client, state):
    prompt = f"""
Clause: {state.get('clause')}
Policy: {state.get('policy')}
Risk Level: {state.get('risk_level')}
Vendor Importance: {state.get('vendor_importance')}
Reply with exactly one word: accept, propose_edit, or escalate.
"""
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=10,
        )
        action = completion.choices[0].message.content.strip().lower()
        if action not in ["accept", "propose_edit", "escalate"]:
            return "accept"
        return action
    except Exception as e:
        print(f"[DEBUG] Model error: {e}", flush=True)
        return "accept"

def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = ContractEnv(task=TASK_NAME)

    rewards = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        state = env.reset()

        for step in range(1, MAX_STEPS + 1):
            action = get_action(client, state)
            state, reward, done, _ = env.step(action)

            rewards.append(reward)
            steps_taken = step
            log_step(step=step, action=action, reward=reward, done=done, error=None)

            if done:
                break

        score = sum(rewards) / steps_taken if steps_taken > 0 else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= 0.5

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

if __name__ == "__main__":
    main()