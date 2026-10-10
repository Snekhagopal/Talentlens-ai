"""TalentLens AI — Resume Analyzer & Job Matcher."""

import streamlit as st

from src.job_analyzer import analyze_job, analyze_resume
from src.matcher import match_skills
from src.recommendations import generate_recommendations
from src.report_generator import to_csv, to_json
from src.resume_parser import UnsupportedFileError, extract_text
from src.schemas import MatchReport
from src.scoring import calculate_score
from src.config import SUPPORTED_EXTENSIONS
from src.gemini_client import GeminiClient, GeminiError


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="TalentLens AI | Resume Matcher",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            145deg, #faf8ff 0%, #f3f5ff 52%, #ffffff 100%
        );
        color: #302847;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    .stApp p,
    .stApp label,
    .stApp li {
        color: #302847;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg, #eee7ff 0%, #f6f4ff 55%, #ffffff 100%
        );
        border-right: 1px solid #ded5f5;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #30254d;
    }

    [data-testid="stSidebar"] code {
        display: block;
        background: #28243a !important;
        color: #ffffff !important;
        border-radius: 9px;
        padding: 0.75rem;
    }

    [data-testid="stSidebar"] code span {
        color: #ffffff !important;
    }

    .hero {
        background: linear-gradient(
            120deg, #6843d9 0%, #8060e8 48%, #4389ed 100%
        );
        padding: 2.5rem;
        border-radius: 24px;
        color: #ffffff;
        margin-top: 0.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 12px 35px rgba(104, 67, 217, 0.17);
    }

    .hero .hero-label {
        color: #ffffff !important;
        font-size: 0.76rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 750;
    }

    .hero h1 {
        color: #ffffff !important;
        font-size: clamp(2rem, 4vw, 3.1rem);
        line-height: 1.15;
        margin: 0.8rem 0;
        font-weight: 800;
    }

    .hero p {
        color: #f5f1ff !important;
        font-size: 1rem;
        max-width: 760px;
        line-height: 1.8;
        margin-bottom: 0;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 1.2rem;
        padding: 0.5rem 0.9rem;
        border: 1px solid rgba(255, 255, 255, 0.45);
        background: rgba(255, 255, 255, 0.15);
        color: #ffffff !important;
        border-radius: 999px;
        font-size: 0.8rem;
    }

    .section-heading {
        color: #292344 !important;
        font-size: 1.35rem;
        font-weight: 800;
        margin-top: 1.2rem;
        margin-bottom: 0.35rem;
    }

    .section-description {
        color: #625b78 !important;
        font-size: 0.92rem;
        line-height: 1.6;
        margin-bottom: 1.1rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #e5ddf5;
        border-radius: 17px;
    }

    [data-testid="stFileUploader"] {
        background: #ffffff !important;
        border: 1px solid #ded3f7 !important;
        border-radius: 14px !important;
        padding: 1rem !important;
    }

    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small {
        color: #41365d !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #faf8ff !important;
        border: 1px dashed #c9b9ef !important;
        border-radius: 11px !important;
    }

    [data-testid="stFileUploaderDropzone"] p,
    [data-testid="stFileUploaderDropzone"] span {
        color: #51446e !important;
    }

    [data-testid="stFileUploader"] button {
        background: #ffffff !important;
        color: #633fc4 !important;
        border: 1px solid #cfc1f3 !important;
        border-radius: 9px !important;
    }

    [data-testid="stFileUploader"] button p,
    [data-testid="stFileUploader"] button span {
        color: #633fc4 !important;
    }

    [data-testid="stTextArea"] label {
        color: #41365d !important;
        font-weight: 650;
    }

    [data-testid="stTextArea"] textarea {
        background: #ffffff !important;
        color: #292344 !important;
        border: 1px solid #dcd3ef !important;
        border-radius: 12px !important;
        line-height: 1.6;
        caret-color: #5635b7;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #777087 !important;
        -webkit-text-fill-color: #777087 !important;
        opacity: 1 !important;
    }

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e7e0f5;
        padding: 1.2rem;
        border-radius: 17px;
        box-shadow: 0 5px 20px rgba(69, 48, 125, 0.045);
    }

    [data-testid="stMetricLabel"] {
        color: #655c7b !important;
    }

    [data-testid="stMetricValue"] {
        color: #5635b7 !important;
        font-weight: 800;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(
            100deg, #7048d9 0%, #4389ed 100%
        ) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        min-height: 3.2rem;
        font-weight: 700;
        box-shadow: 0 6px 18px rgba(104, 67, 217, 0.20);
        transition: 0.2s ease;
    }

    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span {
        color: #ffffff !important;
    }

    .stButton > button[kind="primary"]:hover:not(:disabled) {
        filter: brightness(1.06);
        border: none !important;
        transform: translateY(-1px);
    }

    .stButton > button[kind="primary"]:disabled {
        background: #e5ddf8 !important;
        color: #5b4b7c !important;
        border: 1px solid #d4c5f2 !important;
        opacity: 1 !important;
        box-shadow: none !important;
        cursor: not-allowed;
    }

    .stButton > button[kind="primary"]:disabled p,
    .stButton > button[kind="primary"]:disabled span {
        color: #5b4b7c !important;
    }

    .stDownloadButton > button {
        background: #ffffff !important;
        color: #633fc4 !important;
        border: 1px solid #cfc1f3 !important;
        border-radius: 11px !important;
        min-height: 2.8rem;
        font-weight: 650;
    }

    .stDownloadButton > button p,
    .stDownloadButton > button span {
        color: #633fc4 !important;
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #7650df, #4389ed);
    }

    [data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid #e7e0f5;
        border-radius: 13px;
    }

    .footer {
        color: #777087 !important;
        text-align: center;
        font-size: 0.82rem;
        padding-top: 2.5rem;
        border-top: 1px solid #e9e3f5;
        margin-top: 2rem;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1.5rem 1rem;
        }

        .hero {
            padding: 1.5rem;
            border-radius: 18px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# GEMINI CLIENT
# =====================================================

client = GeminiClient()


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("# 💜 TalentLens AI")
    st.caption("RESUME INTELLIGENCE")
    st.divider()

    st.markdown("### Navigation")
    st.markdown("🏠 Resume Dashboard")
    st.markdown("📊 Match Analysis")
    st.markdown("✨ AI Recommendations")
    st.markdown("📥 Export Reports")
    st.divider()

    st.markdown("### Hosted AI Settings")
    st.caption("ACTIVE MODEL")
    st.code(client.model, language=None)

    try:
        gemini_available = client.is_available()
    except Exception:
        gemini_available = False

    if gemini_available:
        st.success("Gemini API is connected")
    else:
        st.error("Gemini API is not reachable")
        st.caption(
            "Check your API key, model availability, internet connection, and quota."
        )

    want_recs = st.checkbox(
        "Generate AI recommendations",
        value=True,
        help="Generate suggestions using the configured hosted Gemini model.",
    )

    st.divider()
    st.caption(
        "🔒 Resume text is sent to the configured AI service for analysis. "
        "Avoid uploading sensitive documents when testing."
    )


# =====================================================
# HERO SECTION
# =====================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-label">
            AI-POWERED CAREER INTELLIGENCE
        </div>
        <h1>Find your next opportunity.</h1>
        <p>
            Discover how your resume aligns with a job description.
            Identify your strengths, uncover skill gaps, and get
            actionable suggestions using the hosted Gemini API.
        </p>
        <div class="hero-badge">
            ✦ Powered by Gemini API · Free-tier usage subject to limits
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# RESUME AND JOB INPUT
# =====================================================

st.markdown(
    '<div class="section-heading">Start your analysis</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Upload your resume and provide the job description you want to target.
        Your analysis will appear below.
    </div>
    """,
    unsafe_allow_html=True,
)

resume_col, job_col = st.columns([0.9, 1.1], gap="large")

with resume_col:
    with st.container(border=True):
        st.markdown("### 📄 Your resume")
        st.caption("Upload a PDF, DOCX or TXT file.")

        uploaded = st.file_uploader(
            "Upload your resume",
            type=[ext.lstrip(".") for ext in SUPPORTED_EXTENSIONS],
            help="Select a resume file from your computer.",
            key="resume_upload",
        )

        if uploaded is not None:
            st.success(f"Ready to analyze: {uploaded.name}")

with job_col:
    with st.container(border=True):
        st.markdown("### 🎯 Target job")
        st.caption("Paste the complete job description below.")

        job_text = st.text_area(
            "Job description",
            height=235,
            placeholder=(
                "Paste the job title, required skills, responsibilities, "
                "experience requirements and qualifications here..."
            ),
            label_visibility="collapsed",
            key="job_description",
        )

st.markdown("")

analyze_clicked = st.button(
    "✨  Analyze My Resume",
    type="primary",
    use_container_width=True,
    disabled=not (uploaded is not None and job_text.strip()),
)


# =====================================================
# ANALYSIS PIPELINE
# =====================================================

if analyze_clicked:
    try:
        with st.spinner("Reading your resume..."):
            resume_text = extract_text(
                uploaded.getvalue(),
                uploaded.name,
            )

        if not resume_text or not resume_text.strip():
            st.error(
                "No readable text was extracted from your resume. "
                "A scanned PDF may require OCR."
            )
            st.stop()

        with st.spinner(
            "AI is analyzing your resume and job description..."
        ):
            resume = analyze_resume(resume_text, client)
            job = analyze_job(job_text, client)

        with st.spinner("Matching skills and calculating your score..."):
            skills = match_skills(resume, job)
            score = calculate_score(resume, job, skills)

        recommendations = None

        if want_recs:
            with st.spinner("Generating personalized recommendations..."):
                recommendations = generate_recommendations(
                    resume,
                    job,
                    skills,
                    score,
                    client,
                )

        report = MatchReport(
            resume=resume,
            job=job,
            skills=skills,
            score=score,
            recommendations=recommendations,
        )

        st.session_state["report"] = report
        st.session_state["report_filename"] = uploaded.name

        st.success("Analysis completed successfully!")

    except (UnsupportedFileError, GeminiError) as exc:
        st.error(str(exc))
        print(f"Analysis error: {type(exc).__name__}: {exc}")

    except Exception as err:
        import traceback

        st.error("Analysis failed. Check the terminal for the full error.")
        print("\n--- FULL ANALYSIS ERROR ---")
        traceback.print_exc()
        print("--- END ERROR ---\n")


# =====================================================
# RESULTS DASHBOARD
# =====================================================

report: MatchReport | None = st.session_state.get("report")

if report:
    st.divider()

    score = report.score
    skills = report.skills

    st.markdown(
        '<div class="section-heading">Your match overview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Review your compatibility scores and understand how your
            qualifications compare with the target job.
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric1, metric2, metric3, metric4 = st.columns(4, gap="medium")

    metric1.metric("Overall match", f"{score.overall:.1f}%")
    metric2.metric("Required skills", f"{score.required_skills:.1f}%")
    metric3.metric("Preferred skills", f"{score.preferred_skills:.1f}%")
    metric4.metric("Experience", f"{score.experience:.1f}%")

    progress_value = max(
        0.0,
        min(1.0, float(score.overall) / 100),
    )

    st.progress(
        progress_value,
        text=f"Overall compatibility: {score.overall:.1f}%",
    )

    # Skill categories
    st.markdown(
        '<div class="section-heading">Skills breakdown</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Review matching skills, missing requirements and additional
            skills found in your resume.
        </div>
        """,
        unsafe_allow_html=True,
    )

    matched_skills = (
        skills.matched_required + skills.matched_preferred
    )

    missing_skills = (
        [(item, "Required") for item in skills.missing_required]
        + [(item, "Preferred") for item in skills.missing_preferred]
    )

    matched_col, missing_col, extra_col = st.columns(3, gap="medium")

    with matched_col:
        with st.container(border=True):
            st.markdown("### 🟢 Matched skills")

            if matched_skills:
                for item in matched_skills:
                    st.markdown(f"- {item}")
            else:
                st.caption("No matching skills identified.")

    with missing_col:
        with st.container(border=True):
            st.markdown("### 🔴 Missing skills")

            if missing_skills:
                for item, category in missing_skills:
                    st.markdown(f"- **{item}** — {category}")
            else:
                st.caption("No missing skills identified.")

    with extra_col:
        with st.container(border=True):
            st.markdown("### 🔵 Additional skills")

            if skills.extra_skills:
                for item in skills.extra_skills:
                    st.markdown(f"- {item}")
            else:
                st.caption("No additional skills identified.")

    # Recommendations
    if report.recommendations:
        st.markdown(
            '<div class="section-heading">AI recommendations</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-description">
                Suggestions generated from your resume and job analysis.
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown("### ✨ Your improvement plan")
            st.write(report.recommendations.summary)

            for index, suggestion in enumerate(
                report.recommendations.suggestions,
                start=1,
            ):
                st.markdown(f"**{index}.** {suggestion}")

    # Downloads
    st.markdown(
        '<div class="section-heading">Export your report</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Download the current analysis for later review.
        </div>
        """,
        unsafe_allow_html=True,
    )

    json_col, csv_col = st.columns(2)

    with json_col:
        st.download_button(
            "📄 Download JSON",
            data=to_json(report),
            file_name="match_report.json",
            mime="application/json",
            use_container_width=True,
        )

    with csv_col:
        st.download_button(
            "📊 Download CSV",
            data=to_csv(report),
            file_name="match_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

else:
    with st.container(border=True):
        st.markdown("### ✨ Your analysis will appear here")
        st.write(
            "Upload your resume, paste a job description and click "
            "**Analyze My Resume** to generate your first report."
        )


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">
        <strong>TalentLens AI</strong><br>
        Python · Streamlit · Gemini API<br>
        AI-assisted career insights with Python-based scoring
    </div>
    """,
    unsafe_allow_html=True,
)