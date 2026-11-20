
from app.graph.state import TalentLensState


initial_state: TalentLensState = {
    "jd_text": """
    We are hiring a Python Backend Developer
    with experience in FastAPI, PostgreSQL,
    REST APIs and Docker.
    """
}

print("Initial State:")
print(initial_state)

print("\nJD Text:")
print(initial_state["jd_text"])

print("\nState initialized successfully!")
