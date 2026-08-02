import streamlit as st
from core.theme import get_complete_theme, get_glass_navbar

st.markdown(get_complete_theme(), unsafe_allow_html=True)
st.markdown(get_glass_navbar(), unsafe_allow_html=True)

# --- Logo ---
left, center, right = st.columns([2, 2, 1])
with center:
    st.image("assets/Mini (2).png", width=250)

# --- Features Section ---
st.markdown("<div class='hero'><h1>Everything You Need to Succeed</h1><p>Our AI-powered platform provides comprehensive interview preparation tailored for engineering students</p></div>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "<div class='feature-box'><h3>🤖 AI-powered Interviews</h3><p>Practice with intelligent, adaptive mock interviews and detailed feedback</p></div>", 
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<div class='feature-box'><h3>📊 Real-time Analytics</h3><p>Track your performance and pinpoint areas for improvement instantly</p></div>", 
        unsafe_allow_html=True
    )

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.markdown(
        "<div class='feature-box'><h3>🏢 Company Questions Generator</h3><p>Generate custom interview questions instantly and save valuable time</p></div>", 
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        "<div class='feature-box'><h3>💡 AI Feedback</h3><p>Receive personalized feedback to improve your interview skills</p></div>", 
        unsafe_allow_html=True
    )
st.markdown("---")

col5, col6 = st.columns(2)

with col5:
    st.markdown(
        "<div class='feature-box'><h3>📝 Resume Builder via AI</h3><p>Create professional resumes with AI assistance to highlight your strengths</p></div>", 
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        "<div class='feature-box'><h3>✅ Resume Checker</h3><p>Analyze and improve your resume with AI-driven insights</p></div>", 
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
- Groq (gwen3 - 32B by default) for local AI generation and analysis.
"""

)
