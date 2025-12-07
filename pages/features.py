import streamlit as st

st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f2027 0%, #2c5364 33%, #6a3093 66%, #ffeb70 100%);
        min-height: 100vh;
    }
    .full-navbar {
        width: 100vw !important;
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        background: linear-gradient(90deg, #0f2027 0%, #6a3093 50%, #ffeb70 100%);
        height: 76px;
        box-shadow: 0 12px 40px rgba(44,83,100,0.18);
        border-bottom-left-radius: 30px;
        border-bottom-right-radius: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        font-size: 2.25rem;
        color: #fff;
        letter-spacing: 2px;
        position: sticky;
        top: 0;
        z-index: 999;
        text-shadow: 0 2px 6px #0f2027;
    }
    .feature-box {
        background: linear-gradient(135deg, #2c5364 0%, #6a3093 65%, #ffeb70 100%);
        padding: 32px;
        margin: 12px;
        border-radius: 30px;
        font-size: 1.30rem;
        color: lightyellow;
        box-shadow: 0 8px 24px rgba(44,83,100,0.15);
        transition: transform .35s, box-shadow .35s;
        cursor: pointer;
        border: none;
        text-align: center;
    }
    .feature-box:hover {
        background: linear-gradient(135deg, #ffeb70 0%, #6a3093 75%, #0f2027 100%);
        transform: translateY(-12px) scale(1.06);
        box-shadow: 0 16px 60px rgba(44,83,100,0.17);
    }
    h1, h2, h4 {
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        text-shadow: 0 2px 4px #2c5364;
    }
    h1 {
        color: #6a3093;
        font-size: 2.35rem;
        margin-bottom: 16px;
    }
    h4 {
        color: #ffeb70;
        margin-bottom: 7px;
    }
    </style>
    <div class='full-navbar'>InterviewAce</div>
""", unsafe_allow_html=True)

# --- Logo ---
st.image("assets/Mini (2).png", width=250)

# --- Features Section ---
st.markdown("<h1 style='text-align:center; margin-top:20px;'>Everything You Need to Succeed</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Our AI-powered platform provides comprehensive interview preparation tailored for engineering students.</h4>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "<div class='feature-box'><h3>AI-powered Interviews</h3>Practice with intelligent, adaptive mock interviews and detailed feedback.</div>", 
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<div class='feature-box'><h3>Real-time Analytics</h3>Track your performance and pinpoint areas for improvement instantly.</div>", 
        unsafe_allow_html=True
    )

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.markdown(
        "<div class='feature-box'><h3>Company Questions generator</h3>Company can generate its questions for the Interview and saves his time.</div>", 
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        "<div class='feature-box'><h3>AI Feedback</h3>Receive customized AI feedback based on the User Interview and helps improve his/her skills.</div>", 
        unsafe_allow_html=True
    )
st.markdown("---")

col5, col6 = st.columns(2)

with col5:
    st.markdown(
        "<div class='feature-box'><h3>Resume Builder via AI</h3>Create professional resumes with AI assistance to highlight your strengths effectively.</div>", 
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        "<div class='feature-box'><h3>Resume Checker</h3>Analyze and improve your resume with AI-driven insights.</div>", 
        unsafe_allow_html=True
    )

st.markdown("---")

st.subheader("For Candidates")
st.markdown(
    """
- AI-generated interview questions tailored to role and level.
- Answer boxes for each question with detailed AI feedback.
- Overall score and category-wise breakdown (Strengths, Weaknesses, Communication, Technical Depth).
- Downloadable PDF report of your analysis.
"""
)

st.subheader("For Companies")
st.markdown(
    """
- Generate consistent interview question sets for specific roles.
- Quickly evaluate candidate responses with AI suggestions.
- Use scores and analysis to guide your hiring decisions.
"""
)

st.subheader("Technology Stack")
st.markdown(
    """
- Streamlit for fast, interactive UI.
- SQLite for lightweight authentication & data.
- Ollama (phi3:mini by default) for local AI generation and analysis.
"""
)