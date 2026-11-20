
from langgraph.graph import StateGraph, START, END

from app.graph.state import TalentLensState

from app.agents.jd_analyser import analyze_job_description
from app.agents.assessment_planner import plan_assessment
from app.agents.question_generator import generate_questions
from app.agents.assessment_validator import validate_assessment
from app.agents.quality_reviewer import review_assessment_quality
from app.agents.review_combiner import combine_reviews


# Maximum number of revisions after the initial generation
MAX_RETRIES = 2


# --------------------------------------------------
# REVISION CONTROL
# --------------------------------------------------

def route_after_review(state: TalentLensState) -> str:
    """
    Decide whether the assessment should be accepted,
    revised, or returned as rejected after retry exhaustion.
    """

    if state["is_valid"]:
        return "end"

    revision_count = state.get("revision_count", 0)

    if revision_count < MAX_RETRIES:
        return "revise"

    return "end"


def prepare_revision(state: TalentLensState) -> dict:
    """
    Increment the revision counter before regenerating
    the assessment.
    """

    current_count = state.get("revision_count", 0)

    return {
        "revision_count": current_count + 1
    }


# --------------------------------------------------
# BUILD LANGGRAPH WORKFLOW
# --------------------------------------------------

builder = StateGraph(TalentLensState)


# Register nodes
builder.add_node("jd_analyzer", analyze_job_description)
builder.add_node("assessment_planner", plan_assessment)
builder.add_node("question_generator", generate_questions)
builder.add_node("deterministic_validator", validate_assessment)
builder.add_node("quality_reviewer", review_assessment_quality)
builder.add_node("review_combiner", combine_reviews)
builder.add_node("prepare_revision", prepare_revision)


# Initial execution flow
builder.add_edge(START, "jd_analyzer")

builder.add_edge("jd_analyzer", "assessment_planner")
builder.add_edge("assessment_planner", "question_generator")

builder.add_edge("question_generator", "deterministic_validator")
builder.add_edge("deterministic_validator", "quality_reviewer")
builder.add_edge("quality_reviewer", "review_combiner")


# Conditional routing after both reviews are combined
builder.add_conditional_edges(
    "review_combiner",
    route_after_review,
    {
        "revise": "prepare_revision",
        "end": END
    }
)


# Revision loop
builder.add_edge("prepare_revision", "question_generator")


# Compile the graph
talentlens_graph = builder.compile()
