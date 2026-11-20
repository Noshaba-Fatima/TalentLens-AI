
from app.graph.workflow import talentlens_graph
from app.schemas.assessment import Assessment


def test_complete_workflow():

    jd_text = """
    We are hiring a Python Backend Developer with 2-3 years
    of experience.

    Required skills:
    - Python
    - FastAPI
    - PostgreSQL
    - Docker

    Responsibilities:
    - Build REST APIs using FastAPI.
    - Design and optimize database queries.
    - Write clean, maintainable Python code.
    - Containerize applications using Docker.
    - Handle API errors and improve backend performance.
    """

    result = talentlens_graph.invoke({
        "jd_text": jd_text,
        "revision_count": 0
    })

    print("\n========== WORKFLOW RESULT ==========")

    print("\nJob Title:")
    print(result["job_description"].job_title)

    print("\nTotal Questions:")
    print(len(result["assessment"].questions))

    print("\nRevision Attempts:")
    print(result.get("revision_count", 0))

    print("\nFinal Review:")
    print(result["final_review"].model_dump_json(indent=2))

    print("\nAssessment Status:")
    print("APPROVED" if result["is_valid"] else "REJECTED")

    assert isinstance(result["assessment"], Assessment)
    assert result["final_review"] is not None
    assert result["revision_count"] <= 2

    print("\nEnd-to-end workflow test completed!")


if __name__ == "__main__":
    test_complete_workflow()
