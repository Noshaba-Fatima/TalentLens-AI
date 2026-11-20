# TalentLens AI

**Agentic AI-Powered Technical Assessment & Candidate Evaluation Platform**

TalentLens AI is an end-to-end recruitment assessment system built with **LangGraph**, **Pydantic**, **Groq**, **Google Gemini**, and **Streamlit**. It automates the complete technical hiring assessment lifecycle—from transforming raw job descriptions into quality-reviewed candidate assessments (`.docx`) to extracting submitted answers, grading them against structured rubrics, and generating recruiter-ready evaluation reports.

---

## Problem Statement

Designing and grading technical assessments manually is slow, repetitive, and inconsistent. Hiring teams must analyze job descriptions, balance skill weights and difficulty, author clear questions with measurable rubrics, audit assessment quality, and grade candidate submissions objectively.

TalentLens AI solves this by combining **LLM-powered specialized agents** with **deterministic Python validation and scoring** inside two orchestrated LangGraph workflows.

---

## Key Features

### Assessment Generation Pipeline
- **Automated Job Description Analysis:** Extracts job title, experience bounds, responsibilities, required/preferred skills, and education into validated Pydantic schemas.
- **Intelligent Assessment Planning:** Allocates skill weightages (enforcing an exact 100% sum), question counts, difficulty levels, question types, and total duration.
- **Role-Specific Question Generation:** Generates technical questions with expected answers, marks, time limits, and measurable evaluation rubrics.
- **Hybrid Review & Bounded Revision Loop:** Combines deterministic Python structural checks (`assessment_validator.py`) with LLM quality auditing (`quality_reviewer.py`) and routes rejected assessments back for revision up to a configurable retry limit (`MAX_RETRIES = 2`).
- **Confidential Candidate Document Export:** Generates a clean, downloadable `.docx` assessment for candidates while strictly excluding expected answers and internal rubrics.

### Candidate Evaluation Pipeline
- **Assessment Persistence:** Stores full assessments (including rubrics and expected answers) by `assessment_id` so submitted candidate documents can be graded reliably.
- **Automated Response Extraction:** Parses candidate answers from completed `.docx` submissions and maps them to original question IDs.
- **Hybrid Rubric Grading:** Skips LLM calls deterministically for blank answers, grades attempted responses against expected answers and rubrics via Gemini, and clamps awarded marks in Python to `[0, max_marks]`.
- **Deterministic Score Aggregation:** Computes exact totals, overall percentages, skill-wise breakdowns, and hiring recommendation tiers (`Strong Hire`, `Hire`, `Maybe`, `No Hire`) in Python—never relying on an LLM for arithmetic.
- **Recruiter Evaluation Reports:** Synthesizes an executive summary, key strengths, and improvement areas via Groq, and exports a formatted `.docx` evaluation report.

### Interactive Recruiter Dashboard
- **Streamlit Console:** Clean 3-tab interface (**Generate Assessment**, **Evaluate Candidate**, **Assessment History**) with KPI cards, skill progress bars, rubric badges, and one-click `.docx` downloads.

---

## System Architecture

![TalentLens Workflow](talentlens_workflow.png)

### 1. Assessment Generation Workflow (`app/graph/workflow.py`)

| Agent / Component | Responsibility | Technology |
| :--- | :--- | :--- |
| **JD Analyzer** | Extracts structured job requirements and skills from raw JD text | Groq + Pydantic |
| **Assessment Planner** | Builds a balanced blueprint (weightages, counts, difficulty, duration) | Groq + Pydantic |
| **Question Generator** | Generates or revises questions, expected answers, and rubrics | Gemini + Pydantic |
| **Deterministic Validator** | Enforces question counts, skill distribution, difficulty, types, time limits, and unique IDs | Python |
| **Quality Reviewer** | Audits technical accuracy, clarity, relevance, rubric quality, and duplication | Gemini + Pydantic |
| **Review Combiner** | Merges deterministic and AI reviews into actionable revision feedback | Python |
| **Revision Controller** | Conditionally routes failed assessments for revision with bounded retries | LangGraph |

### 2. Candidate Evaluation Workflow (`app/graph/evaluation_workflow.py`)

| Agent / Component | Responsibility | Technology |
| :--- | :--- | :--- |
| **Response Extractor** | Extracts and maps candidate answers from submitted `.docx` files | Python (`python-docx`) |
| **Answer Evaluator** | Grades each answer against its rubric with prompt-injection guards and Python mark clamping | Gemini + Python |
| **Report Generator** | Computes exact scores/skill percentages in Python and synthesizes an executive summary | Python + Groq |
| **Report Exporter** | Exports the structured `CandidateEvaluationReport` to a recruiter-facing `.docx` | Python (`python-docx`) |

---

## Technology Stack

- **Agent Orchestration:** LangGraph, LangChain
- **LLM Providers:** Groq API, Google Gemini API (`langchain-groq`, `langchain-google-genai`)
- **Data Validation & Config:** Python 3.11+, Pydantic, Pydantic Settings, `python-dotenv`
- **Document Processing:** `python-docx`
- **Frontend:** Streamlit
- **Testing:** `pytest`

---

## Project Structure

```text
TalentLens-AI/
│
├── .streamlit/
│   └── config.toml
│
├── app/
│   ├── agents/
│   │   ├── jd_analyser.py
│   │   ├── assessment_planner.py
│   │   ├── question_generator.py
│   │   ├── assessment_validator.py
│   │   ├── quality_reviewer.py
│   │   ├── review_combiner.py
│   │   ├── answer_evaluator.py
│   │   └── report_generator.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   ├── workflow.py
│   │   └── evaluation_workflow.py
│   │
│   ├── schemas/
│   │   ├── job_description.py
│   │   ├── assessment.py
│   │   └── evaluation.py
│   │
│   └── services/
│       ├── llm_service.py
│       ├── storage_service.py
│       ├── assessment_document_generator.py
│       ├── candidate_response_extractor.py
│       └── evaluation_report_generator.py
│
├── tests/
│   ├── test_schemas.py
│   ├── test_state.py
│   ├── test_llm.py
│   ├── test_jd_analyser.py
│   ├── test_assessment_planner.py
│   ├── test_question_generator.py
│   ├── test_assessment_validator.py
│   ├── test_quality_reviewer.py
│   ├── test_review_combiner.py
│   ├── test_workflow.py
│   ├── test_workflow_routing.py
│   ├── test_document_generator.py
│   └── visualize_workflow.py
│
├── outputs/
│   ├── assessments/
│   ├── saved_assessments/
│   └── evaluation_reports/
│
├── main.py
├── streamlit_app.py
├── talentlens_workflow.png
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
