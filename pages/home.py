import streamlit as st
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt

from core.db import (
    create_tables,
    register_user,
    register_company,
    login_user,
    login_company,
)
from core.ai import prompt

# ---- DB INIT ----
create_tables()

# ---- SESSION MANAGEMENT ----
SESSION_DEFAULTS = {
    "navbar_state": None,
    "role": None,
    "login_success": None,
    "questions_generated": None,
}

def init_session():
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_to_home():
    for key, value in SESSION_DEFAULTS.items():
        st.session_state[key] = value
    st.rerun()

init_session()

# ---- PDF CREATOR ----
def _sanitize_for_pdf(text: str) -> str:
    text = (
        text.replace("–", "-")
            .replace("—", "-")
            .replace("“", "\"")
            .replace("”", "\"")
            .replace("’", "'")
    )
    cleaned = []
    for ch in text:
        try:
            ch.encode("latin-1")
            cleaned.append(ch)
        except UnicodeEncodeError:
            cleaned.append("?")
    return "".join(cleaned)

def create_interview_pdf(transcript_text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    safe_text = _sanitize_for_pdf(transcript_text)

    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf_bytes = pdf.output(dest="S").encode("latin-1", "ignore")
    return pdf_bytes

# ---- SIMPLE SCORING FROM ANALYSIS ----
def compute_score_from_analysis(analysis: str) -> int:
    text = analysis.lower()
    score = 50  # neutral baseline

    positives = ["strong", "excellent", "good", "confident", "clear", "impressive"]
    negatives = ["weak", "improve", "improvement", "poor", "unclear", "lack", "insufficient"]

    for w in positives:
        if w in text:
            score += 5
    for w in negatives:
        if w in text:
            score -= 5

    return max(0, min(100, score))

def get_score_breakdown(analysis: str) -> dict:
    text = analysis.lower()
    categories = {
        "Strengths": 0,
        "Weaknesses": 0,
        "Communication": 0,
        "Technical Depth": 0,
    }

    if "strength" in text or "strong" in text or "good" in text:
        categories["Strengths"] = 70
    if "weak" in text or "improve" in text or "lack" in text:
        categories["Weaknesses"] = 60
    if "communication" in text or "clarity" in text or "clear" in text:
        categories["Communication"] = 65
    if "technical" in text or "concepts" in text or "knowledge" in text:
        categories["Technical Depth"] = 65

    for k, v in categories.items():
        if v == 0:
            categories[k] = 40

    return categories

# ---- BASIC STYLES & NAVBAR ----
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f2027 0%, #2c5364 35%, #6a3093 75%, #ffeb70 100%);
        min-height: 100vh;
    }
    .navbar-flex {
        width: 100vw; margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        background: linear-gradient(90deg, #0f2027 0%, #6a3093 48%, #ffeb70 100%);
        height: 76px; box-shadow: 0 12px 40px rgba(44,83,100,0.18);
        border-bottom-left-radius: 30px; border-bottom-right-radius: 30px;
        display: flex; align-items: center; justify-content: space-between;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        font-size: 2.25rem; color: #fff; letter-spacing: 2px;
        position: sticky; top: 0; z-index: 999; text-shadow: 0 2px 6px #0f2027;
        padding: 0 2.5em;
    }
    </style>
    <div class='navbar-flex'>
        <span>InterviewAce</span>
    </div>
""", unsafe_allow_html=True)

st.image("assets/Mini (2).png", width=250)

# ---------------- SCREENS ----------------
def render_welcome():
    st.markdown("<h1 style='text-align:center;'>Welcome to InterviewAce!</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h4 style='text-align:center;'>Practice AI-powered mock interviews, get feedback, and build confidence for real interviews.</h4>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state["navbar_state"] = "login"
            st.rerun()
    with col2:
        if st.button("Register"):
            st.session_state["navbar_state"] = "register"
            st.rerun()

def render_login():
    role = st.radio("Login as:", ["User", "Company"], horizontal=True)
    st.session_state["role"] = role

    if role == "User":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(u, p):
                st.session_state["navbar_state"] = "user_dashboard"
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        c = st.text_input("Company Name")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_company(c, p):
                st.session_state["navbar_state"] = "company_dashboard"
                st.rerun()
            else:
                st.error("Invalid credentials")

    if st.button("Back"):
        reset_to_home()

def render_register():
    role = st.radio("Register as:", ["User", "Company"], horizontal=True)

    if role == "User":
        u = st.text_input("Username")
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("Register"):
            register_user(u, e, p)
            st.success("Registered successfully")
    else:
        c = st.text_input("Company Name")
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("Register"):
            register_company(c, e, p)
            st.success("Registered successfully")

    if st.button("Back"):
        reset_to_home()

# ---------------- USER DASHBOARD ----------------
def render_user_dashboard():
    st.header("🎤 Audio-Only Mock Interview")

    # SINGLE CAMERA (OPTIONAL)
    st.subheader("Camera Preview (Optional)")
    cam = st.camera_input("Camera Preview", key="single_camera")
    if cam:
        st.video(cam)

    career = st.selectbox(
        "Career Field",
        ["Software Engineering", "Data Science", "Machine Learning",
         "Cyber Security", "Cloud Computing", "Database Administrator", "Data Analyst", "Web Development"]
    )

    interview_type = st.selectbox(
        "Interview Type",
        ["HR", "Technical", "Behavioral"]
    )

    if st.button("Start Interview"):
        question_prompt = f"""
Generate exactly 5 {interview_type} interview questions
for a {career} candidate.

Rules:
- Each line must be ONE question
- Each must end with ?
- No explanations
- No numbering
"""

        # ---- SAFER PROMPT HANDLING + PARSING ----
        raw, err = prompt(question_prompt, mode="questions")
        if err:
            st.error(err)
            return

        if not isinstance(raw, str) or not raw.strip():
            st.error("Could not generate questions. Please check the AI service and try again.")
            return

        lines = [l.strip() for l in raw.split("\n") if l.strip()]
        candidate_qs = [l for l in lines if "?" in l]

        cleaned = []
        for q in candidate_qs:
            # Keep text up to first question mark
            if "?" in q:
                q = q.split("?", 1)[0] + "?"
            # Remove simple numbering like "1. ", "Q1:", etc.
            q = q.lstrip("Qq0123456789.:-) ").strip()
            cleaned.append(q)

        questions = cleaned[:5]

        if len(questions) < 5:
            st.error("Failed to generate valid questions. Retry.")
            # Optional debug (remove in production)
            st.write("DEBUG RAW QUESTIONS:", raw)
            return

        st.session_state["questions_generated"] = questions

    questions = st.session_state.get("questions_generated") or []

    transcript_lines = []
    audio_flags = []

    if questions:
        for i, q in enumerate(questions, 1):
            st.markdown(f"### Q{i}: {q}")

            audio = st.audio_input(
                f"Record Answer (Q{i})",
                key=f"audio_{i}"
            )

            transcript_lines.append(f"Q{i}: {q}")

            if audio:
                st.audio(audio)
                transcript_lines.append("Audio Answer: [recorded]")
                audio_flags.append(True)
            else:
                audio_flags.append(False)

        if st.button("Analyze Interview"):
            if not any(audio_flags):
                st.warning("Please record at least one audio answer.")
                return

            analysis_prompt = """
You are an expert interviewer.

The candidate answered questions using audio only.
No transcript is available.

Evaluate based on:
- Clarity
- Confidence
- Structure
- Professional tone
- Likely technical depth

Provide strengths, weaknesses, and improvement tips.
"""

            analysis, err = prompt(analysis_prompt, mode="analysis")
            if err:
                st.error(err)
                return

            st.subheader("AI Feedback")
            st.write(analysis)

            score = compute_score_from_analysis(analysis)
            st.metric("Overall Score", f"{score}/100")
            st.progress(score / 100)

            transcript = "\n".join(transcript_lines) + "\n\nAI Analysis:\n" + analysis
            pdf = create_interview_pdf(transcript)

            st.download_button(
                "Download Interview Report (PDF)",
                pdf,
                "interview_report.pdf",
                "application/pdf"
            )

    if st.button("Logout"):
        reset_to_home()

# ---------------- COMPANY DASHBOARD ----------------
def render_company_dashboard():
    st.header("Company Question Generator")

    topic = st.selectbox(
        "Topic",
        ["Python", "System Design", "Data Science", "Cloud Computing", "Database Administrator", "Data Analyst", "Web Development"]
    )

    level = st.radio("Difficulty", ["Basic", "Intermediate", "Advanced"], horizontal=True)

    if st.button("Generate Questions"):
        q, err = prompt(
            f"Generate 5 {level} interview questions for {topic}.",
            mode="questions"
        )
        if err:
            st.error(err)
        else:
            if not isinstance(q, str) or not q.strip():
                st.error("Could not generate questions. Please try again.")
            else:
                for line in q.split("\n"):
                    if line.strip():
                        st.write("•", line)

    if st.button("Logout"):
        reset_to_home()

# ---------------- ROUTER ----------------
state = st.session_state["navbar_state"]

if state is None:
    render_welcome()
elif state == "login":
    render_login()
elif state == "register":
    render_register()
elif state == "user_dashboard":
    render_user_dashboard()
elif state == "company_dashboard":
    render_company_dashboard()
