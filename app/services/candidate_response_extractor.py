import re
from pathlib import Path

from docx import Document

from app.schemas.assessment import Assessment


def extract_candidate_responses(
    file_path: str,
    assessment: Assessment
) -> list[dict]:

    document_path = Path(file_path)

    if not document_path.exists():
        raise FileNotFoundError(
            f"Candidate document not found: {file_path}"
        )

    if document_path.suffix.lower() != ".docx":
        raise ValueError("Only DOCX files are supported.")

    document = Document(str(document_path))

    answers = {}
    current_question = None
    collecting_answer = False

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        # Detect question heading
        match = re.fullmatch(
            r"Question\s+(\d+)",
            text,
            re.IGNORECASE
        )

        if match:
            current_question = int(match.group(1))
            collecting_answer = False

            answers.setdefault(current_question, [])
            continue

        # Detect answer section
        if text.lower() == "your answer:":
            collecting_answer = True
            continue

        # Extract candidate's response
        if collecting_answer and current_question is not None:

            # Ignore blank lines and underscore placeholders
            if text and not re.fullmatch(r"_+", text):
                answers[current_question].append(text)

    # Map answers to original assessment questions
    candidate_responses = []

    for index, question in enumerate(
        assessment.questions,
        start=1
    ):

        answer_text = "\n".join(
            answers.get(index, [])
        ).strip()

        candidate_responses.append({
            "question_id": question.question_id,
            "skill_name": question.skill_name,
            "question_number": index,
            "candidate_answer": answer_text,
            "is_answered": bool(answer_text)
        })

    return candidate_responses