from graders.medium import grade

TASK_ID = "medium"
DESCRIPTION = "Intermediate contract clause evaluation"

def get_task():
    return {
        "id": TASK_ID,
        "description": DESCRIPTION,
        "grader": grade
    }
