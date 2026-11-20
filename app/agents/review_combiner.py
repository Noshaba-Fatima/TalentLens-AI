
from app.graph.state import TalentLensState
from app.schemas.assessment import AssessmentReview


def combine_reviews(state: TalentLensState) -> dict:

    deterministic_review = state["review_result"]
    quality_review = state["quality_review"]

    combined_issues = (
        deterministic_review.issues
        + quality_review.issues
    )

    combined_suggestions = (
        deterministic_review.revision_suggestions
        + quality_review.revision_suggestions
    )

    is_valid = (
        deterministic_review.is_valid
        and quality_review.is_valid
    )

    if is_valid:
        overall_feedback = (
            "Assessment passed deterministic and LLM quality checks."
        )

        revision_feedback = overall_feedback

    else:
        overall_feedback = (
            f"Assessment failed review with "
            f"{len(combined_issues)} issue(s)."
        )

        # Give the question generator actionable feedback
        feedback_parts = []

        for issue in combined_issues:
            feedback_parts.append(
                f"""
                Issue: {issue.issue_type}
                Question ID: {issue.question_id}
                Description: {issue.description}
                Suggested Fix: {issue.suggested_fix}
                """
            )

        revision_feedback = (
            overall_feedback
            + "\n\nDetailed review feedback:\n"
            + "\n".join(feedback_parts)
        )

    final_review = AssessmentReview(
        is_valid=is_valid,
        overall_feedback=overall_feedback,
        issues=combined_issues,
        revision_suggestions=combined_suggestions
    )

    return {
        "final_review": final_review,
        "is_valid": is_valid,
        "review_feedback": revision_feedback
    }
