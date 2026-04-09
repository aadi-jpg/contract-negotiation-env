# env.py
import json

class ContractEnv:
    def __init__(self, task="easy"):
        self.task = task
        self.data = self.load_data(task)
        self.index = 0

    def load_data(self, task):
        file_path = f"data/{task}.json"
        with open(file_path, "r") as f:
            return json.load(f)

    def reset(self):
        self.index = 0
        return self.data[self.index]["state"]

    def step(self, action):
        item = self.data[self.index]
        correct_action = item["correct_action"]
        reward = self._get_reward(action, correct_action)
        self.index += 1
        done = self.index >= len(self.data)
        next_state = self.data[self.index]["state"] if not done else None
        return next_state, reward, done, {}

    def state(self):
        return self.data[self.index]["state"]

    def _get_reward(self, action, correct_action):
        if action == correct_action:
            return 0.99
        if action == "escalate":
            if correct_action == "propose_edit":
                return 0.6
            elif correct_action == "accept":
                return 0.01
            else:
                return 0.8
        if action == "accept" and correct_action == "propose_edit":
            return 0.01
        if action == "propose_edit" and correct_action == "accept":
            return 0.3
        return 0.01
