TalentLens AIAgentic AI-Powered Technical Assessment & Candidate Evaluation PlatformTalentLens AI is an end-to-end recruitment assessment system built with LangGraph, Pydantic, Groq, Google Gemini, and Streamlit. It automates the full technical assessment lifecycle—from analyzing a job description and generating a quality-audited assessment to extracting candidate responses, grading them against structured rubrics, and producing recruiter-ready evaluation reports.By pairing LLM reasoning with deterministic Python validation and scoring, TalentLens AI ensures structured outputs, bounded revision loops, strict candidate confidentiality, and reliable score arithmetic.Problem StatementDesigning and grading technical assessments is manual, inconsistent, and time-intensive. Hiring teams must translate job descriptions into balanced skill blueprints, author role-specific questions with measurable rubrics, audit them for technical accuracy, strip internal grading criteria before sending them to candidates, and then evaluate submissions consistently.TalentLens AI solves this by orchestrating two specialized multi-agent workflows—one for Assessment Generation and one for Candidate Evaluation—backed by persistent assessment storage and a clean recruiter dashboard.Key FeaturesAssessment Generation PipelineAutomated Job Description Analysis: Extracts job title, experience bounds, responsibilities, required vs. preferred skills, proficiency levels, and education into validated Pydantic models.Intelligent Assessment Planning: Allocates skill weightages (strictly totaling 100%), question counts, difficulty levels, question formats, and total duration.Role-Specific Question Generation: Creates technical questions (mcq, coding, debugging, scenario, system_design, sql) with expected answers, marks, time limits, and measurable evaluation rubrics.Hybrid Two-Stage Review: Combines programmatic Deterministic Validation (counts, skill distribution, difficulty, question types, marks, time budgets, duplicate IDs) with LLM Quality Auditing (technical accuracy, clarity, job relevance, rubric alignment).Bounded Revision Loop: Automatically routes rejected assessments back to the generator with consolidated issue-level feedback, capped by a configurable retry limit (MAX_RETRIES = 2).Confidential Candidate DOCX Export: Generates a formatted candidate-facing .docx assessment that strictly excludes expected answers and evaluation rubrics.Candidate Evaluation PipelinePersistent Assessment Storage: Saves full assessments (including rubrics and expected answers) by assessment_id so submitted documents can be graded reliably later.Automated Response Extraction: Parses candidate answers from submitted .docx files and maps them back to the original question IDs.Rubric-Based Grading with Prompt-Injection Guardrails: Evaluates answered questions against the expected answer and rubric while treating candidate text as untrusted data. Automatically assigns zero marks to blank responses without wasting LLM calls and clamps awarded marks to [0, max_marks] in Python.Deterministic Scoring & Skill Aggregation: Computes total marks, overall percentage, hiring recommendation tier (Strong Hire, Hire, Maybe, No Hire), and skill-wise breakdowns deterministically in Python.Recruiter Evaluation Reports: Synthesizes an executive summary, key strengths, and improvement areas, and exports a downloadable .docx evaluation report.Recruiter DashboardStreamlit Console: Clean 3-tab interface (Generate Assessment, Evaluate Candidate, Assessment History) with KPI cards, skill progress bars, rubric badges, and one-click .docx downloads.System Architecture1. Assessment Generation Workflow (app/graph/workflow.py)Agent / ComponentResponsibilityEngineJD AnalyzerExtracts structured job requirements, skills, and experience rangeGroqAssessment PlannerBuilds a validated blueprint (100% weightage, question counts, duration)GroqQuestion GeneratorAuthors or revises questions, expected answers, and evaluation rubricsGeminiDeterministic ValidatorEnforces structural, numerical, and constraint checks programmaticallyPythonQuality ReviewerAudits technical accuracy, clarity, relevance, and rubric alignmentGeminiReview CombinerMerges deterministic and AI reviews into actionable revision feedbackPythonRevision ControllerConditionally routes failed assessments for bounded revisionLangGraph2. Candidate Evaluation Workflow (app/graph/evaluation_workflow.py)Stage / ComponentResponsibilityEngineResponse ExtractorExtracts answers from submitted .docx files and maps them to question IDsPython (python-docx)Answer EvaluatorGrades responses per rubric criterion; skips blank answers; clamps marksGemini + PythonReport GeneratorCalculates exact totals, skill percentages, and recommendation; drafts summaryPython + GroqReport ExporterGenerates a formatted recruiter-facing .docx evaluation reportPython (python-docx)Technology StackAgent Orchestration: LangGraph, LangChainLLM Providers: Groq API (langchain-groq), Google Gemini API (langchain-google-genai)Data Validation & Config: Pydantic, Pydantic Settings, Python TypedDictDocument Processing: python-docxInterface: StreamlitTesting: pytestProject StructureTalentLens-AI/
├── .streamlit/
│   └── config.toml
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
│   ├── config/
│   │   └── settings.py
│   ├── graph/
│   │   ├── state.py
│   │   ├── workflow.py
│   │   └── evaluation_workflow.py
│   ├── schemas/
│   │   ├── job_description.py
│   │   ├── assessment.py
│   │   └── evaluation.py
│   └── services/
│       ├── llm_service.py
│       ├── storage_service.py
│       ├── assessment_document_generator.py
│       ├── candidate_response_extractor.py
│       └── evaluation_report_generator.py
├── outputs/
│   ├── assessments/
│   ├── saved_assessments/
│   ├── evaluation_reports/
│   └── test_assessments/
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
├── main.py
├── streamlit_app.py
├── talentlens_workflow.png
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
Installation & SetupPrerequisitesPython 3.11+Groq API keyGoogle AI (Gemini) API key1. Clone the Repositorygit clone https://github.com/Noshaba-Fatima/TalentLens-AI.git
cd TalentLens-AI
2. Create & Activate a Virtual EnvironmentWindows (PowerShell):python -m venv venv
.\venv\Scripts\activate
macOS / Linux:python -m venv venv
source venv/bin/activate
3. Install Dependenciespip install -r requirements.txt
4. Configure Environment VariablesCopy .env.example to .env and add your API keys:GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
GEMINI_MODEL=gemini-2.5-flash
TEMPERATURE=0.2
MAX_TOKENS=4096
Security Note: Never commit your .env file or expose API keys publicly.5. Launch the Applicationpython main.py
This launches the Streamlit recruiter dashboard at http://localhost:8501.TestingOffline Deterministic Unit Tests (No API Calls)Run schema, validator, review combiner, routing, and document confidentiality tests without consuming LLM tokens:python -m pytest tests/test_schemas.py tests/test_state.py tests/test_assessment_validator.py tests/test_review_combiner.py tests/test_workflow_routing.py tests/test_document_generator.py
Live Agent & Workflow Integration Tests (Uses Groq / Gemini APIs)python -m tests.test_jd_analyser
python -m tests.test_assessment_planner
python -m tests.test_question_generator
python -m tests.test_quality_reviewer
python -m tests.test_workflow
Regenerate Workflow Diagrampython -m tests.visualize_workflow
Design PhilosophyHybrid Intelligence: LLMs handle semantic extraction, question authoring, and rubric reasoning; Python handles structural validation, mark clamping, and score arithmetic.Strict Data Contracts: Every agent boundary is enforced with Pydantic schemas.Controlled Autonomy: Conditional edges and bounded retries prevent runaway agent loops.Prompt-Injection Defense: Job descriptions, generated content, and candidate answers are explicitly treated as untrusted data.Confidentiality by Design: Candidate .docx files are strictly separated from expected answers and internal grading rubrics.Human-in-the-Loop Hiring: AI supports recruiters with structured evidence and reports rather than making autonomous hiring decisions.Roadmap[ ] LangSmith Observability & Tracing: End-to-end execution traces, latency monitoring, and token cost tracking across both LangGraph workflows.[ ] Database Persistence: Migrate JSON file storage to SQLite / PostgreSQL for multi-user assessment and candidate history.[ ] Automated Evaluation Benchmarks: Add golden test datasets to measure grading consistency and rubric alignment.[ ] Candidate Submission Portal: Allow candidates to complete assessments directly in-browser alongside .docx uploads.DisclaimerTalentLens AI is an experimental AI-powered recruitment assistance platform built for educational and engineering purposes. AI-generated assessments and candidate evaluations may contain inaccuracies or biases. Recruiters should review all generated assessments and reports before making hiring decisions.AuthorNoshaba FatimaData Science | AI & Machine Learning | Agentic AIGitHub: Noshaba-Fatima
