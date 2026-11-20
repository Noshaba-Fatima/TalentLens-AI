
from app.services.llm_service import groq_llm

from app.graph.state import TalentLensState

from app.schemas.assessment import AssessmentPlan


SYSTEM_PROMPT = """
You are an expert technical assessment designer.

Your responsibility is to create an assessment plan
based on the structured job description.

RULES:

1. Assess all important required skills.
2. Give more weight to critical required skills.
3. Preferred skills should receive less weight
   than core required skills.
4. Choose question formats appropriate to each skill.
5. Match difficulty to the expected proficiency
   and experience level.
6. Distribute questions across the competencies.
7. Keep the assessment practical and job-relevant.
8. Total skill weightage MUST equal exactly 100%.
9. Sum of skill question counts MUST equal total_questions.
10. Avoid assessing the same competency redundantly.

Choose reasonable assessment duration and question count.

Return only data matching the supplied schema.
"""


structured_planner = groq_llm.with_structured_output(
    AssessmentPlan
)


def plan_assessment(
    state: TalentLensState
) -> dict:

    job_description = state["job_description"]

    response = structured_planner.invoke(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                "Create an assessment plan for this job description:\n\n"
                + job_description.model_dump_json(indent=2)
            )
        ]
    )

    return {
        "assessment_plan": response
    }
