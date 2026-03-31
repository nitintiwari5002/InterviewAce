import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt

def create_interview_pdf(text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    safe_text = _sanitize_for_pdf(text)

    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin-1", "ignore")
    
from core.db import (
    create_tables,
    register_company,
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
            Build AI Powered Interview Questions and Sample Code By team Shaurya
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
    role = st.radio("Login as:", ["Company"], horizontal=True)
    st.session_state["role"] = role

    if role == "Company":
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
    role = st.radio("Register as:", ["Company"], horizontal=True)

    if role == "Company":
        c = st.text_input("Company Name")
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("Register"):
            register_company(c, e, p)
            st.success("Registered successfully")

    if st.button("Back"):
        reset_to_home()

# DASHBOARD[COMPANY]
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

    # Inputs specific to company
    role_title = st.text_input(
        "Role title",
        placeholder="e.g., Senior Data Engineer",
    )
    extra_instr = st.text_area(
        "Additional instructions for AI (optional)",
        placeholder="e.g., Focus more on distributed systems, Kafka, and data modelling.",
    )
    num_q_company = st.slider("Number of questions", 3, 15, 5, key="num_q_company")

    if st.button("Generate Questions"):
        # --- Prompt selection ---
        if q_type == "Coding Round":
            prompt_text = f"""
You are a senior {topic} interviewer at a top tech company.
Speak in a professional, concise, and realistic coding interview tone.

Design coding interview questions for a {role_title or "Not specified"} in a {q_type}.

Role/topic: {topic}
Difficulty: {level}

Extra instructions from company (if any): {extra_instr or "None"}

Generate exactly {num_q_company} interview question and answer pairs.

For each pair:
- First line: start with "Q:" then the coding question.
- Immediately after that, include a line starting with "Demo answer:" then provide DEMO CODE.
- The demo code can span multiple lines and may include triple backticks for code blocks.

Example format for ONE pair:
Q: Write a function to reverse a string.
Demo answer:
```python
def reverse_string(s: str) -> str:
    return s[::-1]
Hard rules:

Always include the line starting with "Demo answer:" for every question.

Do NOT add numbering or bullets.

Do NOT add any extra text before or after the Q/A pairs.
"""
        else:
            prompt_text = f"""
You are a senior {topic} interviewer at a top tech company.
Speak in a professional, concise, and realistic interview tone.

Design questions for a {q_type} round.
Role/topic: {topic}
Role title: {role_title or "Not specified"}
Difficulty: {level}

Extra instructions from company (if any): {extra_instr or "None"}

Generate exactly {num_q_company} interview question and answer pairs.

For each pair:

First line: start with "Q:" then the question.

Second line: start with "Demo answer:" then a strong but realistic candidate answer.

Answers should:

Sound like a real candidate speaking in first person ("I ...").

Be structured (2–5 sentences), with brief reasoning or an example.

Match the specified difficulty and round type:

HR / Behavioral: focus on situations, actions, and results (use STAR-like structure).

Technical: focus on concepts, trade-offs, and brief logic or code explanations.

Do NOT add numbering or bullets.

Do NOT add any extra text before or after the Q/A pairs.
"""

        # --- Call AI ---
        q_raw, err = prompt(prompt_text, mode="questions")
        if err:
            st.error(err)
        else:
            if not isinstance(q_raw, str) or not q_raw.strip():
                st.error("Could not generate questions. Please try again.")
            else:
                # Optional: debug view to inspect raw LLM output once
                with st.expander("DEBUG raw LLM output"):
                    st.text(q_raw)

                lines = [l for l in q_raw.split("\n")]
                qa_pairs = []

                current_q = None
                current_demo_lines = []
                in_demo = False

                # --- Robust parser: Q: + Demo answer: with multi-line code ---
                for raw_line in lines:
                    line = raw_line.strip()

                    # Preserve blank lines inside demo answers (code blocks)
                    if not line:
                        if in_demo:
                            current_demo_lines.append("")
                        continue

                    # Normalize leading bullets / numbering
                    clean_line = line.lstrip("-*0123456789. ").strip()

                    # New question
                    if clean_line.startswith("Q:"):
                        # flush previous
                        if current_q is not None:
                            demo_answer = "\n".join(current_demo_lines).strip()
                            qa_pairs.append(
                                {"question": current_q, "demo_answer": demo_answer}
                            )
                        parts = clean_line.split(":", 1)
                        if len(parts) > 1:
                            current_q = parts[1].strip()  # keep only the question text
                        else:
                            current_q = clean_line.strip()
                        current_demo_lines = []
                        in_demo = False
                        continue

                    # Start of demo answer
                    if clean_line.startswith("Demo answer:"):
                        in_demo = True
                        parts = clean_line.split("Demo answer:", 1)
                        after = parts[1].strip() if len(parts) > 1 else ""

                        current_demo_lines.append(after)
                        continue

                    # Lines inside demo answer (code, text, etc.)
                    if in_demo:
                        current_demo_lines.append(raw_line)

                # Flush last pair
                if current_q is not None:
                    demo_answer = "\n".join(current_demo_lines).strip()
                    qa_pairs.append(
                        {"question": current_q, "demo_answer": demo_answer}
                    )

                # Keep requested count
                qa_pairs = qa_pairs[:num_q_company]

                if len(qa_pairs) < num_q_company:
                    st.error(
                        "Failed to parse all Q/A pairs from the AI response. Please retry."
                    )
                else:
                    st.session_state["company_qa_pairs"] = qa_pairs

    # --- Display section ---
    qa_pairs = st.session_state.get("company_qa_pairs") or []

    if qa_pairs:
        st.subheader("Generated Questions with Demo Answers")

        for idx, pair in enumerate(qa_pairs, start=1):
            st.markdown(f"Q{idx}: {pair['question']}")
            with st.expander("View demo answer"):
                if pair["demo_answer"]:
                    # Render markdown/code blocks correctly
                    st.markdown(pair["demo_answer"], unsafe_allow_html=False)
                else:
                    st.write("No demo answer available.")

        # --- PDF build section ---
        pdf_lines = []
        pdf_lines.append("Company Question Set")
        pdf_lines.append("=" * 40)
        pdf_lines.append("")
        pdf_lines.append(f"Topic: {topic}")
        pdf_lines.append(f"Round: {q_type}")
        pdf_lines.append(f"Difficulty: {level}")
        pdf_lines.append(f"Role title: {role_title or 'Not specified'}")
        pdf_lines.append(f"Extra instructions: {extra_instr or 'None'}")
        pdf_lines.append("")

        for i, pair in enumerate(qa_pairs, 1):
            pdf_lines.append(f"Q{i}: {pair['question']}")
            pdf_lines.append("Demo answer:")
            pdf_lines.append(pair["demo_answer"])
            pdf_lines.append("")

        pdf_text = "\n".join(pdf_lines)

        pdf_bytes = create_interview_pdf(pdf_text)

        st.download_button(
            "Download Questions + Demo Answers (PDF)",
            data=pdf_bytes,
            file_name="company_questions_demo_answers.pdf",
            mime="application/pdf",
        )

    if st.button("Logout"):
        reset_to_home()

state = st.session_state["navbar_state"]

if state is None:
    render_welcome()
elif state == "login":
    render_login()
elif state == "register":
    render_register()
elif state == "company_dashboard":
    render_company_dashboard()
