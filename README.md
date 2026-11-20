# TalentLens AI

**Agentic AI-Powered Technical Assessment & Candidate Evaluation Platform**

TalentLens AI automates the end-to-end technical hiring assessment lifecycle using **LangGraph**, **Pydantic**, **Groq**, **Google Gemini**, and **Streamlit**. It pairs LLM agents with deterministic Python validation and scoring to generate quality-reviewed assessments and objectively evaluate candidate submissions.

---

## Key Features

- **JD-to-Assessment Pipeline:** Extracts structured job requirements, plans balanced skill weightages (enforcing 100% total), and generates role-specific questions with expected answers and rubrics.
- **Hybrid Quality Assurance:** Combines deterministic Python checks (question counts, skill distribution, difficulty, types, time limits, unique IDs) with an LLM quality audit inside a bounded LangGraph revision loop (`MAX_RETRIES = 2`).
- **Confidential Candidate Export:** Generates downloadable `.docx` assessments for candidates while stripping out expected answers and rubrics.
- **Automated Candidate Evaluation:** Extracts submitted `.docx` answers, grades attempted responses against rubrics (with Python mark clamping), computes exact skill-wise scores and hiring recommendations (`Strong Hire`, `Hire`, `Maybe`, `No Hire`) deterministically, and exports a recruiter `.docx` report.
- **Recruiter Dashboard:** 3-tab Streamlit workspace (**Generate Assessment**, **Evaluate Candidate**, **Assessment History**) backed by local JSON persistence.

---

## Architecture

![TalentLens Workflow](talentlens_workflow.png)

1. **Assessment Generation (`app/graph/workflow.py`)**  
   `JD Analyzer (Groq)` → `Assessment Planner (Groq)` → `Question Generator (Gemini)` → `Deterministic Validator (Python)` → `Quality Reviewer (Gemini)` → `Review Combiner (Python)` → `Bounded Revision Loop (LangGraph)`
2. **Candidate Evaluation (`app/graph/evaluation_workflow.py`)**  
   `Response Extractor (python-docx)` → `Answer Evaluator (Gemini + Python)` → `Report Generator (Python + Groq)` → `DOCX Report Export`

---

## Tech Stack

- **Orchestration & LLMs:** LangGraph, LangChain, Groq API, Google Gemini API
- **Validation & Processing:** Python 3.11+, Pydantic, `python-docx`
- **UI & Testing:** Streamlit, `pytest`

---

## Quick Start

```bash
# 1. Clone and enter the repository
git clone [https://github.com/Noshaba-Fatima/TalentLens-AI.git](https://github.com/Noshaba-Fatima/TalentLens-AI.git)
cd TalentLens-AI

# 2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
# Copy .env.example to .env and add your GROQ_API_KEY and GOOGLE_API_KEY

# 5. Launch the Streamlit dashboard
python main.py
