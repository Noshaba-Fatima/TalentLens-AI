
from app.agents.assessment_planner import plan_assessment

from app.schemas.job_description import (
    JobDescription,
    Skill,
    SkillCategory,
    ProficiencyLevel
)


sample_jd = JobDescription(

    job_title="Python Backend Developer",

    experience_min=2,
    experience_max=4,

    responsibilities=[
        "Develop REST APIs",
        "Optimize PostgreSQL queries",
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
            proficiency=ProficiencyLevel.INTERMEDIATE,
            is_required=False
        )
    ]
)


state = {
    "jd_text": "Python Backend Developer",
    "job_description": sample_jd
}


result = plan_assessment(state)

plan = result["assessment_plan"]

print(plan.model_dump_json(indent=2))

print("\nTotal questions:", plan.total_questions)

print("\nSkill distribution:")

for skill in plan.skill_assessments:
    print(
        skill.skill_name,
        skill.question_count,
        skill.weightage,
        skill.difficulty.value
    )
