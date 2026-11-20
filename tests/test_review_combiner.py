
from app.agents.review_combiner import combine_reviews
from app.schemas.assessment import AssessmentReview, ReviewIssue


# --------------------------------------------------
# 1. CREATE MOCK REVIEW
# --------------------------------------------------

def create_review(is_valid=True, issue_type=None):

    issues = []
    suggestions = []

    if issue_type:
        issues.append(
            ReviewIssue(
                issue_type=issue_type,
                question_id="q1",
                description="Test validation issue.",
                suggested_fix="Fix the identified problem."
            )
        )

        suggestions.append("Fix the identified problem.")

    return AssessmentReview(
        is_valid=is_valid,
        overall_feedback="Test review feedback.",
        issues=issues,
        revision_suggestions=suggestions
    )


# --------------------------------------------------
# 2. CREATE TEST STATE
# --------------------------------------------------

def create_test_state(deterministic_valid, quality_valid):

    return {
        "review_result": create_review(
            deterministic_valid,
            "difficulty_mismatch" if not deterministic_valid else None
        ),

        "quality_review": create_review(
            quality_valid,
            "technical_accuracy" if not quality_valid else None
        )
    }


# --------------------------------------------------
# 3. BOTH REVIEWS PASS
# --------------------------------------------------

def test_both_reviews_pass():

    state = create_test_state(True, True)

    result = combine_reviews(state)

    assert result["is_valid"] is True
    assert result["final_review"].is_valid is True
    assert len(result["final_review"].issues) == 0

    assert (
        "passed deterministic and LLM quality checks"
        in result["review_feedback"]
    )

    print("\nBoth reviews passed!")


# --------------------------------------------------
# 4. DETERMINISTIC REVIEW FAILS
# --------------------------------------------------

def test_deterministic_review_fails():

    state = create_test_state(False, True)

    result = combine_reviews(state)

    assert result["is_valid"] is False
    assert result["final_review"].is_valid is False
    assert len(result["final_review"].issues) == 1

    assert "difficulty_mismatch" in result["review_feedback"]
    assert "Fix the identified problem." in result["review_feedback"]

    print("\nDeterministic review failure detected!")


# --------------------------------------------------
# 5. QUALITY REVIEW FAILS
# --------------------------------------------------

def test_quality_review_fails():

    state = create_test_state(True, False)

    result = combine_reviews(state)

    assert result["is_valid"] is False
    assert result["final_review"].is_valid is False
    assert len(result["final_review"].issues) == 1

    assert "technical_accuracy" in result["review_feedback"]
    assert "Fix the identified problem." in result["review_feedback"]

    print("\nQuality review failure detected!")


# --------------------------------------------------
# 6. BOTH REVIEWS FAIL
# --------------------------------------------------

def test_both_reviews_fail():

    state = create_test_state(False, False)

    result = combine_reviews(state)

    assert result["is_valid"] is False
    assert result["final_review"].is_valid is False

    assert len(result["final_review"].issues) == 2
    assert len(result["final_review"].revision_suggestions) == 2

    assert "difficulty_mismatch" in result["review_feedback"]
    assert "technical_accuracy" in result["review_feedback"]

    assert "Fix the identified problem." in result["review_feedback"]

    print("\nBoth review failures detected!")


# --------------------------------------------------
# 7. RUN ALL TESTS
# --------------------------------------------------

if __name__ == "__main__":

    test_both_reviews_pass()
    test_deterministic_review_fails()
    test_quality_review_fails()
    test_both_reviews_fail()

    print("\nAll review combiner tests passed!")
