from app.agents.question_generator import generate_questions
from app.graph.state import TalentLensState

from app.schemas.job_description import (
    JobDescription,
    Skill,
    SkillCategory,
    ProficiencyLevel
)

from app.schemas.assessment import (
    AssessmentPlan,
    SkillAssessment,
    QuestionType,
    Difficulty
)

job_description = JobDescription(
    job_title="Python Backend Developer",
    experience_min=2,
    experience_max=4,
    responsibilities=[
        "Develop REST APIs",
        "Optimize database queries",
        "Build scalable backend services"
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
        ),
        Skill(
            name="PostgreSQL",
            category=SkillCategory.DATABASE,
            proficiency=ProficiencyLevel.INTERMEDIATE
        )
    ],
    preferred_skills=[
        Skill(
            name="Docker",
            category=SkillCategory.DEVOPS,
            proficiency=ProficiencyLevel.BEGINNER,
            is_required=False
        )
    ],
    education="Bachelor's degree"
)

assessment_plan = AssessmentPlan(
    total_questions=4,
    duration_minutes=30,
    skill_assessments=[
        SkillAssessment(
            skill_name="Python",
            question_types=[
                QuestionType.CODING,
                QuestionType.DEBUGGING
            ],
            difficulty=Difficulty.HARD,
            question_count=2,
            weightage=50
        ),
        SkillAssessment(
            skill_name="FastAPI",
            question_types=[
                QuestionType.SCENARIO
            ],
            difficulty=Difficulty.MEDIUM,
            question_count=1,
            weightage=25
        ),
        SkillAssessment(
            skill_name="PostgreSQL",
            question_types=[
                QuestionType.SQL
            ],
            difficulty=Difficulty.MEDIUM,
            question_count=1,
            weightage=25
        )
    ]
)

state: TalentLensState = {
    "jd_text": "Python Backend Developer with 2-4 years experience.",
    "job_description": job_description,
    "assessment_plan": assessment_plan
}

result = generate_questions(state)

print("\nGENERATED ASSESSMENT:")
print(result["assessment"].model_dump_json(indent=4))