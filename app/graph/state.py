
from typing import TypedDict, NotRequired

from app.schemas.job_description import JobDescription
from app.schemas.assessment import AssessmentPlan, Assessment
from app.schemas.assessment import AssessmentReview


class TalentLensState(TypedDict):

    # Original input from HR
    jd_text: str

    # Output of JD Analyzer
    job_description: NotRequired[JobDescription]

    # Output of Assessment Planner
    assessment_plan: NotRequired[AssessmentPlan]

    # Output of Question Generator
    assessment: NotRequired[Assessment]

    # Output of Assessment Validator
    review_result: NotRequired[AssessmentReview]
    is_valid: NotRequired[bool]
    revision_count: NotRequired[int]

    #Output of Quality Reviewer
    quality_review: NotRequired[AssessmentReview]
    quality_review_feedback: NotRequired[str]
    quality_is_valid: NotRequired[bool]

    #Output of Review Combiner
    final_review: NotRequired[AssessmentReview]

    # Candidate evaluation
    candidate_responses: NotRequired[list[dict]]
    evaluation_result: NotRequired[dict]

    # Error tracking
    errors: NotRequired[list[str]]
