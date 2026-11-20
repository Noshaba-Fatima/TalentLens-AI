
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class QuestionType(str, Enum):
    MCQ = "mcq"
    CODING = "coding"
    DEBUGGING = "debugging"
    SCENARIO = "scenario"
    SYSTEM_DESIGN = "system_design"
    SQL = "sql"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class SkillAssessment(BaseModel):

    skill_name: str

    question_types: list[QuestionType]

    difficulty: Difficulty

    question_count: int = Field(gt=0, le=20)

    weightage: float = Field(gt=0, le=100)


class AssessmentPlan(BaseModel):

    total_questions: int = Field(gt=0)

    duration_minutes: int = Field(gt=0)

    skill_assessments: list[SkillAssessment]

    @model_validator(mode="after")
    def validate_plan(self):

        total_weight = sum(
            item.weightage
            for item in self.skill_assessments
        )

        if abs(total_weight - 100) > 0.01:
            raise ValueError(
                "Total skill weightage must equal 100%"
            )

        actual_questions = sum(
            item.question_count
            for item in self.skill_assessments
        )

        if actual_questions != self.total_questions:
            raise ValueError(
                "Total questions must match "
                "the sum of skill question counts"
            )

        return self

class AssessmentQuestion(BaseModel):
    question_id: str
    skill_name: str
    question_text: str
    question_type: QuestionType
    difficulty: Difficulty
    max_marks: float = Field(gt=0)
    time_limit_minutes: int = Field(gt=0)
    evaluation_rubric: list[str]
    expected_answer: str

class Assessment(BaseModel):

    assessment_id: str

    job_title: str

    assessment_plan: AssessmentPlan

    questions: list[AssessmentQuestion] = Field(min_length=1)

class GeneratedQuestionSet(BaseModel):

    questions: list[AssessmentQuestion] = Field(min_length=1)


class ReviewIssue(BaseModel):
    issue_type: str
    question_id: str | None = None
    description: str
    suggested_fix: str


class AssessmentReview(BaseModel):
    is_valid: bool
    overall_feedback: str
    issues: list[ReviewIssue] = Field(default_factory=list)
    revision_suggestions: list[str] = Field(default_factory=list)
