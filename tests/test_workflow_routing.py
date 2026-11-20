
from app.graph.workflow import route_after_review, prepare_revision


def test_valid_assessment_ends():
    state = {
        "is_valid": True,
        "revision_count": 0
    }

    assert route_after_review(state) == "end"


def test_invalid_assessment_gets_revision():
    state = {
        "is_valid": False,
        "revision_count": 0
    }

    assert route_after_review(state) == "revise"


def test_second_revision_is_allowed():
    state = {
        "is_valid": False,
        "revision_count": 1
    }

    assert route_after_review(state) == "revise"


def test_retry_limit_stops_workflow():
    state = {
        "is_valid": False,
        "revision_count": 2
    }

    assert route_after_review(state) == "end"


def test_prepare_revision_increments_counter():
    state = {
        "revision_count": 0
    }

    result = prepare_revision(state)

    assert result["revision_count"] == 1


if __name__ == "__main__":
    test_valid_assessment_ends()
    test_invalid_assessment_gets_revision()
    test_second_revision_is_allowed()
    test_retry_limit_stops_workflow()
    test_prepare_revision_increments_counter()

    print("All workflow routing tests passed!")
