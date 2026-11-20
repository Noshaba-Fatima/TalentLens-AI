
from app.agents.assessment_validator import validate_assessment

from app.graph.state import TalentLensState

from app.schemas.job_description import JobDescription

from app.schemas.assessment import (
    Assessment,
    AssessmentPlan,
    AssessmentQuestion,
    SkillAssessment,
    QuestionType,
    Difficulty
)


def create_test_state(invalid=False):

    assessment_plan = AssessmentPlan(
        total_questions=3,
        duration_minutes=30,
        skill_assessments=[
            SkillAssessment(
                skill_name="Python",
                question_types=[QuestionType.CODING],
                difficulty=Difficulty.MEDIUM,
                question_count=2,
                weightage=60
            ),
            SkillAssessment(
                skill_name="FastAPI",
                question_types=[QuestionType.SCENARIO],
                difficulty=Difficulty.MEDIUM,
                question_count=1,
                weightage=40
            )
        ]
    )

    questions = [
        AssessmentQuestion(
            question_id="q1",
            skill_name="Python",
            question_text="Write a function to reverse a string.",
            question_type=QuestionType.CODING,
            difficulty=Difficulty.MEDIUM,
            max_marks=10,
            time_limit_minutes=10,
            evaluation_rubric=["Correct logic", "Edge cases"],
            expected_answer="Use slicing or a loop."
        ),
        AssessmentQuestion(
            question_id="q2",
            skill_name="Python",
            question_text="Implement a function to find duplicates.",
            question_type=QuestionType.CODING,
            difficulty=Difficulty.MEDIUM,
            max_marks=10,
            time_limit_minutes=10,
            evaluation_rubric=["Correct logic", "Efficiency"],
            expected_answer="Use a set to track seen elements."
        ),
        AssessmentQuestion(
            question_id="q3",
            skill_name="FastAPI",
            question_text="Design an authenticated API endpoint.",
            question_type=QuestionType.SCENARIO,
            difficulty=Difficulty.MEDIUM,
            max_marks=10,
            time_limit_minutes=10,
            evaluation_rubric=["Authentication", "Validation"],
            expected_answer="Use dependency injection for authentication."
        )
    ]

    if invalid:

        # Deliberately introduce validation errors
        questions[0].difficulty = Difficulty.HARD
        questions[1].question_type = QuestionType.SQL
        questions[2].question_id = "q1"

    assessment = Assessment(
        assessment_id="assessment-001",
        job_title="Python Backend Developer",
        assessment_plan=assessment_plan,
        questions=questions
    )

    state: TalentLensState = {
        "jd_text": "Python Backend Developer",
        "assessment": assessment
    }

    return state


def run_validator_with_modified_state(modifications):

    state = create_test_state()

    assessment = state["assessment"]

    modifications(assessment)

    return validate_assessment(state)

def test_question_count_mismatch():

    def modify(assessment):
        assessment.questions.pop()

    result = run_validator_with_modified_state(modify)

    issue_types = {
        issue.issue_type
        for issue in result["review_result"].issues
    }

    assert result["is_valid"] is False
    assert "question_count_mismatch" in issue_types

    print("\nQuestion count mismatch test passed!")

def test_skill_distribution_mismatch():

    def modify(assessment):
        assessment.questions[2].skill_name = "Python"

    result = run_validator_with_modified_state(modify)

    issue_types = {
        issue.issue_type
        for issue in result["review_result"].issues
    }

    assert result["is_valid"] is False
    assert "skill_distribution_mismatch" in issue_types

    print("\nSkill distribution test passed!")

def test_time_limit_exceeded():

    def modify(assessment):
        assessment.questions[0].time_limit_minutes = 20

    result = run_validator_with_modified_state(modify)

    issue_types = {
        issue.issue_type
        for issue in result["review_result"].issues
    }

    assert result["is_valid"] is False
    assert "time_limit_exceeded" in issue_types

    print("\nTime limit test passed!")

def test_missing_rubric():

    def modify(assessment):
        assessment.questions[0].evaluation_rubric = []

    result = run_validator_with_modified_state(modify)

    issue_types = {
        issue.issue_type
        for issue in result["review_result"].issues
    }

    assert result["is_valid"] is False
    assert "missing_rubric" in issue_types

    print("\nMissing rubric test passed!")


def test_valid_assessment():

    state = create_test_state(invalid=False)

    result = validate_assessment(state)

    review = result["review_result"]

    print("\nVALID ASSESSMENT RESULT")
    print(review.model_dump_json(indent=4))

    assert result["is_valid"] is True
    assert len(review.issues) == 0

    print("\nValid assessment test passed!")


def test_invalid_assessment():

    state = create_test_state(invalid=True)

    result = validate_assessment(state)

    review = result["review_result"]

    print("\nINVALID ASSESSMENT RESULT")
    print(review.model_dump_json(indent=4))

    assert result["is_valid"] is False

    issue_types = {
        issue.issue_type for issue in review.issues
    }

    assert "difficulty_mismatch" in issue_types
    assert "question_type_mismatch" in issue_types
    assert "duplicate_question_id" in issue_types

    print("\nInvalid assessment test passed!")


if __name__ == "__main__":

    test_valid_assessment()
    test_invalid_assessment()

    test_question_count_mismatch()
    test_skill_distribution_mismatch()
    test_time_limit_exceeded()
    test_missing_rubric()
