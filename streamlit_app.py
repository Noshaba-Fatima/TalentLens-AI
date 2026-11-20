import html
import tempfile
from pathlib import Path
import streamlit as st

from app.graph.workflow import talentlens_graph
from app.graph.evaluation_workflow import evaluation_graph
from app.services.assessment_document_generator import generate_candidate_assessment
from app.services.evaluation_report_generator import generate_evaluation_report_docx
from app.services.storage_service import (
    save_assessment,
    list_saved_assessments,
    save_evaluation_report,
)

st.set_page_config(
    page_title="TalentLens AI",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# CUSTOM STYLING (MINIMALIST SAAS THEME)
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Clean layout spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    /* Hide default Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Brand header */
    .brand-bar {
        display: flex;
        align-items: center;
        gap: 14px;
        padding-bottom: 1.25rem;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    .brand-mark {
        width: 42px;
        height: 42px;
        border-radius: 10px;
        background: linear-gradient(135deg, #0F172A 0%, #334155 100%);
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 16px;
        letter-spacing: 0.04em;
        flex-shrink: 0;
    }
    .brand-title {
        font-size: 1.55rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }
    .brand-subtitle {
        font-size: 0.9rem;
        color: #64748B;
        margin: 2px 0 0 0;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 4px;
        font-weight: 500;
        font-size: 0.95rem;
        color: #64748B;
    }
    .stTabs [aria-selected="true"] {
        color: #0F172A !important;
        font-weight: 600;
    }

    /* Buttons */
    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"] {
        background-color: #0F172A;
        color: #FFFFFF;
        border: 1px solid #0F172A;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.55rem 1.15rem;
        transition: all 0.15s ease;
    }
    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button[kind="primary"]:hover {
        background-color: #1E293B;
        border-color: #1E293B;
    }

    /* Metric cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.25;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .badge-strong-hire { background: #DCFCE7; color: #166534; }
    .badge-hire        { background: #DBEAFE; color: #1E40AF; }
    .badge-maybe       { background: #FEF3C7; color: #92400E; }
    .badge-no-hire     { background: #FEE2E2; color: #991B1B; }
    .badge-met         { background: #DCFCE7; color: #166534; }
    .badge-unmet       { background: #FEE2E2; color: #991B1B; }
    .badge-tag         { background: #F1F5F9; color: #334155; margin-right: 6px; }

    /* Section labels */
    .section-heading {
        font-size: 1.05rem;
        font-weight: 600;
        color: #0F172A;
        margin: 1rem 0 0.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_kpi_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{html.escape(label)}</div>
            <div class="kpi-value">{html.escape(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendation_badge(rec_value: str) -> str:
    css_map = {
        "strong_hire": "badge-strong-hire",
        "hire": "badge-hire",
        "maybe": "badge-maybe",
        "no_hire": "badge-no-hire",
    }
    label = rec_value.replace("_", " ").upper()
    css_class = css_map.get(rec_value, "badge-tag")
    return f'<span class="badge {css_class}">{html.escape(label)}</span>'


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
saved_all = list_saved_assessments()

with st.sidebar:
    st.markdown("### Workspace")
    st.caption("Multi-agent technical assessment & candidate grading console.")
    st.divider()

    st.metric("Saved Assessments", len(saved_all))

    st.divider()
    st.markdown("**Active Pipeline**")
    st.markdown(
        """
        1. JD Analysis (Groq)  
        2. Assessment Planning (Groq)  
        3. Question Generation (Gemini)  
        4. Deterministic Validation (Python)  
        5. Quality Audit & Revision (Gemini)  
        6. Rubric Evaluation & Reporting
        """
    )

# --------------------------------------------------
# HEADER
# --------------------------------------------------
-st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F1F5F9;
        border-right: 1px solid #E2E8F0;
    }

    /* Brand header */
    .brand-bar {
        display: flex;
        align-items: center;
        gap: 14px;
        padding-bottom: 1.25rem;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    .brand-mark {
        width: 42px;
        height: 42px;
        border-radius: 10px;
        background: linear-gradient(135deg, #4F46E5 0%, #3730A3 100%);
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 16px;
        letter-spacing: 0.04em;
        flex-shrink: 0;
    }
    .brand-title {
        font-size: 1.55rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }
    .brand-subtitle {
        font-size: 0.9rem;
        color: #475569;
        margin: 2px 0 0 0;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 4px;
        font-weight: 500;
        font-size: 0.95rem;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        color: #4F46E5 !important;
        font-weight: 600;
    }

    /* Primary Buttons */
    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"] {
        background-color: #4F46E5;
        color: #FFFFFF !important;
        border: 1px solid #4F46E5;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.55rem 1.15rem;
        transition: all 0.15s ease;
    }
    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button[kind="primary"]:hover {
        background-color: #4338CA;
        border-color: #4338CA;
        color: #FFFFFF !important;
    }

    /* KPI Metric Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.25;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .badge-strong-hire { background: #DCFCE7; color: #166534; }
    .badge-hire        { background: #E0E7FF; color: #3730A3; }
    .badge-maybe       { background: #FEF3C7; color: #92400E; }
    .badge-no-hire     { background: #FEE2E2; color: #991B1B; }
    .badge-met         { background: #DCFCE7; color: #166534; }
    .badge-unmet       { background: #FEE2E2; color: #991B1B; }
    .badge-tag         { background: #EEF2FF; color: #3730A3; margin-right: 6px; }

    /* Section headings */
    .section-heading {
        font-size: 1.05rem;
        font-weight: 600;
        color: #0F172A;
        margin: 0.5rem 0 0.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

tab_generate, tab_evaluate, tab_history = st.tabs(
    ["Generate Assessment", "Evaluate Candidate", "Assessment History"]
)

# --------------------------------------------------
# TAB 1: GENERATE ASSESSMENT
# --------------------------------------------------
with tab_generate:
    with st.container(border=True):
        st.markdown('<div class="section-heading">Job Description Input</div>', unsafe_allow_html=True)
        st.caption("Paste a complete job description to generate a validated, role-specific technical assessment.")

        jd_text = st.text_area(
            "Job Description",
            label_visibility="collapsed",
            height=230,
            placeholder="Paste role title, experience range, required/preferred skills, and key responsibilities...",
        )

        col_btn, _ = st.columns([1, 3])
        with col_btn:
            generate_clicked = st.button(
                "Generate Assessment",
                type="primary",
                use_container_width=True,
            )

    if generate_clicked:
        if not jd_text.strip():
            st.warning("Please paste a job description before generating.")
        else:
            with st.spinner("Running multi-agent pipeline (Analyze, Plan, Generate, Validate, Review)..."):
                try:
                    result = talentlens_graph.invoke({"jd_text": jd_text})
                    assessment = result["assessment"]
                    is_valid = result.get("is_valid", False)
                    revisions = result.get("revision_count", 0)
                    final_review = result.get("final_review")

                    save_assessment(assessment)
                    docx_path = generate_candidate_assessment(assessment)

                    st.session_state["last_assessment"] = assessment
                    st.session_state["last_docx_path"] = docx_path
                    st.session_state["last_valid"] = is_valid
                    st.session_state["last_revisions"] = revisions
                    st.session_state["last_review"] = final_review
                except Exception as e:
                    st.error(f"Pipeline execution failed: {e}")

    if "last_assessment" in st.session_state:
        assessment = st.session_state["last_assessment"]
        docx_path = Path(st.session_state["last_docx_path"])
        is_valid = st.session_state["last_valid"]
        revisions = st.session_state["last_revisions"]

        st.markdown("")
        if is_valid:
            st.success(
                f"Assessment approved — ID: {assessment.assessment_id[:8]} | Revisions: {revisions}"
            )
        else:
            st.warning(
                f"Generated after {revisions} revision(s) with remaining review notes — ID: {assessment.assessment_id[:8]}"
            )

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_kpi_card("Role", assessment.job_title)
        with c2:
            render_kpi_card("Questions", str(len(assessment.questions)))
        with c3:
            render_kpi_card("Duration", f"{assessment.assessment_plan.duration_minutes} min")
        with c4:
            total_marks = sum(q.max_marks for q in assessment.questions)
            render_kpi_card("Total Marks", f"{total_marks:g}")

        st.markdown("")
        with open(docx_path, "rb") as f:
            st.download_button(
                label="Download Candidate Assessment (.docx)",
                data=f.read(),
                file_name=docx_path.name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary",
            )

        st.markdown("")
        with st.expander("Preview Questions, Expected Answers & Rubrics (Recruiter View)"):
            for idx, q in enumerate(assessment.questions, start=1):
                tags_html = (
                    f'<span class="badge badge-tag">{html.escape(q.skill_name)}</span>'
                    f'<span class="badge badge-tag">{html.escape(q.question_type.value.upper())}</span>'
                    f'<span class="badge badge-tag">{html.escape(q.difficulty.value.upper())}</span>'
                    f'<span class="badge badge-tag">{q.max_marks:g} Marks</span>'
                    f'<span class="badge badge-tag">{q.time_limit_minutes} Min</span>'
                )
                st.markdown(f"**Question {idx}**", unsafe_allow_html=False)
                st.markdown(tags_html, unsafe_allow_html=True)
                st.write(q.question_text)
                st.markdown(f"**Expected Answer:** {q.expected_answer}")
                st.markdown("**Evaluation Rubric:**")
                for criterion in q.evaluation_rubric:
                    st.markdown(f"- {criterion}")
                st.divider()

# --------------------------------------------------
# TAB 2: EVALUATE CANDIDATE
# --------------------------------------------------
with tab_evaluate:
    saved_assessments = list_saved_assessments()

    if not saved_assessments:
        st.info("No saved assessments available yet. Generate an assessment in the first tab.")
    else:
        with st.container(border=True):
            st.markdown('<div class="section-heading">Candidate Submission</div>', unsafe_allow_html=True)

            options = {
                f"{a.job_title} — {a.assessment_id[:8]} ({len(a.questions)} Questions)": a
                for a in saved_assessments
            }
            selected_label = st.selectbox("Select Reference Assessment", list(options.keys()))
            selected_assessment = options[selected_label]

            col_name, col_email = st.columns(2)
            candidate_name = col_name.text_input("Candidate Name", placeholder="Full name")
            candidate_email = col_email.text_input("Candidate Email", placeholder="candidate@example.com")

            uploaded_file = st.file_uploader(
                "Upload Completed Assessment (.docx)",
                type=["docx"],
            )

            col_eval_btn, _ = st.columns([1, 3])
            with col_eval_btn:
                evaluate_clicked = st.button(
                    "Evaluate Submission",
                    type="primary",
                    use_container_width=True,
                )

        if evaluate_clicked:
            if uploaded_file is None:
                st.warning("Please upload the candidate's completed .docx file.")
            else:
                with st.spinner("Extracting answers, grading against rubrics, and compiling report..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                            tmp.write(uploaded_file.getvalue())
                            tmp_path = tmp.name

                        eval_result = evaluation_graph.invoke(
                            {
                                "assessment": selected_assessment,
                                "submission_file_path": tmp_path,
                                "candidate_name": candidate_name.strip() or "Unknown Candidate",
                                "candidate_email": candidate_email.strip(),
                            }
                        )
                        report = eval_result["evaluation_report"]
                        save_evaluation_report(report)
                        report_docx = generate_evaluation_report_docx(report)

                        st.session_state["last_report"] = report
                        st.session_state["last_report_docx"] = report_docx
                    except Exception as e:
                        st.error(f"Evaluation failed: {e}")

        if "last_report" in st.session_state:
            report = st.session_state["last_report"]
            report_docx = Path(st.session_state["last_report_docx"])

            st.markdown("")
            st.success(f"Evaluation completed for {report.candidate_name}")

            m1, m2, m3 = st.columns(3)
            with m1:
                render_kpi_card(
                    "Total Score",
                    f"{report.total_marks_obtained:g} / {report.total_max_marks:g}",
                )
            with m2:
                render_kpi_card("Overall Percentage", f"{report.overall_percentage}%")
            with m3:
                rec_badge = render_recommendation_badge(report.recommendation.value)
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Recommendation</div>
                        <div style="margin-top: 4px;">{rec_badge}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("")
            with st.container(border=True):
                st.markdown('<div class="section-heading">Executive Summary</div>', unsafe_allow_html=True)
                st.write(report.executive_summary)

                c_str, c_gap = st.columns(2)
                with c_str:
                    st.markdown("**Key Strengths**")
                    for s in report.key_strengths:
                        st.markdown(f"- {s}")
                with c_gap:
                    st.markdown("**Areas for Improvement**")
                    for g in report.areas_for_improvement:
                        st.markdown(f"- {g}")

            with st.container(border=True):
                st.markdown('<div class="section-heading">Skill-Wise Performance</div>', unsafe_allow_html=True)
                for s in report.skill_breakdown:
                    col_label, col_bar, col_score = st.columns([2, 4, 2])
                    with col_label:
                        st.markdown(f"**{s.skill_name}**")
                    with col_bar:
                        st.progress(min(max(s.percentage / 100.0, 0.0), 1.0))
                    with col_score:
                        st.caption(
                            f"{s.marks_obtained:g}/{s.max_marks:g} ({s.percentage}%) · "
                            f"{s.questions_attempted}/{s.total_questions} attempted"
                        )

            st.markdown("")
            with open(report_docx, "rb") as f:
                st.download_button(
                    label="Download Evaluation Report (.docx)",
                    data=f.read(),
                    file_name=report_docx.name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    type="primary",
                )

            st.markdown("")
            with st.expander("Question-Wise Rubric Breakdown"):
                for qe in report.question_evaluations:
                    st.markdown(
                        f"**Question {qe.question_number} — {qe.skill_name} "
                        f"({qe.marks_awarded:g} / {qe.max_marks:g} Marks)**"
                    )
                    st.write(qe.feedback)
                    for rb in qe.rubric_breakdown:
                        badge_cls = "badge-met" if rb.met else "badge-unmet"
                        badge_txt = "MET" if rb.met else "NOT MET"
                        st.markdown(
                            f'<span class="badge {badge_cls}">{badge_txt}</span> '
                            f'<strong>{html.escape(rb.criterion)}</strong>: {html.escape(rb.notes)}',
                            unsafe_allow_html=True,
                        )
                    st.divider()

# --------------------------------------------------
# TAB 3: ASSESSMENT HISTORY
# --------------------------------------------------
with tab_history:
    saved = list_saved_assessments()
    if not saved:
        st.info("No assessments saved yet.")
    else:
        for a in saved:
            with st.container(border=True):
                col_info, col_meta = st.columns([3, 1])
                with col_info:
                    st.markdown(f"**{a.job_title}**")
                    skills_html = "".join(
                        f'<span class="badge badge-tag">{html.escape(s.skill_name)}</span>'
                        for s in a.assessment_plan.skill_assessments
                    )
                    st.markdown(skills_html, unsafe_allow_html=True)
                with col_meta:
                    st.caption(f"ID: `{a.assessment_id[:8]}`")
                    st.caption(
                        f"{len(a.questions)} questions · {a.assessment_plan.duration_minutes} min"
                    )