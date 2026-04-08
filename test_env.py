from env import ContractEnv
from grader import compute_score

env = ContractEnv(task="easy")

state = env.reset()

print("\n--- CONTRACT ENV STARTED ---")
print("Initial State:\n", state)

done = False
total_reward = 0
max_reward = len(env.data) * 1.0  # max possible

while not done:
    print("\nChoose action:")
    print("1 → accept")
    print("2 → propose_edit")
    print("3 → escalate")

    choice = input("Enter 1/2/3: ")

    if choice == "1":
        action = "accept"
    elif choice == "2":
        action = "propose_edit"
    elif choice == "3":
        action = "escalate"
    else:
        print("Invalid input, try again.")
        continue

    state, reward, done, _ = env.step(action)

    total_reward += reward

    print("\nReward:", reward)
    print("Next State:", state)
    print("Done:", done)

# FINAL SCORE
score = compute_score(total_reward, max_reward)

print("\n--- FINAL RESULTS ---")
print("Total Reward:", total_reward)
print("Normalized Score (0–1):", score)