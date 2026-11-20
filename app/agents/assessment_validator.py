
from collections import Counter

from app.schemas.assessment import (
    Assessment,
    AssessmentReview,
    ReviewIssue
)
from app.graph.state import TalentLensState


def validate_assessment(state: TalentLensState) -> dict:

    assessment = state["assessment"]
    plan = assessment.assessment_plan

    issues = []

    # --------------------------------------------------
    # 1. VALIDATE TOTAL QUESTION COUNT
    # --------------------------------------------------

    actual_total = len(assessment.questions)

    if actual_total != plan.total_questions:

        issues.append(
            ReviewIssue(
                issue_type="question_count_mismatch",
                description=(
                    f"Expected {plan.total_questions} questions, "
                    f"but generated {actual_total}."
                ),
                suggested_fix=(
                    "Generate the exact number of questions "
                    "specified in the assessment plan."
                )
            )
        )

    # --------------------------------------------------
    # 2. VALIDATE SKILL DISTRIBUTION
    # --------------------------------------------------

    generated_skill_counts = Counter(
        question.skill_name.strip().casefold()
        for question in assessment.questions
    )

    for skill in plan.skill_assessments:

        skill_key = skill.skill_name.strip().casefold()

        expected_count = skill.question_count
        actual_count = generated_skill_counts.get(skill_key, 0)

        if actual_count != expected_count:

            issues.append(
                ReviewIssue(
                    issue_type="skill_distribution_mismatch",
                    description=(
                        f"Skill '{skill.skill_name}': expected "
                        f"{expected_count} questions, but generated "
                        f"{actual_count}."
                    ),
                    suggested_fix=(
                        f"Generate exactly {expected_count} questions "
                        f"for {skill.skill_name}."
                    )
                )
            )

    # --------------------------------------------------
    # 3. VALIDATE DIFFICULTY
    # --------------------------------------------------

    planned_difficulties = {
        skill.skill_name.strip().casefold(): skill.difficulty
        for skill in plan.skill_assessments
    }

    for question in assessment.questions:

        skill_key = question.skill_name.strip().casefold()
        expected_difficulty = planned_difficulties.get(skill_key)

        if (
            expected_difficulty is not None
            and question.difficulty != expected_difficulty
        ):

            issues.append(
                ReviewIssue(
                    issue_type="difficulty_mismatch",
                    question_id=question.question_id,
                    description=(
                        f"Question difficulty for '{question.skill_name}' "
                        f"is {question.difficulty.value}, but the plan "
                        f"requires {expected_difficulty.value}."
                    ),
                    suggested_fix=(
                        f"Adjust the question difficulty to "
                        f"{expected_difficulty.value}."
                    )
                )
            )

    # --------------------------------------------------
    # 4. VALIDATE QUESTION TYPES
    # --------------------------------------------------

    planned_question_types = {
        skill.skill_name.strip().casefold(): set(skill.question_types)
        for skill in plan.skill_assessments
    }

    for question in assessment.questions:

        skill_key = question.skill_name.strip().casefold()
        allowed_types = planned_question_types.get(skill_key)

        if (
            allowed_types is not None
            and question.question_type not in allowed_types
        ):

            issues.append(
                ReviewIssue(
                    issue_type="question_type_mismatch",
                    question_id=question.question_id,
                    description=(
                        f"Question type '{question.question_type.value}' "
                        f"is not allowed for skill '{question.skill_name}'."
                    ),
                    suggested_fix=(
                        "Use one of the question types specified "
                        "in the assessment plan."
                    )
                )
            )

    # --------------------------------------------------
    # 5. VALIDATE QUESTION MARKS
    # --------------------------------------------------

    for question in assessment.questions:

        if question.max_marks <= 0:

            issues.append(
                ReviewIssue(
                    issue_type="invalid_marks",
                    question_id=question.question_id,
                    description="Question has non-positive marks.",
                    suggested_fix="Assign positive marks to the question."
                )
            )

        if not question.evaluation_rubric:

            issues.append(
                ReviewIssue(
                    issue_type="missing_rubric",
                    question_id=question.question_id,
                    description="Question has no evaluation rubric.",
                    suggested_fix="Add measurable evaluation criteria."
                )
            )

    # --------------------------------------------------
    # 6. VALIDATE TIME LIMIT
    # --------------------------------------------------

    total_question_time = sum(
        question.time_limit_minutes
        for question in assessment.questions
    )

    if total_question_time > plan.duration_minutes:

        issues.append(
            ReviewIssue(
                issue_type="time_limit_exceeded",
                description=(
                    f"Total question time is {total_question_time} minutes, "
                    f"but assessment duration is "
                    f"{plan.duration_minutes} minutes."
                ),
                suggested_fix=(
                    "Reduce individual question time limits or "
                    "increase the assessment duration."
                )
            )
        )

    # --------------------------------------------------
    # 7. VALIDATE DUPLICATE QUESTION IDS
    # --------------------------------------------------

    question_ids = [
        question.question_id
        for question in assessment.questions
    ]

    id_counts = Counter(question_ids)

    for question_id, count in id_counts.items():

        if count > 1:

            issues.append(
                ReviewIssue(
                    issue_type="duplicate_question_id",
                    question_id=question_id,
                    description=(
                        f"Question ID '{question_id}' appears "
                        f"{count} times."
                    ),
                    suggested_fix=(
                        "Assign a unique ID to every assessment question."
                    )
                )
            )

    # --------------------------------------------------
    # 8. BUILD REVIEW RESULT
    # --------------------------------------------------

    is_valid = len(issues) == 0

    if is_valid:
        overall_feedback = (
            "Assessment passed all deterministic validation checks."
        )
    else:
        overall_feedback = (
            f"Assessment failed validation with {len(issues)} issue(s)."
        )

    review = AssessmentReview(
        is_valid=is_valid,
        overall_feedback=overall_feedback,
        issues=issues,
        revision_suggestions=[
            issue.suggested_fix for issue in issues
        ]
    )

    return {
        "review_result": review,
        "is_valid": is_valid,
        "review_feedback": overall_feedback
    }
