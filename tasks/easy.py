from graders.easy import grade

TASK_ID = "easy"
DESCRIPTION = "Basic contract clause evaluation"

def get_task():
    return {
        "id": TASK_ID,
        "description": DESCRIPTION,
        "grader": grade
    }
