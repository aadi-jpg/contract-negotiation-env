# env.py

# This file defines your Contract Environment

import json  # used to read your dataset files


class ContractEnv:
    def __init__(self, task="easy"):
        """
        task: difficulty level (easy / medium / hard)
        """
        self.task = task
        self.data = self.load_data(task)  # load dataset
        self.index = 0  # keeps track of current step

    def load_data(self, task):
        """
        Loads JSON file based on difficulty
        """
        file_path = f"data/{task}.json"

        with open(file_path, "r") as f:
            data = json.load(f)

        return data

    def reset(self):
        """
        Resets environment to beginning
        """
        self.index = 0
        return self.data[self.index]["state"]

    def step(self, action):
        """
        Takes an action and returns:
        next_state, reward, done, info
        """

        # Current data item
        item = self.data[self.index]

        # Correct action (ground truth)
        correct_action = item["correct_action"]

        # Compute reward
        reward = self._get_reward(action, correct_action)

        # Move to next step
        self.index += 1

        # Check if finished
        done = self.index >= len(self.data)

        # Get next state (if not done)
        if not done:
            next_state = self.data[self.index]["state"]
        else:
            next_state = None

        return next_state, reward, done, {}

    def state(self):
        """
        Returns current state
        """
        return self.data[self.index]["state"]

    def _get_reward(self, action, correct_action):
        """
        Improved reward logic with partial credit
        """

        # Perfect decision
        if action == correct_action:
            return 1.0

        # Safe fallback: escalation
        if action == "escalate":
            if correct_action == "propose_edit":
                return 0.6  # cautious but acceptable
            elif correct_action == "accept":
                return -0.2  # unnecessary escalation
            else:
                return 0.8  # correct escalation

        # Accept when should edit → risky
        if action == "accept" and correct_action == "propose_edit":
            return -0.7

        # Edit when accept → slightly inefficient
        if action == "propose_edit" and correct_action == "accept":
            return 0.3

        # Everything else
        return -1.0