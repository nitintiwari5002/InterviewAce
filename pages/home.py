import streamlit as st
import sqlite3
import requests
from fpdf import FPDF

# ---- DATABASE SETUP ----
def get_connection():
    return sqlite3.connect("users.db")

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()
create_tables()

# ---- DB FUNCTIONS ----
def register_user(username, email, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def register_company(company_name, email, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO companies (company_name, email, password) VALUES (?, ?, ?)",
                    (company_name, email, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user

def login_company(company_name, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies WHERE company_name=? AND password=?", (company_name, password))
    company = cur.fetchone()
    conn.close()
    return company

# ---- OLLAMA HELPER ----
def ollama_prompt(prompt, model="llama2"):
    url = "http://localhost:11434/api/generate"
    try:
        response = requests.post(url, json={"model": model, "prompt": prompt, "stream":False})
        if response.ok:
            return response.json()["response"]
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Ollama connection error: {e}"

# ---- PDF CREATOR ----
def create_interview_pdf(transcript_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in transcript_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output

# ---- BASIC STYLES & NAVBAR ----
st.markdown("""
    <style>
    body { background: linear-gradient(135deg, #0f2027 0%, #2c5364 35%, #6a3093 75%, #ffeb70 100%); min-height: 100vh; }
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

for key in ["navbar_state", "role", "login_success", "questions_generated"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ---- WELCOME PAGE ----
if st.session_state["navbar_state"] is None:
    st.markdown("<h1 style='text-align:center;'>Welcome to InterviewAce!</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>Practice with AI-powered mock interviews, get real-time feedback, and ace your engineering interviews with confidence!</h4>", unsafe_allow_html=True)
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

# ---- LOGIN FLOW ----
if st.session_state["navbar_state"] == "login" and st.session_state["login_success"] is None:
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
        st.session_state["navbar_state"] = None
        st.session_state["role"] = None
        st.session_state["login_success"] = None
        st.rerun()

# ---- REGISTRATION FLOW ----
if st.session_state["navbar_state"] == "register":
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
                st.success(f"User {username} registered successfully!")
            else:
                st.error("Username already exists. Please choose a different one.")
    else:
        company_name = st.text_input("Company Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Register as Company"):
            success = register_company(company_name, email, password)
            if success:
                st.success(f"Company {company_name} registered successfully!")
            else:
                st.error("Company name already exists. Please choose a different one.")
    if st.button("Back to Home"):
        st.session_state["navbar_state"] = None
        st.session_state["role"] = None
        st.rerun()

# ---- USER DASHBOARD ----
if st.session_state["navbar_state"] == "user_dashboard":
    st.markdown("<h2>Interview Prep Dashboard (AI Powered)</h2>", unsafe_allow_html=True)
    career = st.selectbox("Select your career field:", [
        "Software Engineering", "Data Science", "Web Development", "Data Analyst", "Cyber Security", "DevOps", "Machine Learning", "Cloud Computing", "Data Structures", "Algorithms", "Database Management", "Networking"
    ])
    interview_type = st.selectbox("Type of Interview:", ["HR", "Technical", "Aptitude", "Behavioral"])
    
    question_prompt = f"Generate 5 relevant {interview_type} interview questions for the field {career}. Only list the questions."
    ai_questions = None

    if st.button("Start Mock Interview (AI)", key="start_user_interview"):
        with st.spinner("Ollama is generating questions..."):
            ai_questions_str = ollama_prompt(question_prompt)
            ai_questions = [line.strip('-•1234567890. ') for line in ai_questions_str.split('\n') if line.strip()]
            st.session_state["questions_generated"] = ai_questions

    questions_for_interview = st.session_state.get("questions_generated", None)
    transcript_lines = []
    if questions_for_interview:
        answers = []
        for i, q in enumerate(questions_for_interview, 1):
            st.write(f"Q{i}: {q}")
            ans = st.text_area(f"Your Text Answer for Q{i}:", key=f"answer_{i}_text")
            transcript_lines.append(f"Q{i}: {q}")
            transcript_lines.append(f"Text Answer: {ans}")

            st.write("Or record a video answer 👇")
            video_bytes = st.camera_input(f"Record Video for Q{i}")
            if video_bytes:
                st.video(video_bytes)
                transcript_lines.append("Video Answer: [saved]")

            st.write("Or record an audio answer 👇")
            audio_bytes = st.audio_input(f"Record Audio for Q{i}")
            if audio_bytes:
                st.audio(audio_bytes)
                transcript_lines.append("Audio Answer: [saved]")

            answers.append((q, ans))

        analysis = None
        if st.button("Analyze Interview (AI)", key="user_analyze"):
            all_q_a = '\n'.join([f"Q: {q}\nA: {a}" for q, a in answers])
            analyze_prompt = (
                f"Act as an HR/technical interview expert. Analyze the following candidate answers for an interview in {career}.\n"
                "Give strengths, weaknesses, and improvement tips. Here are their answers:\n"
                f"{all_q_a}"
            )
            with st.spinner("Ollama is analyzing..."):
                analysis = ollama_prompt(analyze_prompt)
            st.markdown("#### AI Analysis of your interview:")
            st.write(analysis)

            # PDF download
            transcript_text = "\n".join(transcript_lines) + "\n\nAI Analysis:\n" + str(analysis)
            pdf_bytes = create_interview_pdf(transcript_text)
            st.download_button(
                label="Download Your Interview & Analysis (PDF)",
                data=pdf_bytes,
                file_name="interview_analysis.pdf",
                mime="application/pdf"
            )

    if st.button("Logout"):
        st.session_state["navbar_state"] = None
        st.session_state["login_success"] = None
        st.session_state["role"] = None
        st.session_state["questions_generated"] = None
        st.rerun()

# ---- COMPANY DASHBOARD ----
if st.session_state["navbar_state"] == "company_dashboard":
    st.markdown("<h2>Company Interview Question Generator (AI)</h2>", unsafe_allow_html=True)
    topic = st.selectbox("Select topic/role:", [
        "Python", "Java", "System Design", "Data Structures", "Algorithms", "Database Management", "Networking", "Cloud Computing", "DevOps", "Machine Learning", "Web Development", "Cyber Security", "Data Science", "Data Analyst"
    ])
    difficulty = st.radio("Difficulty Level:", ["Basic", "Intermediate", "Advanced"], horizontal=True)

    if st.button("Generate Interview Questions (AI)"):
        prompt = f"Generate 5 {difficulty.lower()} interview questions for the topic {topic}. Just list the questions."
        with st.spinner("Ollama is generating..."):
            questions_str = ollama_prompt(prompt)
            questions = [line.strip('-•1234567890. ') for line in questions_str.split('\n') if line.strip()]
            st.write("Generated Questions:")
            for q in questions:
                st.write("-", q)

    if st.button("Logout (Company)"):
        st.session_state["navbar_state"] = None
        st.session_state["login_success"] = None
        st.session_state["role"] = None
        st.rerun()
