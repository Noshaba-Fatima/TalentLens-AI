from typing import TypedDict, NotRequired
from langgraph.graph import StateGraph, START, END

from app.schemas.assessment import Assessment
from app.schemas.evaluation import (
    CandidateEvaluationReport,
    QuestionEvaluation,
)
from app.services.candidate_response_extractor import extract_candidate_responses
from app.agents.answer_evaluator import evaluate_single_answer
from app.agents.report_generator import build_evaluation_report


class EvaluationState(TypedDict):
    assessment: Assessment
    submission_file_path: str
    candidate_name: NotRequired[str]
    candidate_email: NotRequired[str]
    extracted_responses: NotRequired[list[dict]]
    question_evaluations: NotRequired[list[QuestionEvaluation]]
    evaluation_report: NotRequired[CandidateEvaluationReport]


def extract_responses_node(state: EvaluationState) -> dict:
    responses = extract_candidate_responses(
        file_path=state["submission_file_path"],
        assessment=state["assessment"],
    )
    return {"extracted_responses": responses}


def evaluate_answers_node(state: EvaluationState) -> dict:
    assessment = state["assessment"]
    responses = state["extracted_responses"]

    question_map = {q.question_id: q for q in assessment.questions}
    evaluations: list[QuestionEvaluation] = []

    for resp in responses:
        question = question_map[resp["question_id"]]
        qe = evaluate_single_answer(
            question=question,
            question_number=resp["question_number"],
            candidate_answer=resp["candidate_answer"],
            is_answered=resp["is_answered"],
        )
        evaluations.append(qe)

    return {"question_evaluations": evaluations}


def generate_report_node(state: EvaluationState) -> dict:
    report = build_evaluation_report(
        assessment=state["assessment"],
        question_evaluations=state["question_evaluations"],
        candidate_name=state.get("candidate_name", "Unknown Candidate"),
        candidate_email=state.get("candidate_email", ""),
    )
    return {"evaluation_report": report}


eval_builder = StateGraph(EvaluationState)

eval_builder.add_node("extract_responses", extract_responses_node)
eval_builder.add_node("evaluate_answers", evaluate_answers_node)
eval_builder.add_node("generate_report", generate_report_node)

eval_builder.add_edge(START, "extract_responses")
eval_builder.add_edge("extract_responses", "evaluate_answers")
eval_builder.add_edge("evaluate_answers", "generate_report")
eval_builder.add_edge("generate_report", END)

evaluation_graph = eval_builder.compile()