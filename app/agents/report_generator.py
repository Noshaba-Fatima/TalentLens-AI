from collections import defaultdict
from pydantic import BaseModel, Field

from app.services.llm_service import groq_llm
from app.schemas.assessment import Assessment
from app.schemas.evaluation import (
    CandidateEvaluationReport,
    HiringRecommendation,
    QuestionEvaluation,
    SkillPerformance,
)


class _ExecutiveSummaryOutput(BaseModel):
    executive_summary: str
    key_strengths: list[str] = Field(default_factory=list)
    areas_for_improvement: list[str] = Field(default_factory=list)


SYSTEM_PROMPT = """
You are a technical hiring advisor writing an executive summary
for a recruiter based on a candidate's graded assessment.

RULES:
1. Base your summary strictly on the provided scores and question feedback.
2. Highlight 2-4 concrete technical strengths and 2-4 specific gaps.
3. Keep the tone objective, professional, and concise.
4. Do not invent facts or override the computed scores.
"""

structured_summarizer = groq_llm.with_structured_output(_ExecutiveSummaryOutput)


def _determine_recommendation(percentage: float) -> HiringRecommendation:
    if percentage >= 85.0:
        return HiringRecommendation.STRONG_HIRE
    if percentage >= 70.0:
        return HiringRecommendation.HIRE
    if percentage >= 50.0:
        return HiringRecommendation.MAYBE
    return HiringRecommendation.NO_HIRE


def build_evaluation_report(
    assessment: Assessment,
    question_evaluations: list[QuestionEvaluation],
    candidate_name: str = "Unknown Candidate",
    candidate_email: str = "",
) -> CandidateEvaluationReport:
    # 1. Deterministic total score calculation
    total_obtained = round(
        sum(q.marks_awarded for q in question_evaluations), 2
    )
    total_max = round(
        sum(q.max_marks for q in question_evaluations), 2
    )
    overall_pct = (
        round((total_obtained / total_max) * 100, 2) if total_max > 0 else 0.0
    )
    recommendation = _determine_recommendation(overall_pct)

    # 2. Deterministic skill-wise aggregation
    skill_buckets: dict[str, list[QuestionEvaluation]] = defaultdict(list)
    for qe in question_evaluations:
        skill_buckets[qe.skill_name].append(qe)

    skill_breakdown: list[SkillPerformance] = []
    for skill_name, evals in skill_buckets.items():
        s_obtained = round(sum(e.marks_awarded for e in evals), 2)
        s_max = round(sum(e.max_marks for e in evals), 2)
        s_pct = round((s_obtained / s_max) * 100, 2) if s_max > 0 else 0.0
        attempted = sum(1 for e in evals if e.is_answered)

        skill_breakdown.append(
            SkillPerformance(
                skill_name=skill_name,
                marks_obtained=s_obtained,
                max_marks=s_max,
                percentage=s_pct,
                questions_attempted=attempted,
                total_questions=len(evals),
            )
        )

    # 3. LLM synthesis for executive summary
    summary_context = {
        "job_title": assessment.job_title,
        "overall_percentage": overall_pct,
        "recommendation": recommendation.value,
        "skill_breakdown": [s.model_dump() for s in skill_breakdown],
        "question_feedback": [
            {
                "question_number": q.question_number,
                "skill": q.skill_name,
                "score": f"{q.marks_awarded}/{q.max_marks}",
                "strengths": q.strengths,
                "gaps": q.gaps,
                "feedback": q.feedback,
            }
            for q in question_evaluations
        ],
    }

    summary_output = structured_summarizer.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", f"Generate a recruiter summary from this data:\n\n{summary_context}"),
    ])

    return CandidateEvaluationReport(
        assessment_id=assessment.assessment_id,
        job_title=assessment.job_title,
        candidate_name=candidate_name,
        candidate_email=candidate_email,
        total_marks_obtained=total_obtained,
        total_max_marks=total_max,
        overall_percentage=overall_pct,
        recommendation=recommendation,
        executive_summary=summary_output.executive_summary,
        key_strengths=summary_output.key_strengths,
        areas_for_improvement=summary_output.areas_for_improvement,
        skill_breakdown=skill_breakdown,
        question_evaluations=question_evaluations,
    )