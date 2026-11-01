import streamlit as st
import streamlit.components.v1 as components
import base64
import pickle
import uuid
import re
import html
from pathlib import Path
from fpdf import FPDF
from core.db import create_tables, register_user, login_user
from core.ai import prompt
from components.navbar import render_navbar
st.set_page_config(page_title="InterviewAce", page_icon="", layout="wide")
render_navbar("home")
# APP INITIALIZATION
create_tables()
# PERSISTENT INTERVIEW STATE
STATE_FILE = Path(__file__).resolve().parent / "interview_state.pkl"

SESSION_DEFAULTS = {
    "navbar_state": None,
    "role": None,
    "login_success": None,
    "username": None,
    "auth_token": None,
    "questions_generated": None,
    "qa_pairs": None,
    "analysis": None,
    "score": None,
    "current_question": 0,
    "interview_started": False,
    "interview_config": None,
}

def load_persistent_store():
    if not STATE_FILE.exists():
        return {"sessions": {}, "interviews": {}}
    try:
        with STATE_FILE.open("rb") as f:
            data = pickle.load(f)
        if not isinstance(data, dict):
            return {"sessions": {}, "interviews": {}}
        data.setdefault("sessions", {})
        data.setdefault("interviews", {})
        return data
    except Exception:
        return {"sessions": {}, "interviews": {}}

