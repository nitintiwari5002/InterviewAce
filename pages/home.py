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
from core.ai import ollama_prompt

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

# ---- SECTIONS ----
def render_welcome():
    st.markdown("<h1 style='text-align:center;'>Welcome to InterviewAce!</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h4 style='text-align:center;'>Practice AI-powered mock interviews, get feedback, and build confidence for real interviews.</h4>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Get Started with Login"):
            st.session_state["navbar_state"] = "login"
            st.session_state["role"] = None
            st.session_state["login_success"] = None
            st.rerun()
    with col2:
        if st.button("Get Started with Registration"):
            st.session_state["navbar_state"] = "register"
            st.session_state["role"] = None
            st.session_state["login_success"] = None
            st.rerun()

def render_login():
    st.markdown("<h2 style='text-align:center;'>Login</h2>", unsafe_allow_html=True)
    role = st.radio("Login as:", ("User", "Company"), horizontal=True)
    st.session_state["role"] = role
    if role == "User":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login as User"):
            user = login_user(username, password)
            if user:
                st.success(f"Welcome, {username}!")
                st.session_state["login_success"] = True
                st.session_state["navbar_state"] = "user_dashboard"
                st.rerun()
            else:
                st.error("Invalid username or password.")
    else:
        company_name = st.text_input("Company Name")
        password = st.text_input("Password", type="password")
        if st.button("Login as Company"):
            company = login_company(company_name, password)
            if company:
                st.success(f"Welcome, {company_name}!")
                st.session_state["login_success"] = True
                st.session_state["navbar_state"] = "company_dashboard"
                st.rerun()
            else:
                st.error("Invalid company name or password.")
    if st.button("Back to Home"):
        reset_to_home()

def render_register():
    st.markdown("<h2 style='text-align:center;'>Register</h2>", unsafe_allow_html=True)
    role = st.radio("Register as:", ("User", "Company"), horizontal=True)
    st.session_state["role"] = role
    if role == "User":
        username = st.text_input("Choose Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Register as User"):
            success = register_user(username, email, password)
            if success:
                st.success(f"User {username} registered successfully! Please login.")
            else:
                st.error("Username already exists or invalid input.")
    else:
        company_name = st.text_input("Company Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Register as Company"):
            success = register_company(company_name, email, password)
            if success:
                st.success(f"Company {company_name} registered successfully! Please login.")
            else:
                st.error("Company name already exists or invalid input.")
    if st.button("Back to Home"):
        reset_to_home()

