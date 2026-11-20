
from app.agents.quality_reviewer import review_assessment_quality
from app.schemas.job_description import (
    JobDescription,
    Skill,
    SkillCategory,
    ProficiencyLevel
)
from app.schemas.assessment import (
    Assessment,
    AssessmentPlan,
    AssessmentQuestion,
    SkillAssessment,
    QuestionType,
    Difficulty
)


def create_test_state():

    # --------------------------------------------------
    # 1. JOB DESCRIPTION
    # --------------------------------------------------

    job_description = JobDescription(
        job_title="Python Backend Developer",
        experience_min=2,
        experience_max=4,
        responsibilities=[
            "Develop REST APIs",
            "Work with relational databases",
            "Build and maintain backend services"
        ],
        required_skills=[
            Skill(
                name="Python",
                category=SkillCategory.PROGRAMMING,
                proficiency=ProficiencyLevel.ADVANCED,
                is_required=True
            ),
            Skill(
                name="FastAPI",
                category=SkillCategory.FRAMEWORK,
                proficiency=ProficiencyLevel.INTERMEDIATE,
                is_required=True
            ),
            Skill(
                name="PostgreSQL",
                category=SkillCategory.DATABASE,
                proficiency=ProficiencyLevel.INTERMEDIATE,
                is_required=True
            )
        ],
        preferred_skills=[],
        additional_requirements=[]
    )

    # --------------------------------------------------
    # 2. ASSESSMENT PLAN
    # --------------------------------------------------

    assessment_plan = AssessmentPlan(
        total_questions=3,
        duration_minutes=30,
        skill_assessments=[
            SkillAssessment(
                skill_name="Python",
                question_types=[QuestionType.CODING],
                difficulty=Difficulty.MEDIUM,
                question_count=1,
                weightage=40
            ),
            SkillAssessment(
                skill_name="FastAPI",
                question_types=[QuestionType.SCENARIO],
                difficulty=Difficulty.MEDIUM,
                question_count=1,
                weightage=30
            ),
            SkillAssessment(
                skill_name="PostgreSQL",
                question_types=[QuestionType.SQL],
                difficulty=Difficulty.MEDIUM,
                question_count=1,
                weightage=30
            )
        ]
    )

    # --------------------------------------------------
    # 3. ASSESSMENT QUESTIONS
    # --------------------------------------------------

    questions = [

        AssessmentQuestion(
            question_id="q1",
            skill_name="Python",
            question_text=(
                "Write a Python function that returns the frequency "
                "of each word in a given sentence. Ignore case."
            ),
            question_type=QuestionType.CODING,
            difficulty=Difficulty.MEDIUM,
            max_marks=10,
            time_limit_minutes=10,
            evaluation_rubric=[
                "Correctly tokenizes the sentence into words.",
                "Handles case-insensitive counting.",
                "Returns the correct frequency mapping.",
                "Uses an appropriate data structure."
            ],
            expected_answer=(
                "Use a dictionary or collections.Counter. Convert "
                "the sentence to lowercase, split it into words, "
                "and count each word."
            )
        ),

        AssessmentQuestion(
            question_id="q2",
            skill_name="FastAPI",
            question_text=(
                "Design a FastAPI endpoint that allows an authenticated "
                "user to retrieve their own profile. Explain how you "
                "would prevent one user from accessing another user's data."
            ),
            question_type=QuestionType.SCENARIO,
            difficulty=Difficulty.MEDIUM,
            max_marks=10,
            time_limit_minutes=10,
            evaluation_rubric=[
                "Uses dependency injection for authentication.",
                "Identifies the current authenticated user.",
                "Restricts profile access to that user.",
                "Handles unauthorized access appropriately."
            ],
            expected_answer=(
                "Use an authentication dependency such as "
                "Depends(get_current_user). Retrieve the current user "
                "from the validated token and use that user's ID "
                "when querying the database. Do not trust a user ID "
                "provided by the request."
            )
        ),

        AssessmentQuestion(
            question_id="q3",
            skill_name="PostgreSQL",
            question_text=(
                "Write an SQL query to retrieve the total number "
                "of orders placed by each customer."
            ),
            question_type=QuestionType.SQL,
            difficulty=Difficulty.MEDIUM,
            max_marks=10,
            time_limit_minutes=10,
            evaluation_rubric=[
                "Uses GROUP BY on customer_id.",
                "Uses COUNT correctly.",
                "Returns the customer identifier and order count."
            ],
            expected_answer=(
                "SELECT customer_id, COUNT(*) AS order_count "
                "FROM orders GROUP BY customer_id;"
            )
        )
    ]

    # --------------------------------------------------
    # 4. COMPLETE ASSESSMENT
    # --------------------------------------------------

    assessment = Assessment(
        assessment_id="test-assessment-001",
        job_title="Python Backend Developer",
        assessment_plan=assessment_plan,
        questions=questions
    )

    # --------------------------------------------------
    # 5. SHARED GRAPH STATE
    # --------------------------------------------------

    state = {
        "jd_text": "Python Backend Developer job description",
        "job_description": job_description,
        "assessment_plan": assessment_plan,
        "assessment": assessment
    }

    return state


# ------------------------------------------------------
# TEST QUALITY REVIEWER
# ------------------------------------------------------

def test_quality_reviewer():

    state = create_test_state()

    result = review_assessment_quality(state)

    quality_review = result["quality_review"]

    print("\nQUALITY REVIEW RESULT")
    print(quality_review.model_dump_json(indent=4))

    assert isinstance(quality_review.is_valid, bool)
    assert isinstance(quality_review.issues, list)
    assert isinstance(quality_review.overall_feedback, str)

    assert result["quality_is_valid"] == quality_review.is_valid
    assert result["quality_review_feedback"] == quality_review.overall_feedback

    print("\nQuality reviewer test executed successfully!")


if __name__ == "__main__":
    test_quality_reviewer()
