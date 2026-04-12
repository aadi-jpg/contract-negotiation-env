from graders.hard import grade

TASK_ID = "hard"
DESCRIPTION = "Advanced contract clause evaluation"

def get_task():
    return {
        "id": TASK_ID,
        "description": DESCRIPTION,
        "grader": grade
    }
