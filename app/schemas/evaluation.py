from enum import Enum
from pydantic import BaseModel, Field


class HiringRecommendation(str, Enum):
    STRONG_HIRE = "strong_hire"
    HIRE = "hire"
    MAYBE = "maybe"
    NO_HIRE = "no_hire"


class CandidateResponse(BaseModel):
    question_id: str
    skill_name: str
    question_number: int = Field(gt=0)
    candidate_answer: str = ""
    is_answered: bool = False


class RubricCriterionResult(BaseModel):
    criterion: str
    met: bool
    notes: str


class QuestionEvaluation(BaseModel):
    question_id: str
    question_number: int = Field(gt=0)
    skill_name: str
    marks_awarded: float = Field(ge=0)
    max_marks: float = Field(gt=0)
    is_answered: bool
    rubric_breakdown: list[RubricCriterionResult] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    feedback: str


class SkillPerformance(BaseModel):
    skill_name: str
    marks_obtained: float = Field(ge=0)
    max_marks: float = Field(gt=0)
    percentage: float = Field(ge=0, le=100)
    questions_attempted: int = Field(ge=0)
    total_questions: int = Field(gt=0)


class CandidateEvaluationReport(BaseModel):
    assessment_id: str
    job_title: str
    candidate_name: str = "Unknown Candidate"
    candidate_email: str = ""
    total_marks_obtained: float = Field(ge=0)
    total_max_marks: float = Field(gt=0)
    overall_percentage: float = Field(ge=0, le=100)
    recommendation: HiringRecommendation
    executive_summary: str
    key_strengths: list[str] = Field(default_factory=list)
    areas_for_improvement: list[str] = Field(default_factory=list)
    skill_breakdown: list[SkillPerformance]
    question_evaluations: list[QuestionEvaluation]