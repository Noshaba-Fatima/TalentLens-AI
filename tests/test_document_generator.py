
from pathlib import Path
from docx import Document

from app.schemas.assessment import (
    Assessment,
    AssessmentPlan,
    AssessmentQuestion,
    SkillAssessment,
    QuestionType,
    Difficulty
)

from app.services.assessment_document_generator import (
    generate_candidate_assessment
)


def test_document_generation():

    # Create sample assessment plan
    plan = AssessmentPlan(
        total_questions=1,
        duration_minutes=30,
        skill_assessments=[
            SkillAssessment(
                skill_name="Python",
                question_types=[QuestionType.CODING],
                difficulty=Difficulty.MEDIUM,
                question_count=1,
                weightage=100
            )
        ]
    )

    # Create sample question
    question = AssessmentQuestion(
        question_id="q1",
        skill_name="Python",
        question_text="Write a Python function to reverse a string.",
        question_type=QuestionType.CODING,
        difficulty=Difficulty.MEDIUM,
        max_marks=10,
        time_limit_minutes=30,
        evaluation_rubric=[
            "Correct implementation",
            "Efficient solution"
        ],
        expected_answer="Use string slicing: text[::-1]"
    )

    # Create complete assessment
    assessment = Assessment(
        assessment_id="test-assessment-001",
        job_title="Python Developer",
        assessment_plan=plan,
        questions=[question]
    )

    # Generate document
    file_path = generate_candidate_assessment(
        assessment,
        output_dir="outputs/test_assessments"
    )

    # Verify document exists
    assert file_path.exists()

    # Verify file extension
    assert file_path.suffix == ".docx"

    print("\nDocument generated successfully!")
    print("File location:", file_path.resolve())
    
    generated_doc = Document(file_path)

    document_text = "\n".join(
        paragraph.text
        for paragraph in generated_doc.paragraphs
    )

    assert "Use string slicing: text[::-1]" not in document_text
    assert "Correct implementation" not in document_text

    print("Confidential information check passed!")

if __name__ == "__main__":
    test_document_generation()



