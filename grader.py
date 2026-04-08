# grader.py

def compute_score(total_reward, max_possible_reward):
    """
    Normalize score between 0 and 1
    """
    if max_possible_reward == 0:
        return 0.0

    score = total_reward / max_possible_reward

    # Clamp between 0 and 1
    return max(0.0, min(1.0, score))