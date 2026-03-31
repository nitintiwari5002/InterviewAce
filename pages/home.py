import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import re

from core.db import (
    create_tables,
    register_user,
    register_company,
    login_user,
    login_company,
)
from core.ai import prompt

st.set_page_config(page_title="InterviewAce", layout="wide")

# DB INIT
create_tables()

# SESSION
SESSION_DEFAULTS = {
    "navbar_state": None,
    "role": None,
    "questions_generated": None,
    "qa_pairs": None,
    "company_qa_pairs": None,
}

def init_session():
    for k, v in SESSION_DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_to_home():
    for k in SESSION_DEFAULTS:
        st.session_state[k] = None
    st.rerun()

init_session()

# ---------------- PDF ----------------
def _sanitize_for_pdf(text: str) -> str:
    text = (
        text.replace("–", "-")
        .replace("—", "-")
        .replace("“", "\"")
        .replace("”", "\"")
        .replace("’", "'")
    )
    return "".join(ch if ch.encode("latin-1", "ignore") else "?" for ch in text)

def create_interview_pdf(text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(True, 15)
    pdf.set_font("Arial", size=12)

    for line in _sanitize_for_pdf(text).split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin-1", "ignore")

# ---------------- UTIL ----------------
def img_to_data_url(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    b64 = base64.b64encode(p.read_bytes()).decode()
    mime = "image/jpeg" if p.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
    return f"data:{mime};base64,{b64}"

def compute_score_from_analysis(text: str) -> int:
    if not text:
        return 0
    score = 50
    pos = ["strong","excellent","good","confident","clear"]
    neg = ["weak","poor","unclear","lack","improve"]

    for w in pos:
        if w in text.lower(): score += 5
    for w in neg:
        if w in text.lower(): score -= 5

    return max(0, min(100, score))

# ---------------- UI ----------------
def render_welcome():
    st.title("InterviewAce")
    st.subheader("AI Mock Interviews + Feedback")

    c1, c2 = st.columns(2)
    if c1.button("Login"):
        st.session_state["navbar_state"] = "login"
        st.rerun()
    if c2.button("Register"):
        st.session_state["navbar_state"] = "register"
        st.rerun()

# ---------------- LOGIN ----------------
def render_login():
    role = st.radio("Login as", ["User", "Company"])

    if role == "User":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(u, p):
                st.session_state["navbar_state"] = "user_dashboard"
                st.rerun()
            else:
                st.error("Invalid login")
    else:
        c = st.text_input("Company")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_company(c, p):
                st.session_state["navbar_state"] = "company_dashboard"
                st.rerun()
            else:
                st.error("Invalid login")

    if st.button("Back"):
        reset_to_home()

# ---------------- REGISTER ----------------
def render_register():
    role = st.radio("Register as", ["User", "Company"])

    if role == "User":
        if st.button("Register"):
            register_user("user","email","pass")
            st.success("Registered")
    else:
        if st.button("Register"):
            register_company("company","email","pass")
            st.success("Registered")

    if st.button("Back"):
        reset_to_home()

# ---------------- USER DASHBOARD ----------------
def render_user_dashboard():
    st.header("Mock Interview")

    career = st.selectbox("Field", ["Software Engineering","Data Science"])
    difficulty = st.selectbox("Difficulty", ["Basic","Intermediate","Advanced"])

    if st.button("Generate Questions"):
        q_raw, _ = prompt("Generate 5 interview Q/A", mode="questions")

        qa = []
        for line in q_raw.split("\n"):
            if line.startswith("Q:"):
                qa.append({"q": line, "a": ""})

        st.session_state["qa_pairs"] = qa

    qa_pairs = st.session_state.get("qa_pairs") or []

    if qa_pairs:
        transcript = []

        for i, p in enumerate(qa_pairs, 1):
            st.write(p["q"])
            audio = st.audio_input("Answer")

            transcript.append(p["q"])
            transcript.append("Answered" if audio else "No answer")

        if st.button("Analyze"):
            analysis, _ = prompt("Analyze interview", mode="analysis")
            st.write(analysis)

            score = compute_score_from_analysis(analysis)
            st.metric("Score", score)

            pdf = create_interview_pdf("\n".join(transcript + [analysis]))

            st.download_button(
                "Download PDF",
                pdf,
                "report.pdf",
                "application/pdf"
            )

    if st.button("Logout"):
        reset_to_home()

# ---------------- COMPANY DASHBOARD ----------------
def render_company_dashboard():
    st.header("Company Question Generator")

    topic = st.selectbox("Topic", ["Python","System Design"])
    level = st.radio("Difficulty", ["Basic","Intermediate","Advanced"])

    if st.button("Generate"):
        q_raw, _ = prompt("Generate Q/A", mode="questions")

        qa = re.findall(r"Q:(.*?)Demo answer:(.*?)(?=Q:|$)", q_raw, re.DOTALL)

        pairs = [{"q": q.strip(), "a": a.strip()} for q, a in qa]

        st.session_state["company_qa_pairs"] = pairs

    pairs = st.session_state.get("company_qa_pairs") or []

    for i, p in enumerate(pairs, 1):
        st.write(f"Q{i}: {p['q']}")
        with st.expander("Answer"):
            st.write(p["a"])

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
