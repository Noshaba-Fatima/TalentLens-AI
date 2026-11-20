from pathlib import Path
from app.schemas.assessment import Assessment
from app.schemas.evaluation import CandidateEvaluationReport

DEFAULT_STORAGE_DIR = Path("outputs/saved_assessments")
DEFAULT_REPORTS_DIR = Path("outputs/evaluation_reports")


def save_assessment(
    assessment: Assessment,
    storage_dir: Path = DEFAULT_STORAGE_DIR
) -> Path:
    storage_dir.mkdir(parents=True, exist_ok=True)
    file_path = storage_dir / f"{assessment.assessment_id}.json"
    file_path.write_text(assessment.model_dump_json(indent=2), encoding="utf-8")
    return file_path


def load_assessment(
    assessment_id: str,
    storage_dir: Path = DEFAULT_STORAGE_DIR
) -> Assessment:
    file_path = storage_dir / f"{assessment_id}.json"
    if not file_path.exists():
        raise FileNotFoundError(f"Saved assessment not found: {assessment_id}")
    return Assessment.model_validate_json(file_path.read_text(encoding="utf-8"))


def list_saved_assessments(
    storage_dir: Path = DEFAULT_STORAGE_DIR
) -> list[Assessment]:
    if not storage_dir.exists():
        return []
    assessments = []
    for file_path in sorted(storage_dir.glob("*.json"), reverse=True):
        assessments.append(
            Assessment.model_validate_json(file_path.read_text(encoding="utf-8"))
        )
    return assessments


def save_evaluation_report(
    report: CandidateEvaluationReport,
    reports_dir: Path = DEFAULT_REPORTS_DIR
) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    safe_name = report.candidate_name.strip().replace(" ", "_") or "candidate"
    file_path = reports_dir / f"{report.assessment_id}_{safe_name}_report.json"
    file_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return file_path