def save_persistent_store(data):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp_file = STATE_FILE.with_suffix(".tmp")
    with temp_file.open("wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    temp_file.replace(STATE_FILE)

def init_session():
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_auth_token_from_url():
    try:
        return st.query_params.get("session")
    except Exception:
        return None

def restore_persistent_session():
    token = get_auth_token_from_url()
    if not token:
        return

    store = load_persistent_store()
    session = store.get("sessions", {}).get(token)
    if not session:
        return

    username = session.get("username")
    if not username:
        return

    st.session_state.auth_token = token
    st.session_state.username = username
    st.session_state.navbar_state = "user_dashboard"

    saved = store.get("interviews", {}).get(username)
    if saved:
        for key in (
            "questions_generated",
            "qa_pairs",
            "analysis",
            "score",
            "current_question",
            "interview_started",
            "interview_config",
        ):
            if key in saved:
                st.session_state[key] = saved[key]

def persist_interview_state():
    username = st.session_state.get("username")
    if not username:
        return

    store = load_persistent_store()
    store.setdefault("interviews", {})
    store["interviews"][username] = {
        "questions_generated": st.session_state.get("questions_generated"),
        "qa_pairs": st.session_state.get("qa_pairs"),
        "analysis": st.session_state.get("analysis"),
        "score": st.session_state.get("score"),
        "current_question": st.session_state.get("current_question", 0),
        "interview_started": st.session_state.get("interview_started", False),
        "interview_config": st.session_state.get("interview_config"),
    }
    save_persistent_store(store)

def create_login_session(username):
    token = uuid.uuid4().hex
    store = load_persistent_store()
    store.setdefault("sessions", {})
    store["sessions"][token] = {"username": username}
    save_persistent_store(store)
    st.session_state.auth_token = token
    st.session_state.username = username
    st.query_params["session"] = token

def reset_to_home():
    # Do not delete the saved interview. It remains available on next login.
    for key, value in SESSION_DEFAULTS.items():
        st.session_state[key] = value
    try:
        st.query_params.clear()
    except Exception:
        pass
    st.rerun()

init_session()
restore_persistent_session()

# HELPERS
def img_to_data_url(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    data = p.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    mime = "image/jpeg" if p.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
    return f"data:{mime};base64,{b64}"

def sanitize_for_pdf(text: str) -> str:
    replacements = {
        "–": "-", "—": "-", "“": '"', "”": '"', "’": "'",
        "•": "-", "→": "->", "←": "<-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return "".join(ch if ord(ch) <= 255 else "?" for ch in text)

def create_interview_pdf(text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)
    for line in sanitize_for_pdf(text).splitlines():
        pdf.multi_cell(0, 7, line)
    return pdf.output(dest="S").encode("latin-1", "ignore")

def compute_score_from_analysis(analysis: str) -> int:
    if not isinstance(analysis, str) or not analysis.strip():
        return 0
    text = analysis.lower()
    score = 50
    positive = ["strong", "excellent", "good", "confident", "clear", "impressive", "well-structured", "outstanding", "solid"]
    negative = ["weak", "improve", "improvement", "poor", "unclear", "lack", "insufficient", "disorganized", "inconsistent"]
    score += sum(5 for word in positive if word in text)
    score -= sum(5 for word in negative if word in text)
    return max(0, min(100, score))

def get_score_breakdown(analysis: str) -> dict:
    text = (analysis or "").lower()
    return {
        "Strengths": 70 if any(x in text for x in ["strength", "strong", "good"]) else 40,
        "Weaknesses": 60 if any(x in text for x in ["weak", "improve", "lack"]) else 40,
        "Communication": 65 if any(x in text for x in ["communication", "clarity", "clear"]) else 40,
        "Technical Depth": 65 if any(x in text for x in ["technical", "concepts", "knowledge"]) else 40,
    }
# GLOBAL CLASSY THEME
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --ink: #172033;
    --muted: #667085;
    --cream: #f7f5f0;
    --paper: #ffffff;
    --navy: #182338;
    --gold: #c9a45c;
    --gold-light: #ead8ad;
    --line: #e7e2d8;
    --shadow: 0 18px 55px rgba(24,35,56,.10);
}

html, body, [class*="css"] {
    font-family: "DM Sans", sans-serif;
    color: var(--ink);
}
.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(201,164,92,.12), transparent 26%),
        radial-gradient(circle at 92% 12%, rgba(24,35,56,.08), transparent 25%),
        linear-gradient(180deg, #fbfaf7 0%, #f3f1eb 100%);
}
.block-container {
    width: min(97%, 1800px);
    max-width: 1800px;
    padding: 1.4rem 0 4.5rem 0;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { visibility: hidden; }

.topbar {
    padding: 1.05rem 1.4rem;
    border: 1px solid rgba(255,255,255,.7);
    border-radius: 20px;
    background: rgba(24,35,56,.96);
    box-shadow: 0 14px 35px rgba(24,35,56,.16);
    display:flex;
    align-items: center;
    justify-content:space-between;
    color:#fff;
    margin-bottom: 0.8rem;
}
.brand { font-weight:700; letter-spacing:.04em; font-size:1.15rem; }
.brand span { color:var(--gold-light); }
.eyebrow {
    text-transform:uppercase;
    letter-spacing:.18em;
    font-size:.80rem;
    font-weight:700;
    color:var(--gold);
}
.hero {
    padding: 3.8rem 2rem 3.2rem;
    border-radius: 30px;
    background:
        linear-gradient(135deg, rgba(24,35,56,.98), rgba(34,47,72,.96)),
        radial-gradient(circle at 80% 20%, rgba(201,164,92,.25), transparent 35%);
    color:#fff;
    box-shadow: var(--shadow);
    text-align:center;
    overflow:hidden;
    position:relative;
}
.hero:after {
    content:"";
    position:absolute;
    width:220px;height:220px;
    right:-70px;top:-70px;
    border:1px solid rgba(234,216,173,.35);
    border-radius:50%;
}
.hero h1 {
    font-family:"Playfair Display",serif;
    font-size:clamp(2.5rem,6vw,4.6rem);
    line-height:1.05;
    margin:.45rem 0 1rem;
    color:#fff;
}
.hero p { max-width:900px; margin:auto; color:#f4f6fa !important; font-size:1.08rem; line-height:1.8; }
.hero .eyebrow { display:inline-flex; align-items:center; justify-content:center; padding:.62rem 1.05rem; margin:0 auto .8rem; border-radius:999px; background:#f0d99f; color:#172238 !important; border:1px solid #fff0c9; font-size:.78rem; font-weight:900; letter-spacing:.12em; box-shadow:0 7px 20px rgba(0,0,0,.18); text-shadow:none; }

.card {
    background:rgba(255,255,255,.88);
    border:1px solid rgba(231,226,216,.9);
    border-radius:24px;
    padding:1.7rem;
    box-shadow:0 12px 35px rgba(24,35,56,.07);
    color:#172033;
}

/* Light-blue typography for the Performance Review content. */
.st-key-analysis-review {
    background:rgba(255,255,255,.96);
    border:1px solid rgba(231,226,216,.9);
    border-radius:24px;
    padding:1rem 1.7rem;
    box-shadow:0 12px 35px rgba(24,35,56,.07);
    color:#5B9BD5 !important;
}

.st-key-analysis-review,
.st-key-analysis-review [data-testid="stMarkdownContainer"],
.st-key-analysis-review [data-testid="stMarkdownContainer"] * {
    color: #5B9BD5 !important;
    -webkit-text-fill-color: #5B9BD5 !important;
    opacity: 1 !important;
}

.st-key-analysis-review p,
.st-key-analysis-review li {
    color: #5B9BD5 !important;
    -webkit-text-fill-color: #5B9BD5 !important;
    font-size: 16px !important;
    line-height: 1.8 !important;
}

.st-key-analysis-review strong,
.st-key-analysis-review b,
.st-key-analysis-review h1,
.st-key-analysis-review h2,
.st-key-analysis-review h3,
.st-key-analysis-review h4 {
    color: #3182CE !important;
    -webkit-text-fill-color: #3182CE !important;
    font-weight: 700 !important;
}

.st-key-analysis-review ul,
.st-key-analysis-review ol {
    padding-left: 24px !important;
    margin-bottom: 12px !important;
}
.section-title {
    font-family:"Playfair Display",serif;
    font-size:1.65rem;
    color:var(--navy);
    margin:0 0 .45rem;
}
.muted { color:var(--muted); line-height:1.7; }
.badge {
    display:inline-block;
    padding:.45rem .8rem;
    margin:.25rem;
    border:1px solid #e6d8b9;
    border-radius:999px;
    background:#fbf7ed;
    color:#6e5730;
    font-size:.82rem;
    font-weight:600;
}
.feature-strip {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:1rem;
    margin:1.4rem 0;
}
.feature-mini {
    background:#fff;
    border:1px solid var(--line);
    border-radius:20px;
    padding:1.25rem;
    box-shadow:0 10px 30px rgba(24,35,56,.06);
}
.feature-mini strong { display:block; margin-bottom:.35rem; color:var(--navy); }
.feature-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; margin:1.2rem 0 1.6rem; }
.feature-card { background:rgba(255,255,255,.92); border:1px solid var(--line); border-radius:22px; padding:1.5rem; min-height:155px; box-shadow:0 12px 30px rgba(24,35,56,.06); }
.feature-card .feature-icon {font-size:1.55rem;margin-bottom:.55rem}
.feature-card h3 {margin:0 0 .4rem;color:var(--navy);font-size:1.08rem}
.feature-card p {margin:0;color:var(--muted);line-height:1.65}
.info-panel {background:#fff;border:1px solid var(--line);border-radius:22px;padding:1.5rem 1.7rem;margin:1rem 0;box-shadow:0 10px 28px rgba(24,35,56,.05)}
.info-panel h3 {font-family:"Playfair Display",serif;color:var(--navy);margin-top:0}
.info-panel li {color:var(--muted);margin:.45rem 0;line-height:1.6}

.feature-mini span { color:var(--muted); font-size:.9rem; line-height:1.5; }

.stButton > button, .stDownloadButton > button {
    border-radius:12px !important;
    min-height:44px;
    font-weight:700 !important;
    border:1px solid #c9a45c !important;
    background:linear-gradient(135deg,#c9a45c,#dfc485) !important;
    color:#182338 !important;
    box-shadow:0 8px 22px rgba(201,164,92,.18) !important;
    transition:transform .2s ease, box-shadow .2s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform:translateY(-2px);
    box-shadow:0 12px 28px rgba(201,164,92,.28) !important;
}
input, textarea, [data-baseweb="select"] > div {
    border-radius:12px !important;
}
[data-testid="stMetric"] {
    background:#fff;
    border:1px solid var(--line);
    border-radius:18px;
    padding:1rem;
}
hr { border-color:var(--line) !important; }
[data-testid="stAlert"] p { color: #000000 !important; }
@media (max-width: 800px) {
    .feature-strip { grid-template-columns:1fr; }
    .hero { padding:2.7rem 1rem; }
}

/* Premium full-width 3D visual refresh */
.block-container{width:min(97%,1800px)!important;max-width:1800px!important;padding-left:0!important;padding-right:0!important}
html,body,[class*="css"],.stApp{color:#172033!important}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{color:#263244}
.feature-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:1.35rem;margin:1.6rem 0 2rem}
.feature-card{background:#fff;border:1px solid #ded8ca;border-radius:24px;padding:1.8rem;min-height:180px;box-shadow:0 14px 32px rgba(24,35,56,.10);transition:transform .28s ease,box-shadow .28s ease,border-color .28s ease}
.feature-card:hover{transform:translateY(-10px) scale(1.015);box-shadow:0 26px 48px rgba(24,35,56,.20);border-color:#c9a45c}
.feature-card .feature-icon{font-size:2.1rem;margin-bottom:.8rem;display:block}
.feature-card h3{margin:0 0 .55rem;color:#050505!important;font-size:1.12rem;font-weight:900!important}
.feature-card p{margin:0;color:#263244!important;line-height:1.7}
.feature-mini{transition:transform .25s ease,box-shadow .25s ease}
.feature-mini:hover{transform:translateY(-8px);box-shadow:0 24px 42px rgba(24,35,56,.17)}
.feature-mini strong{color:#050505!important;font-weight:900!important}
.info-panel{transition:transform .25s ease,box-shadow .25s ease}
.info-panel:hover{transform:translateY(-5px);box-shadow:0 22px 42px rgba(24,35,56,.14)}
.section-title,.info-panel h3{color:#101828!important;font-weight:850!important}
.hero{padding:5rem 3rem 4.3rem;border-radius:34px;box-shadow:0 28px 70px rgba(24,35,56,.22)}
.hero p{max-width:1000px;color:#f4f6fa!important}
[data-testid="stVideo"]{width:100%!important;border-radius:24px;overflow:hidden;box-shadow:0 22px 52px rgba(24,35,56,.18);margin:24px auto 34px}
.stButton>button,.stDownloadButton>button{transition:all .25s ease!important}
.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-4px) scale(1.02)!important;box-shadow:0 18px 34px rgba(201,164,92,.32)!important}
@media(max-width:950px){.feature-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:650px){.feature-grid{grid-template-columns:1fr}.block-container{width:94%!important}.hero{padding:3rem 1.2rem}}

</style>
""", unsafe_allow_html=True)

header_left, header_login, header_register = st.columns([6, 1.5, 1.5], vertical_alignment="center")
with header_left:
    st.markdown('<div class="topbar"><div class="brand">Interview<span>Ace</span></div><div class="eyebrow">AI Powered Interview Prep Studio</div></div>', unsafe_allow_html=True)
with header_login:
    if st.button("Login", key="header_login", use_container_width=True):
        st.session_state.navbar_state = "login"
        st.rerun()
with header_register:
    if st.button("Register", key="header_register", use_container_width=True):
        st.session_state.navbar_state = "register"
        st.rerun()

# -----------------------------
# WELCOME
# -----------------------------
def render_welcome():
    st.markdown("""
    <section class="hero">
        <div class="eyebrow">Prepare smarter · perform better</div>
        <h1>Own Your Next Interview.</h1>
        <p>Practice AI-powered mock interviews, receive focused feedback, and build the confidence to walk into your next interview prepared.</p>
    </section>
    """, unsafe_allow_html=True)

    video_path = Path(__file__).resolve().parent.parent/"assets"/"interviewace.mp4"
    if video_path.exists():
        st.video(str(video_path))
    else:
        st.warning("Homepage video not found. Please place interviewace.mp4 inside the assets folder.")

    st.markdown("""
    <div class="feature-strip">
      <div class="feature-mini"><strong>01 · Adaptive Questions</strong><span>Generate questions around your career field, interview type, difficulty, role, and custom focus.</span></div>
      <div class="feature-mini"><strong>02 · Practice Naturally</strong><span>Use audio responses to simulate a realistic interview environment.</span></div>
      <div class="feature-mini"><strong>03 · Actionable Feedback</strong><span>Review an AI-generated evaluation and download a polished interview report.</span></div>
    </div>
    <h2 class="section-title" style="margin-top:2rem;">Core capabilities</h2>
    <div class="feature-grid">
      <div class="feature-card"><div class="feature-icon">🤖</div><h3>AI-powered Interviews</h3><p>Practice with intelligent, adaptive mock interviews and detailed feedback.</p></div>
      <div class="feature-card"><div class="feature-icon">📊</div><h3>Real-time Analytics</h3><p>Track your performance and pinpoint areas for improvement instantly.</p></div>
      <div class="feature-card"><div class="feature-icon">🏢</div><h3>Code environment</h3><p>User-friendly interface for coding practice and interview preparation.</p></div>
      <div class="feature-card"><div class="feature-icon">💡</div><h3>AI Feedback</h3><p>Receive customized AI feedback based on the interview and identify areas to improve.</p></div>
      <div class="feature-card"><div class="feature-icon">📄</div><h3>Resume Builder via AI</h3><p>Create professional resumes with AI assistance to highlight your strengths effectively.</p></div>
      <div class="feature-card"><div class="feature-icon">🔎</div><h3>Resume Checker</h3><p>Analyze and improve your resume with AI-driven insights.</p></div>
    </div>
    <div class="info-panel">
      <h3>For Candidates</h3>
      <ul>
        <li>AI-generated interview questions tailored to role and level.</li>
        <li>Answer boxes for each question with detailed AI feedback.</li>
        <li>Overall score and category-wise breakdown: strengths, weaknesses, communication, and technical depth.</li>
        <li>Downloadable PDF report of your analysis.</li>
      </ul>
    </div>
    <div class="info-panel">
      <h3>Technology Stack</h3>
      <ul>
        <li>Streamlit for fast, interactive UI.</li>
        <li>SQLite for lightweight authentication and data.</li>
        <li>Groq / OSS-120B for AI generation and analysis.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)


# LOGIN / REGISTER
def render_login():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Welcome back</div><div class="section-title">Sign in to InterviewAce</div><p class="muted">Continue your interview preparation journey.</p>', unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Login", use_container_width=True):
            if login_user(u, p):
                create_login_session(u)
                st.session_state.navbar_state = "user_dashboard"
                st.rerun()
            else:
                st.error("Invalid credentials.")
    with c2:
        if st.button("Back", use_container_width=True):
            reset_to_home()
    st.markdown('</div>', unsafe_allow_html=True)

def render_register():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Create your account</div><div class="section-title">Start preparing with InterviewAce</div><p class="muted">Create an account to access your personalized interview workspace.</p>', unsafe_allow_html=True)
    u = st.text_input("Username")
    e = st.text_input("Email")
    p = st.text_input("Password", type="password")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Create Account", use_container_width=True):
            try:
                register_user(u, e, p)
                st.success("Registered successfully. You can now log in.")
            except Exception as exc:
                st.error(f"Registration failed: {exc}")
    with c2:
        if st.button("Back", use_container_width=True):
            reset_to_home()
    st.markdown('</div>', unsafe_allow_html=True)

# USER DASHBOARD
def render_user_dashboard():
    st.markdown("""
    <div class="hero" style="text-align:left;padding:2.2rem 2rem;">
      <div class="eyebrow">Interview workspace</div>
      <h1 style="font-size:2.6rem;margin-bottom:.6rem;">Your Mock Interview</h1>
      <p style="margin:0;max-width:720px;">Set your interview parameters, generate tailored questions, record answers, and receive a focused performance review.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Interview Setup</div>', unsafe_allow_html=True)

        saved_config = st.session_state.get("interview_config") or {}

        if st.session_state.get("qa_pairs") and st.session_state.get("interview_started"):
            current = st.session_state.get("current_question", 0) + 1
            total = len(st.session_state.get("qa_pairs") or [])
            st.info(
                f"Interview in progress — question {current} of {total}. "
                "Refreshing the page will not reset your interview."
            )


        career_options = [
            "Software Engineering", "Data Structures", "Data Science",
            "Machine Learning", "Cyber Security", "Cloud Computing",
            "Database Administrator", "Data Analyst", "Web Development",
        ]
        interview_type_options = ["HR", "Technical", "Behavioral", "Coding"]
        difficulty_options = ["Basic", "Intermediate", "Advanced"]

        saved_career = saved_config.get("career", career_options[0])
        saved_type = saved_config.get("interview_type", interview_type_options[0])
        saved_difficulty = saved_config.get("difficulty", difficulty_options[0])
        saved_num_q = max(3, min(10, int(saved_config.get("num_q", 5))))

        career = st.selectbox(
            "Career Field",
            career_options,
            index=career_options.index(saved_career) if saved_career in career_options else 0,
            key="career_field",
        )
        interview_type = st.selectbox(
            "Interview Type",
            interview_type_options,
            index=interview_type_options.index(saved_type) if saved_type in interview_type_options else 0,
            key="interview_type",
        )
        difficulty = st.selectbox(
            "Difficulty Level",
            difficulty_options,
            index=difficulty_options.index(saved_difficulty) if saved_difficulty in difficulty_options else 0,
            key="difficulty_level",
        )
        job_role = st.text_input(
            "Target role / position (optional)",
            value=saved_config.get("job_role", ""),
            placeholder="e.g. Backend Engineer",
            key="job_role",
        )
        custom_focus = st.text_area(
            "Custom focus (optional)",
            value=saved_config.get("custom_focus", ""),
            placeholder="e.g. system design, REST APIs, database transactions",
            key="custom_focus",
        )
        num_q = st.slider(
            "Number of questions", 3, 10, saved_num_q, key="num_questions"
        )

        if st.button("Start Interview", key="btn_start_interview", use_container_width=True):
            question_prompt = f"""
You are an experienced interviewer for {career} candidates.

Generate exactly {num_q} {interview_type} interview questions.

Target role/position: {job_role or "Not specified"}
Difficulty: {difficulty}
Additional focus: {custom_focus or "None"}

If Basic, focus on fundamentals and simple direct questions.
If Intermediate, focus on applied concepts and moderate depth.
If Advanced, focus on complex scenario-based and deep questions.

For a Coding round, ask practical programming problems appropriate to the career field
and target role. Include constraints or sample input/output when useful. The expected
answer should include a correct solution approach and code in a suitable language.
For HR, Technical, and Behavioral rounds, provide a concise model answer.

Output format:
- Start every question with "Q:" on its own line.
- Follow it with "Expected answer:" and the model answer.
- The expected answer may span multiple lines.
- Do not include numbering or unrelated commentary.
- Output plain text only; do not use HTML tags, Markdown tables, or wrapper tags.
- Keep each question on one line immediately after the Q: label.
- Do not place questions inside code blocks.

Now generate exactly {num_q} question-and-expected-answer pairs.
"""
            # Coding questions and model solutions can be lengthy, so request a
            # larger completion to reduce the chance of truncated output.
            token_limit = 4096 if interview_type == "Coding" else 2048
            raw, err = prompt(
                question_prompt,
                mode="questions",
                max_new_tokens=token_limit,
            )
            if err:
                st.error(err)
                return
            if not isinstance(raw, str) or not raw.strip():
                st.error("Could not generate questions. Please try again.")
                return

            def clean_question_text(value: str) -> str:
                """Remove accidental HTML wrappers from question text only."""
                value = html.unescape(value or "")
                value = re.sub(
                    r"</?(?:div|p|span|strong|em|br|h[1-6])\b[^>]*>",
                    " ", value, flags=re.IGNORECASE
                )
                return re.sub(r"\s+", " ", value).strip(" \t\r\n:-")

            # Accept Q: and Question 1: labels, but do not treat numbered
            # solution steps (1., 2.) as new questions.
            question_start = re.compile(
                r"^\s*(?:Q\s*[:.)-]|Question\s*\d*\s*[:.)-])\s*(.*?)\s*$",
                re.IGNORECASE,
            )
            lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
            qa_pairs = []
            current_question = None
            expected_lines = []
            collecting_answer = False

            def save_current_pair():
                if current_question:
                    qa_pairs.append({
                        "question": current_question,
                        "expected_answer": "\n".join(expected_lines).strip(),
                        "audio_bytes": None,
                        "code_answer": "",
                    })

            for raw_line in lines:
                line = raw_line.strip()
                if not line:
                    if collecting_answer:
                        expected_lines.append("")
                    continue

                match = question_start.match(line)
                if match:
                    save_current_pair()
                    current_question = clean_question_text(match.group(1))
                    expected_lines = []
                    collecting_answer = False
                    continue

                if current_question is None:
                    continue

                if not collecting_answer and re.match(r"^Expected\s+answer\s*:", line, re.IGNORECASE):
                    collecting_answer = True
                    answer_first_line = re.sub(
                        r"^Expected\s+answer\s*:", "", line,
                        count=1, flags=re.IGNORECASE
                    ).strip()
                    if answer_first_line:
                        expected_lines.append(answer_first_line)
                    continue

                # Keep multiline explanations, sample I/O, and code intact.
                collecting_answer = True
                expected_lines.append(raw_line)

            save_current_pair()
            qa_pairs = [
                pair for pair in qa_pairs
                if pair["question"] and pair["expected_answer"].strip()
            ][:num_q]

            if len(qa_pairs) < num_q:
                st.error(
                    f"The AI returned {len(qa_pairs)} complete question(s), but "
                    f"{num_q} were requested. Please retry, or choose fewer questions."
                )
                with st.expander("View AI response for troubleshooting"):
                    st.text(raw[:12000])
                return

            st.session_state.qa_pairs = qa_pairs
            st.session_state.questions_generated = [p["question"] for p in qa_pairs]
            st.session_state.current_question = 0
            st.session_state.interview_started = True
            st.session_state.analysis = None
            st.session_state.score = None
            st.session_state.interview_config = {
                "career": career,
                "interview_type": interview_type,
                "difficulty": difficulty,
                "job_role": job_role,
                "custom_focus": custom_focus,
                "num_q": num_q,
            }
            persist_interview_state()
            st.success(f"{len(qa_pairs)} questions generated. Your interview has started.")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Camera Preview</div>', unsafe_allow_html=True)
        cam = st.camera_input("Camera Preview", key="single_camera")
        if cam:
            st.image(cam, use_container_width=True)
        else:
            st.markdown('<p class="muted">Camera preview is optional. Your interview can still be completed using audio responses.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    qa_pairs = st.session_state.get("qa_pairs") or []

    if qa_pairs and st.session_state.get("interview_started"):
        st.write("")
        st.markdown('<div class="section-title">Live Interview</div>', unsafe_allow_html=True)

        current_index = int(st.session_state.get("current_question", 0))
        current_index = max(0, min(current_index, len(qa_pairs) - 1))
        st.session_state.current_question = current_index
        pair = qa_pairs[current_index]

        st.progress((current_index + 1) / len(qa_pairs))

        # Escape AI-generated text before embedding it in HTML so stray tags
        # such as </div> cannot break the question card.
        safe_question = html.escape(str(pair.get("question", "")))
        st.markdown(
            f"""<div class="card" style="margin-bottom:18px;">
                <div class="eyebrow">Question {current_index + 1} of {len(qa_pairs)}</div>
                <div style="font-size:1.35rem;font-weight:700;color:#182338;line-height:1.6;margin-top:12px;">
                    {safe_question}
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

        interview_config = st.session_state.get("interview_config") or {}
        is_coding_round = interview_config.get("interview_type") == "Coding"

        if is_coding_round:
            st.caption("Write your solution in the code editor below. You can use any programming language.")
            code_answer = st.text_area(
                "Your code",
                value=pair.get("code_answer", ""),
                height=280,
                key=f"code_answer_{current_index}",
                placeholder="def solution(...):\\n    # Write your solution here\\n    pass",
            )
            if code_answer != pair.get("code_answer", ""):
                pair["code_answer"] = code_answer
                persist_interview_state()
            if code_answer.strip():
                st.success("Code answer saved. You can continue to the next question.")
        else:
            existing_audio = pair.get("audio_bytes")
            if existing_audio:
                st.success("Your recorded answer is saved. You can re-record it below if needed.")
                st.audio(existing_audio, format="audio/wav")

            audio = st.audio_input(
                "Record your answer",
                key=f"audio_{current_index}",
            )
            if audio:
                audio_bytes = audio.getvalue()
                if audio_bytes:
                    pair["audio_bytes"] = audio_bytes
                    persist_interview_state()
                    st.audio(audio_bytes, format="audio/wav")
                    st.success("Answer saved. You can continue to the next question.")

        with st.expander("View expected answer / solution"):
            st.markdown(pair.get("expected_answer") or "No expected answer was generated.")

        nav_left, nav_right = st.columns([1, 1])

        with nav_left:
            if current_index > 0:
                if st.button(
                    "← Previous Question",
                    key=f"previous_{current_index}",
                    use_container_width=True,
                ):
                    st.session_state.current_question -= 1
                    persist_interview_state()
                    st.rerun()

        with nav_right:
            if current_index < len(qa_pairs) - 1:
                if st.button(
                    "Next Question →",
                    key=f"next_{current_index}",
                    use_container_width=True,
                ):
                    answer_saved = bool(
                        pair.get("code_answer", "").strip()
                        if is_coding_round
                        else pair.get("audio_bytes")
                    )
                    if not answer_saved:
                        st.warning("Please enter your code before continuing." if is_coding_round
                                   else "Please record your answer before continuing.")
                    else:
                        st.session_state.current_question += 1
                        persist_interview_state()
                        st.rerun()
            else:
                if st.button(
                    "Submit Interview & Analyze",
                    key="btn_analyze",
                    use_container_width=True,
                ):

                    interview_config = st.session_state.get("interview_config") or {}
                    is_coding_round = interview_config.get("interview_type") == "Coding"

                    def answer_exists(item):
                        return bool(
                            item.get("code_answer", "").strip()
                            if is_coding_round else item.get("audio_bytes")
                        )

                    if not answer_exists(pair):
                        st.warning("Please enter your code before submitting." if is_coding_round
                                   else "Please record your answer before submitting.")
                    elif not all(answer_exists(item) for item in qa_pairs):
                        answered = sum(1 for item in qa_pairs if answer_exists(item))
                        st.warning(
                            f"Please answer every question before submitting. "
                            f"{answered}/{len(qa_pairs)} completed."
                        )
                    else:
                        persist_interview_state()
                        qa_summary = []
                        for idx, item in enumerate(qa_pairs, 1):
                            candidate_answer = (
                                item.get("code_answer", "").strip()
                                if is_coding_round
                                else "Audio answer recorded; transcript is not available."
                            )
                            qa_summary.append(
                                f"Q{idx}: {item['question']}\\n"
                                f"Expected answer / solution: {item.get('expected_answer', '')}\\n"
                                f"Candidate answer: {candidate_answer}"
                            )

                        analysis_prompt = f"""
                        You are an expert interviewer evaluating a mock interview.

                        Career Field: {career}
                        Interview Type: {interview_type}
                        Difficulty Level: {difficulty}
                        Target Role: {job_role or "Not specified"}
                        Custom Focus: {custom_focus or "None"}

                        Questions, model answers, and candidate answers:
                        {chr(10).join(qa_summary)}

                        For a Coding round, evaluate submitted code for correctness, approach,
                        edge cases, readability, and complexity. Do not claim the code was executed.
                        For non-coding rounds, audio answers are recorded but transcripts are not
                        available, so do not invent what the candidate said. Evaluate honestly
                        using the expected answers, question difficulty, interview context, and
                        the fact that each question was attempted.

                        Use this format:
                        Strengths:
                        - ...

                        Weaknesses:
                        - ...

                        Improvement tips:
                        - ...

                        Use explicit words such as strong, excellent, good, weak, poor, unclear,
                        or lacking where appropriate.
"""

                        with st.spinner("Analyzing your interview..."):
                            analysis, err = prompt(
                                analysis_prompt,
                                mode="analysis",
                            )

                        if err:
                            st.error(f"Analysis failed: {err}")
                        elif not isinstance(analysis, str) or not analysis.strip():
                            st.error(
                                "The AI returned an empty analysis. "
                                "Please try submitting again."
                            )
                        else:
                            score = compute_score_from_analysis(analysis)
                            st.session_state.analysis = analysis
                            st.session_state.score = score
                            st.session_state.interview_started = False
                            persist_interview_state()
                            st.success("Interview completed successfully!")
                            st.rerun()

        # Persist the state on normal reruns too.
        persist_interview_state()

    if st.session_state.get("analysis"):
        st.write("")
        st.markdown('<div class="section-title">Performance Review</div>', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("Overall Score", f'{st.session_state.score}/100')
            st.progress(st.session_state.score / 100)
        with c2:
            breakdown = get_score_breakdown(st.session_state.analysis)
            bcols = st.columns(4)
            for idx, (label, value) in enumerate(breakdown.items()):
                with bcols[idx]:
                    st.metric(label, value)

        with st.container(key="analysis-review"):
            st.markdown(st.session_state.analysis)

        completed_pairs = st.session_state.get("qa_pairs") or []
        if completed_pairs:
            st.markdown('<div class="section-title">Questions & Expected Answers</div>', unsafe_allow_html=True)
            for idx, item in enumerate(completed_pairs, 1):
                with st.expander(f"Question {idx}: {item.get('question', '')}"):
                    st.markdown("**Expected answer / solution**")
                    st.markdown(item.get("expected_answer") or "No expected answer was generated.")
                    if (st.session_state.get("interview_config") or {}).get("interview_type") == "Coding":
                        st.markdown("**Your submitted code**")
                        st.code(item.get("code_answer", "") or "No code submitted.")

        report_qa = []
        for idx, item in enumerate(completed_pairs, 1):
            report_qa.append(
                f"Question {idx}: {item.get('question', '')}\\n"
                f"Expected answer / solution: {item.get('expected_answer', '')}\\n"
                f"Your code: {item.get('code_answer', '')}"
            )

        pdf_lines = [
            "InterviewAce - Interview Report",
            "=" * 42,
            "",
            f"Overall Score: {st.session_state.score}/100",
            "",
            st.session_state.analysis,
            "",
            "Questions and Expected Answers",
            "=" * 42,
            "",
            "\\n\\n".join(report_qa),
        ]
        pdf = create_interview_pdf("\n".join(pdf_lines))
        st.download_button("Download Interview Report (PDF)", pdf, "interview_report.pdf", "application/pdf")

    if st.button("Logout", key="logout_bottom"):
        reset_to_home()
# ROUTER
state = st.session_state.navbar_state
if state is None:
    render_welcome()
elif state == "login":
    render_login()
elif state == "register":
    render_register()
elif state == "user_dashboard":
    render_user_dashboard()
else:
    reset_to_home()