def render_user_dashboard():
    st.markdown("<h2>Interview Prep Dashboard (AI Powered)</h2>", unsafe_allow_html=True)
    career = st.selectbox("Select your career field:", [
        "Software Engineering", "Data Science", "Web Development", "Data Analyst",
        "Cyber Security", "DevOps", "Machine Learning", "Cloud Computing",
        "Data Structures", "Algorithms", "Database Management", "Networking",
    ])
    interview_type = st.selectbox("Type of Interview:", ["HR", "Technical", "Aptitude", "Behavioral"])

    question_prompt = (
        f"Generate 5 clear, non-repetitive {interview_type} interview questions "
        f"for the field {career}. Just list the questions, one per line, no numbering."
    )

    if st.button("Start Mock Interview (AI)", key="start_user_interview"):
        with st.spinner("Ollama is generating questions..."):
            ai_questions_str, err = ollama_prompt(question_prompt)
            if err:
                st.error(err)
            else:
                questions = [line.strip() for line in ai_questions_str.split("\n") if line.strip()]
                st.session_state["questions_generated"] = questions

    questions_for_interview = st.session_state.get("questions_generated") or []
    transcript_lines = []
    answers = []

    if questions_for_interview:
        total_q = len(questions_for_interview)
        for i, q in enumerate(questions_for_interview, 1):
            st.progress(i / total_q)
            st.write(f"Q{i}: {q}")
            ans = st.text_area(f"Your Text Answer for Q{i}:", key=f"answer_{i}_text")
            transcript_lines.append(f"Q{i}: {q}")
            transcript_lines.append(f"Text Answer: {ans}")

            st.write("Or record a video answer 👇")
            video_bytes = st.camera_input(f"Record Video for Q{i}")
            if video_bytes:
                st.video(video_bytes)
                transcript_lines.append("Video Answer: [recorded]")

            st.write("Or record an audio answer 👇")
            audio_bytes = st.audio_input(f"Record Audio for Q{i}")
            if audio_bytes:
                st.audio(audio_bytes)
                transcript_lines.append("Audio Answer: [recorded]")

            answers.append((q, ans))

        if st.button("Analyze Interview (AI)", key="user_analyze"):
            if not any(a.strip() for _, a in answers):
                st.warning("Please provide at least one text answer before analysis.")
            else:
                all_q_a = "\n".join([f"Q: {q}\nA: {a}" for q, a in answers])
                analyze_prompt = (
                    f"Act as an expert interviewer for {career}. Analyze the following answers.\n"
                    "Provide strengths, weaknesses, and concrete improvement tips.\n"
                    f"{all_q_a}"
                )
                with st.spinner("Ollama is analyzing..."):
                    analysis, err = ollama_prompt(analyze_prompt)
                    if err:
                        st.error(err)
                    else:
                        st.markdown("#### AI Analysis of your interview:")
                        st.write(analysis)

                        score = compute_score_from_analysis(analysis)
                        st.markdown(f"### Overall Score: {score}/100")
                        st.progress(score / 100)

                        breakdown = get_score_breakdown(analysis)
                        st.markdown("#### Visual Breakdown")

                        # Bar chart
                        st.bar_chart(breakdown)

                        # Pie chart
                        df = pd.DataFrame(
                            {"Category": list(breakdown.keys()), "Score": list(breakdown.values())}
                        )
                        fig, ax = plt.subplots()
                        ax.pie(df["Score"], labels=df["Category"], autopct="%1.0f%%", startangle=90)
                        ax.axis("equal")
                        st.pyplot(fig)

                        transcript_text = "\n".join(transcript_lines) + "\n\nAI Analysis:\n" + analysis
                        pdf_bytes = create_interview_pdf(transcript_text)
                        st.download_button(
                            label="Download Your Interview & Analysis (PDF)",
                            data=pdf_bytes,
                            file_name="interview_analysis.pdf",
                            mime="application/pdf",
                        )

    if st.button("Logout"):
        reset_to_home()

def render_company_dashboard():
    st.markdown("<h2>Company Interview Question Generator (AI)</h2>", unsafe_allow_html=True)
    topic = st.selectbox("Select topic/role:", [
        "Python", "Java", "System Design", "Data Structures", "Algorithms",
        "Database Management", "Networking", "Cloud Computing", "DevOps",
        "Machine Learning", "Web Development", "Cyber Security", "Data Science", "Data Analyst",
    ])
    difficulty = st.radio("Difficulty Level:", ["Basic", "Intermediate", "Advanced"], horizontal=True)

    if st.button("Generate Interview Questions (AI)"):
        prompt = (
            f"Generate 5 {difficulty.lower()} interview questions for the topic {topic}. "
            "Just list the questions, one per line, no numbering."
        )
        with st.spinner("Ollama is generating..."):
            questions_str, err = ollama_prompt(prompt)
            if err:
                st.error(err)
            else:
                questions = [line.strip() for line in questions_str.split("\n") if line.strip()]
                st.write("Generated Questions:")
                for q in questions:
                    st.write("-", q)

    if st.button("Logout (Company)"):
        reset_to_home()

# ---- ROUTER ----
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

# ---- SIDEBAR CHATBOT ABOUT SITE ----
with st.sidebar:
    st.markdown("### Ask about InterviewAce")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    user_msg = st.text_input("Your question about the site:", key="site_chat_input")

    if st.button("Ask", key="site_chat_button") and user_msg.strip():
        st.session_state["chat_history"].append(("You", user_msg))

        site_context = (
            "You are a helpful assistant for a web app called InterviewAce. "
            "InterviewAce is a Streamlit-based platform that lets users practice interviews "
            "with AI-generated questions and feedback, and lets companies generate interview "
            "questions for candidates. Explain features, usage, and benefits clearly and concisely."
        )

        prompt = site_context + "\nUser question: " + user_msg
        answer, err = ollama_prompt(prompt)

        if err:
            bot_reply = f"(Error from AI: {err})"
        else:
            bot_reply = answer

        st.session_state["chat_history"].append(("Bot", bot_reply))

    for speaker, msg in st.session_state["chat_history"]:
        if speaker == "You":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Bot:** {msg}")