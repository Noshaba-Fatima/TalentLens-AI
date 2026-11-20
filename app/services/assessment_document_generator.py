
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt

from app.schemas.assessment import Assessment


def generate_candidate_assessment(
    assessment: Assessment,
    output_dir: str = "outputs/assessments"
) -> Path:

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Initialize Word document
    document = Document()

    # Configure page margins
    section = document.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    # Document title
    title = document.add_heading(
        "Technical Assessment",
        level=0
    )
    title.alignment = 1

    # Assessment information
    document.add_heading("Assessment Information", level=1)

    document.add_paragraph(
        f"Position: {assessment.job_title}"
    )

    document.add_paragraph(
        f"Total Questions: {len(assessment.questions)}"
    )

    document.add_paragraph(
        f"Duration: "
        f"{assessment.assessment_plan.duration_minutes} minutes"
    )

    total_marks = sum(
        question.max_marks
        for question in assessment.questions
    )

    document.add_paragraph(
        f"Total Marks: {total_marks}"
    )

    # Candidate details
    document.add_heading("Candidate Details", level=1)

    document.add_paragraph("Candidate Name: __________________________")
    document.add_paragraph("Email: ____________________________________")
    document.add_paragraph("Date: _____________________________________")

    # Instructions
    document.add_heading("Instructions", level=1)

    instructions = [
        "Read each question carefully before answering.",
        "Attempt all questions.",
        "Manage your time according to the allocated duration.",
        "For coding questions, provide clear and readable code.",
        "Submit your completed assessment document."
    ]

    for instruction in instructions:
        document.add_paragraph(
            instruction,
            style="List Bullet"
        )

    # Assessment questions
    document.add_heading("Assessment Questions", level=1)

    for index, question in enumerate(
        assessment.questions,
        start=1
    ):

        document.add_heading(
            f"Question {index}",
            level=2
        )

        document.add_paragraph(
            f"Skill: {question.skill_name}"
        )

        document.add_paragraph(
            f"Type: {question.question_type.value}"
        )

        document.add_paragraph(
            f"Difficulty: {question.difficulty.value}"
        )

        document.add_paragraph(
            f"Maximum Marks: {question.max_marks}"
        )

        document.add_paragraph(
            f"Time Limit: {question.time_limit_minutes} minutes"
        )

        # Actual question
        document.add_paragraph(
            question.question_text
        )

        # Blank space for candidate response
        document.add_heading(
            "Your Answer:",
            level=3
        )

        for _ in range(5):
            paragraph = document.add_paragraph(
                "_" * 85
            )
            paragraph.paragraph_format.space_after = Pt(10)

        document.add_paragraph("")

    # Save document
    file_path = (
        output_path /
        f"{assessment.assessment_id}_candidate_assessment.docx"
    )

    document.save(file_path)

    return file_path
