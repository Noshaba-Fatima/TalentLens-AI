from pathlib import Path
from docx import Document
from docx.shared import Inches

from app.schemas.evaluation import CandidateEvaluationReport


def generate_evaluation_report_docx(
    report: CandidateEvaluationReport,
    output_dir: str = "outputs/evaluation_reports",
) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    title = doc.add_heading("Candidate Evaluation Report", level=0)
    title.alignment = 1

    # Overview
    doc.add_heading("Candidate & Assessment Overview", level=1)
    doc.add_paragraph(f"Candidate Name: {report.candidate_name}")
    if report.candidate_email:
        doc.add_paragraph(f"Candidate Email: {report.candidate_email}")
    doc.add_paragraph(f"Position: {report.job_title}")
    doc.add_paragraph(f"Assessment ID: {report.assessment_id}")
    doc.add_paragraph(
        f"Overall Score: {report.total_marks_obtained} / "
        f"{report.total_max_marks} ({report.overall_percentage}%)"
    )
    doc.add_paragraph(
        f"Recommendation: {report.recommendation.value.replace('_', ' ').title()}"
    )

    # Executive Summary
    doc.add_heading("Executive Summary", level=1)
    doc.add_paragraph(report.executive_summary)

    if report.key_strengths:
        doc.add_heading("Key Strengths", level=2)
        for item in report.key_strengths:
            doc.add_paragraph(item, style="List Bullet")

    if report.areas_for_improvement:
        doc.add_heading("Areas for Improvement", level=2)
        for item in report.areas_for_improvement:
            doc.add_paragraph(item, style="List Bullet")

    # Skill Breakdown Table
    doc.add_heading("Skill-Wise Performance", level=1)
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    headers = ["Skill", "Score", "Percentage", "Attempted"]
    for i, header in enumerate(headers):
        table.rows[0].cells[i].text = header

    for skill in report.skill_breakdown:
        row = table.add_row().cells
        row[0].text = skill.skill_name
        row[1].text = f"{skill.marks_obtained} / {skill.max_marks}"
        row[2].text = f"{skill.percentage}%"
        row[3].text = f"{skill.questions_attempted} / {skill.total_questions}"

    # Question-by-Question Evaluation
    doc.add_heading("Question-Wise Evaluation", level=1)
    for qe in report.question_evaluations:
        doc.add_heading(
            f"Question {qe.question_number} — {qe.skill_name} "
            f"({qe.marks_awarded}/{qe.max_marks})",
            level=2,
        )
        doc.add_paragraph(f"Feedback: {qe.feedback}")
        if qe.rubric_breakdown:
            doc.add_paragraph("Rubric Breakdown:")
            for rb in qe.rubric_breakdown:
                status = "Met" if rb.met else "Not Met"
                doc.add_paragraph(
                    f"[{status}] {rb.criterion} — {rb.notes}",
                    style="List Bullet",
                )

    safe_name = report.candidate_name.strip().replace(" ", "_") or "candidate"
    file_path = output_path / f"{report.assessment_id}_{safe_name}_evaluation_report.docx"
    doc.save(file_path)
    return file_path