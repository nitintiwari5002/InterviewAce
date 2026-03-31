import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path
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

st.set_page_config(page_title="InterviewAce", layout="wide")

# DB INITIALIZATION
create_tables()

# SESSION MANAGEMENT
SESSION_DEFAULTS = {
    "navbar_state": None,
    "role": None,
    "login_success": None,
    "questions_generated": None,
    "qa_pairs": None,
    "company_qa_pairs": None,  # for company dashboard Q/A
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
from fpdf import FPDF

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

def create_interview_pdf(text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    safe_text = _sanitize_for_pdf(text)

    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin-1", "ignore")
# IMAGE VIA URL
def img_to_data_url(path: str) -> str:
    p = Path(path)
    if not p.exists():
        st.warning(f"Image not found: {path}")
        return ""
    data = p.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    if p.suffix.lower() in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    else:
        mime = "image/png"
    return f"data:{mime};base64,{b64}"

# PDF GENERATION
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
        pdf.multi_cell(0, 8, line)

    pdf_bytes = pdf.output(dest="S").encode("latin-1", "ignore")
    return pdf_bytes

# SIMPLE SCORING FROM ANALYSIS
def compute_score_from_analysis(analysis: str) -> int:
    """Heuristic score 0–100 based on analysis text."""
    if not isinstance(analysis, str) or not analysis.strip():
        return 0

    text = analysis.lower()
    score = 50  # neutral baseline

    positive_keywords = [
        "strong", "excellent", "good", "confident", "clear",
        "impressive", "well-structured", "outstanding", "solid",
    ]
    negative_keywords = [
        "weak", "improve", "improvement", "poor", "unclear",
        "lack", "insufficient", "disorganized", "inconsistent",
        "needs significant improvement",
    ]

    for w in positive_keywords:
        if w in text:
            score += 5
    for w in negative_keywords:
        if w in text:
            score -= 5

    score = max(0, min(100, score))
    return score

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

# STYLES AND NAVBAR
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

# centered logo
left, center, right = st.columns([2, 2, 1])
with center:
    st.image("assets/Mini (2).png", width=250)

# SCREENS
def render_welcome():
    st.markdown(
        """
        <h1 style='text-align:center; margin-top: 1.5rem;'>Welcome to InterviewAce!</h1>
        <h4 style='text-align:center; font-weight: 400; margin-bottom: 1.2rem;'>
            Practice AI-powered mock interviews, get feedback, and build confidence for real interviews.
        </h4>
        """,
        unsafe_allow_html=True,
    )

    img1 = img_to_data_url("assets/banner1.png")
    img2 = img_to_data_url("assets/banner2.png")
    img3 = img_to_data_url("assets/banner3.png")

    carousel_html = f"""
<div style="display:flex; justify-content:center; margin-bottom: 2.5rem;">
  <div id="hero-carousel" style="
      width: 80vw;
      max-width: 1100px;
      position: relative;
      overflow: hidden;
      border-radius: 18px;
      box-shadow: 0 22px 55px rgba(0,0,0,0.55);
      background: radial-gradient(circle at top left, rgba(255,235,112,0.35), transparent 50%),
                  radial-gradient(circle at bottom right, rgba(106,48,147,0.45), transparent 55%);
  ">
    <div style="
        position:absolute; inset:0;
        background: linear-gradient(to bottom,
                    rgba(0,0,0,0.35),
                    rgba(0,0,0,0.45));
        pointer-events:none;
        z-index: 1;
    "></div>

    <div id="hero-slides" style="
        display: flex;
        width: 300%;
        transition: transform 0.6s ease-in-out;
    ">
      <img src="{img1}" alt="Mock interview practice"
           style="width: 33.3333%; height: 360px; object-fit: contain; background:#000; flex-shrink: 0;">
      <img src="{img2}" alt="AI-powered feedback"
           style="width: 33.3333%; height: 360px; object-fit: contain; background:#000; flex-shrink: 0;">
      <img src="{img3}" alt="Interview analytics"
           style="width: 33.3333%; height: 360px; object-fit: contain; background:#000; flex-shrink: 0;">
    </div>

    <button id="hero-prev" style="
        position:absolute; top:50%; left:18px; transform:translateY(-50%);
        width:42px; height:42px;
        display:flex; align-items:center; justify-content:center;
        background:rgba(0,0,0,0.55); color:#fff; border:none;
        border-radius:50%; cursor:pointer; font-size:20px; z-index: 3;
        box-shadow:0 6px 18px rgba(0,0,0,0.4);
    ">❮</button>

    <button id="hero-next" style="
        position:absolute; top:50%; right:18px; transform:translateY(-50%);
        width:42px; height:42px;
        display:flex; align-items:center; justify-content:center;
        background:rgba(0,0,0,0.55); color:#fff; border:none;
        border-radius:50%; cursor:pointer; font-size:20px; z-index: 3;
        box-shadow:0 6px 18px rgba(0,0,0,0.4);
    ">❯</button>

    <div id="hero-dots" style="
        position:absolute; bottom:16px; left:50%; transform:translateX(-50%);
        text-align:center; z-index: 3;
    ">
      <span class="hero-dot" data-idx="0"
            style="height:10px;width:10px;margin:0 6px;
                   background:rgba(255,255,255,0.45);border-radius:50%;
                   display:inline-block;cursor:pointer;"></span>
      <span class="hero-dot" data-idx="1"
            style="height:10px;width:10px;margin:0 6px;
                   background:rgba(255,255,255,0.45);border-radius:50%;
                   display:inline-block;cursor:pointer;"></span>
      <span class="hero-dot" data-idx="2"
            style="height:10px;width:10px;margin:0 6px;
                   background:rgba(255,255,255,0.45);border-radius:50%;
                   display:inline-block;cursor:pointer;"></span>
    </div>
  </div>
</div>

<script>
if (!window.__heroCarouselV3) {{
  window.__heroCarouselV3 = true;

  const totalSlides = 3;
  let index = 0;

  const slides = document.getElementById("hero-slides");
  const prev = document.getElementById("hero-prev");
  const next = document.getElementById("hero-next");
  const dots = document.querySelectorAll("#hero-dots .hero-dot");
  const container = document.getElementById("hero-carousel");

  function update() {{
    if (!slides) return;
    slides.style.transform = "translateX(-" + (index * 33.3333) + "%)";
    if (dots && dots.length) {{
      dots.forEach((d, i) => {{
        d.style.background = i === index ? "#ffffff" : "rgba(255,255,255,0.45)";
      }});
    }}
  }}

  function go(delta) {{
    index = (index + delta + totalSlides) % totalSlides;
    update();
  }}

  function goTo(n) {{
    index = n;
    update();
  }}

  if (prev) prev.addEventListener("click", () => go(-1));
  if (next) next.addEventListener("click", () => go(1));
  if (dots && dots.length) {{
    dots.forEach(d => {{
      d.addEventListener("click", () => {{
        const n = parseInt(d.getAttribute("data-idx"));
        goTo(n);
      }});
    }});
  }}

  let timer = setInterval(() => go(1), 3500);
  if (container) {{
    container.addEventListener("mouseenter", () => clearInterval(timer));
    container.addEventListener("mouseleave", () => {{
      timer = setInterval(() => go(1), 3500);
    }});
  }}

  update();
}}
</script>
"""
    components.html(carousel_html, height=420, scrolling=False)

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Login", use_container_width=True):
                st.session_state["navbar_state"] = "login"
                st.rerun()
        with c2:
            if st.button("Register", use_container_width=True):
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

# DASHBOARD[USER]
def render_user_dashboard():
    st.header("🎤 Audio-Only Mock Interview")

    st.subheader("Camera Preview")
    cam = st.camera_input("Camera Preview", key="single_camera")
    if cam:
        # st.camera_input returns an UploadedFile-like object; display as image instead of video
        st.image(cam)

    career = st.selectbox(
        "Career Field",
        [
            "Software Engineering",
            "Data Structures",
            "Data Science",
            "Machine Learning",
            "Cyber Security",
            "Cloud Computing",
            "Database Administrator",
            "Data Analyst",
            "Web Development",
        ],
    )

    interview_type = st.selectbox(
        "Interview Type",
        ["HR", "Technical", "Behavioral"]
    )

    difficulty = st.selectbox(
        "Difficulty Level",
        ["Basic", "Intermediate", "Advanced"]
    )

    # NEW: extra inputs for user
    job_role = st.text_input(
        "Target role / position (optional)",
        placeholder="e.g., Backend Engineer at fintech startup"
    )
    custom_focus = st.text_area(
        "Custom focus (optional)",
        placeholder="e.g., Focus more on system design, REST APIs, and database transactions."
    )
    num_q = st.slider("Number of questions", 3, 10, 5)

    # Generate questions + expected answers
    if st.button("Start Interview", key="btn_start_interview"):
        question_prompt = f"""
You are an experienced interviewer for {career} candidates.

Generate exactly {num_q} {interview_type} interview questions for a candidate.

Target role/position (if provided): {job_role or "Not specified"}

Difficulty: {difficulty}
- If difficulty is Basic, focus on fundamentals and simple, direct questions.
- If difficulty is Intermediate, focus on applied concepts and moderate depth.
- If difficulty is Advanced, focus on complex, scenario-based and deep questions.

Additional focus (if provided): {custom_focus or "None"}

For each question:
- Write the question on one line starting with "Q:".
- On the next line, write a short expected answer (1–3 sentences) starting with "Expected answer:".
- Make sure the question and expected answer match the specified difficulty and interview type.
- Do not add numbering or bullets.
- Do not add any extra text before or after the Q/A pairs.

Example format:
Q: Tell me about yourself.
Expected answer: The candidate gives a concise summary of their background, skills, and goals.

Now generate {num_q} such Q/A pairs.
"""

        raw, err = prompt(question_prompt, mode="questions")
        if err:
            st.error(err)
            return

        if not isinstance(raw, str) or not raw.strip():
            st.error("Could not generate questions. Please check the AI service and try again.")
            return

        qa_pairs = []
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("Q:"):
                q = line.split(":", 1)[1].strip()
                exp = ""
                if i + 1 < len(lines) and lines[i + 1].startswith("Expected answer:"):
                    exp = lines[i + 1].split(":", 1)[1].strip()
                    i += 1
                qa_pairs.append({"question": q, "expected_answer": exp})
            i += 1

        qa_pairs = qa_pairs[:num_q]

        if len(qa_pairs) < num_q:
            st.error("Failed to generate valid questions. Retry.")
            st.write("DEBUG RAW QUESTIONS:", raw)
            return

        # store questions and placeholder for audio/transcripts
        for pair in qa_pairs:
            pair["audio_bytes"] = None
            pair["transcript"] = None  # placeholder if you later add ASR

        st.session_state["qa_pairs"] = qa_pairs
        st.session_state["questions_generated"] = [p["question"] for p in qa_pairs]

    # Render questions, audio, and build transcript lines
    qa_pairs = st.session_state.get("qa_pairs") or []
    transcript_lines = []
    audio_flags = []

    if qa_pairs:
        for i, pair in enumerate(qa_pairs, 1):
            q = pair["question"]
            exp = pair["expected_answer"]

            st.markdown(f"### Q{i}: {q}")

            with st.expander("View expected answer"):
                st.write(exp or "Expected answer not available.")

            audio = st.audio_input(
                f"Record Answer (Q{i})",
                key=f"audio_{i}"
            )

            transcript_lines.append(f"Q{i}: {q}")
            transcript_lines.append(f"Expected answer: {exp}")

            if audio:
                # st.audio_input returns an UploadedFile (file-like object) [web:11]
                audio_bytes = audio.read()
                pair["audio_bytes"] = audio_bytes
                st.audio(audio)
                transcript_lines.append("Candidate answer: [audio recorded]")
                audio_flags.append(True)
            else:
                transcript_lines.append("Candidate answer: [no answer]")
                audio_flags.append(False)

        # ---- Analyze interview ----
        if st.button("Analyze Interview", key="btn_analyze"):
            if not any(audio_flags):
                st.warning("Please record at least one audio answer.")
                return

            # Build a more contextual analysis prompt using Qs + answer availability
            qa_summary_lines = []
            for idx, pair in enumerate(qa_pairs, 1):
                answered = "provided" if audio_flags[idx - 1] else "not provided"
                qa_summary_lines.append(
                    f"Q{idx}: {pair['question']}\nCandidate answer: {answered}"
                )

            analysis_prompt = f"""
You are an expert interviewer.

Below is an audio-only mock interview session.
For each question, you see whether the candidate answered it or not.
You do NOT have the actual transcript, so base your evaluation on which questions were attempted,
their difficulty, and the interview context.

Interview context:
Career Field: {career}
Interview Type: {interview_type}
Difficulty Level: {difficulty}
Target Role: {job_role or "Not specified"}
Custom Focus: {custom_focus or "None"}

Questions and answer availability:
{chr(10).join(qa_summary_lines)}

Return a detailed, honest evaluation using explicit words like
"strong", "excellent", "good", "weak", "poor", "unclear", "lacking"
so that it can be scored automatically.

Format:
Strengths:
- ...

Weaknesses:
- ...

Improvement tips:
- ...
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

            # PDF content
            pdf_text_lines = []
            pdf_text_lines.append("Interview Report")
            pdf_text_lines.append("=" * 40)
            pdf_text_lines.append("")
            pdf_text_lines.append(f"Career Field: {career}")
            pdf_text_lines.append(f"Interview Type: {interview_type}")
            pdf_text_lines.append(f"Difficulty Level: {difficulty}")
            pdf_text_lines.append(f"Target Role: {job_role or 'Not specified'}")
            pdf_text_lines.append(f"Custom Focus: {custom_focus or 'None'}")
            pdf_text_lines.append("")

            for i, pair in enumerate(qa_pairs, 1):
                pdf_text_lines.append(f"Q{i}: {pair['question']}")
                pdf_text_lines.append(f"Expected answer: {pair['expected_answer']}")
                if audio_flags[i - 1]:
                    pdf_text_lines.append("Candidate answer: [audio recorded]")
                else:
                    pdf_text_lines.append("Candidate answer: [no answer]")
                pdf_text_lines.append("")

            pdf_text_lines.append("")
            pdf_text_lines.append("AI Analysis")
            pdf_text_lines.append("=" * 40)
            pdf_text_lines.append(analysis)

            full_text = "\n".join(pdf_text_lines)

            pdf = create_interview_pdf(full_text)

            st.download_button(
                "Download Interview Report (PDF)",
                pdf,
                "interview_report.pdf",
                "application/pdf"
            )

    if st.button("Logout"):
        reset_to_home()

# DASHBOARD[COMPANY]
import streamlit as st
# --- ONLY SHOWING UPDATED COMPANY DASHBOARD PART ---
# Replace your existing render_company_dashboard() with this

import re
import streamlit as st

def render_company_dashboard():
    st.header("Company Question Generator")

    topic = st.selectbox(
        "Topic",
        [
            "Python",
            "Data Structures",
            "System Design",
            "Data Science",
            "Cloud Computing",
            "Database Administrator",
            "Data Analyst",
            "Web Development",
        ],
    )

    level = st.radio("Difficulty", ["Basic", "Intermediate", "Advanced"], horizontal=True)

    q_type = st.selectbox(
        "Interview Round / Question Type",
        ["Behavioral", "HR", "Technical", "Coding Round"],
    )

    role_title = st.text_input("Role title", placeholder="e.g., Senior Data Engineer")

    extra_instr = st.text_area(
        "Additional instructions (optional)",
        placeholder="Focus on system design, APIs, etc.",
    )

    num_q_company = st.slider("Number of questions", 3, 15, 5)

    if st.button("Generate Questions"):

        # 🔥 STRONG PROMPT
        if q_type == "Coding Round":
            prompt_text = f"""
You MUST follow the format EXACTLY.

Generate exactly {num_q_company} coding interview Q/A pairs.

STRICT FORMAT:

Q: <question>
Demo answer:
<code or explanation + code>

Rules:
- ALWAYS include "Demo answer:"
- Code can be multi-line
- NO numbering
- NO extra text before/after
- DO NOT skip any pair

Topic: {topic}
Difficulty: {level}
Role: {role_title or "Not specified"}
Extra instructions: {extra_instr or "None"}
"""
        else:
            prompt_text = f"""
You MUST follow the format EXACTLY.

Generate exactly {num_q_company} interview Q/A pairs.

STRICT FORMAT:

Q: <question>
Demo answer: <answer>

Rules:
- Every question MUST start with "Q:"
- Every answer MUST start with "Demo answer:"
- NO numbering
- NO extra text before/after
- DO NOT skip any pair

Topic: {topic}
Difficulty: {level}
Role: {role_title or "Not specified"}
Round: {q_type}
Extra instructions: {extra_instr or "None"}
"""

        q_raw, err = prompt(prompt_text, mode="questions")

        if err:
            st.error(err)
            return

        if not isinstance(q_raw, str) or not q_raw.strip():
            st.error("Empty response from AI.")
            return

        # 🔍 DEBUG VIEW
        with st.expander("DEBUG raw LLM output"):
            st.text(q_raw)

        qa_pairs = []

        # ✅ PRIMARY PARSER (REGEX)
        pattern = r"Q:\s*(.*?)\n+Demo answer:\s*(.*?)(?=\n\s*Q:|\Z)"
        matches = re.findall(pattern, q_raw, re.DOTALL | re.IGNORECASE)

        for q, a in matches:
            qa_pairs.append({
                "question": q.strip(),
                "demo_answer": a.strip()
            })

        # 🔁 FALLBACK PARSER
        if len(qa_pairs) == 0:
            lines = q_raw.split("\n")
            current_q = None
            current_a = []
            in_demo = False

            for line in lines:
                clean = line.strip()

                if clean.startswith("Q:"):
                    if current_q:
                        qa_pairs.append({
                            "question": current_q,
                            "demo_answer": "\n".join(current_a).strip()
                        })
                    current_q = clean.split(":", 1)[1].strip()
                    current_a = []
                    in_demo = False

                elif clean.lower().startswith("demo answer"):
                    in_demo = True
                    current_a.append(clean.split(":", 1)[-1].strip())

                elif in_demo:
                    current_a.append(line)

            if current_q:
                qa_pairs.append({
                    "question": current_q,
                    "demo_answer": "\n".join(current_a).strip()
                })

        # 🧹 CLEAN INVALID
        qa_pairs = [
            p for p in qa_pairs
            if p["question"] and p["demo_answer"]
        ]

        qa_pairs = qa_pairs[:num_q_company]

        # ⚠️ SOFT WARNING INSTEAD OF FAIL
        if len(qa_pairs) < num_q_company:
            st.warning(
                f"Only {len(qa_pairs)} valid Q/A pairs parsed (requested {num_q_company})."
            )

        if len(qa_pairs) == 0:
            st.error("Could not parse any valid Q/A pairs.")
            return

        st.session_state["company_qa_pairs"] = qa_pairs

    # --- DISPLAY ---
    qa_pairs = st.session_state.get("company_qa_pairs") or []

    if qa_pairs:
        st.subheader("Generated Questions with Demo Answers")

        for i, pair in enumerate(qa_pairs, 1):
            st.markdown(f"### Q{i}: {pair['question']}")
            with st.expander("View demo answer"):
                st.markdown(pair["demo_answer"])

    if st.button("Logout"):
        reset_to_home()

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
