
from app.schemas.job_description import (
    JobDescription,
    Skill,
    SkillCategory,
    ProficiencyLevel
)
from app.schemas.assessment import (
    AssessmentPlan,
    SkillAssessment,
    AssessmentQuestion,
    Assessment,
    QuestionType,
    Difficulty
)
from app.schemas.assessment import (
    ReviewIssue,
    AssessmentReview
)

jd = JobDescription(
    job_title="Python Backend Developer",

    experience_min=2,
    experience_max=4,

    responsibilities=[
        "Develop REST APIs",
        "Optimize database queries"
    ],

    required_skills=[
        Skill(
            name="Python",
            category=SkillCategory.PROGRAMMING,
            proficiency=ProficiencyLevel.ADVANCED
        ),
        Skill(
            name="FastAPI",
            category=SkillCategory.FRAMEWORK,
            proficiency=ProficiencyLevel.INTERMEDIATE
        )
    ],

    preferred_skills=[],

    education="Bachelor's degree"
)

print(jd.model_dump_json(indent=4))

question = AssessmentQuestion(
    question_id="Q001",
    skill_name="Python",
    question_text="Explain the difference between lists and tuples.",
    question_type=QuestionType.SCENARIO,
    difficulty=Difficulty.MEDIUM,
    max_marks=10,
    time_limit_minutes=5,
    evaluation_rubric=[
        "Explains mutability",
        "Explains performance differences",
        "Provides appropriate examples"
    ],
    expected_answer="Lists are mutable, whereas tuples are immutable."
)

print("\nASSESSMENT QUESTION:")
print(question.model_dump_json(indent=4))

plan = AssessmentPlan(
    total_questions=1,
    duration_minutes=5,
    skill_assessments=[
        SkillAssessment(
            skill_name="Python",
            question_types=[QuestionType.SCENARIO],
            difficulty=Difficulty.MEDIUM,
            question_count=1,
            weightage=100
        )
    ]
)

assessment = Assessment(
    assessment_id="ASSESS-001",
    job_title="Python Backend Developer",
    assessment_plan=plan,
    questions=[question]
)

print("\nCOMPLETE ASSESSMENT:")
print(assessment.model_dump_json(indent=4))

def test_assessment_review_schema():

    review = AssessmentReview(
        is_valid=False,
        overall_feedback="Assessment requires revision.",
        issues=[
            ReviewIssue(
                issue_type="technical_accuracy",
                question_id="question-123",
                description="Authentication is not properly implemented.",
                suggested_fix="Use Depends(get_current_user)."
            )
        ],
        revision_suggestions=[
            "Correct the FastAPI reference implementation."
        ]
    )

    print("\nAssessment Review:")
    print(review.model_dump_json(indent=4))

    assert review.is_valid is False
    assert len(review.issues) == 1
    assert review.issues[0].issue_type == "technical_accuracy"
    assert len(review.revision_suggestions) == 1

    print("\nAssessment Review schema passed!")

if __name__ == "__main__":
    # Keep your existing test calls here
    test_assessment_review_schema()