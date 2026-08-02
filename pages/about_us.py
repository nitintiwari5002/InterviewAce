import streamlit as st
from core.theme import get_complete_theme, get_glass_navbar

st.set_page_config(page_title="About - InterviewAce", layout="wide")

st.markdown(get_complete_theme(), unsafe_allow_html=True)
st.markdown(get_glass_navbar(), unsafe_allow_html=True)


# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>The Story Behind InterviewAce</h1>
    <p>Bridging innovation with cutting-edge AI technology</p>
</div>
""", unsafe_allow_html=True)


# ---------------- MAIN CONTENT ----------------
st.markdown('<div class="section">', unsafe_allow_html=True)

col1, col2 = st.columns([1.6, 1])

with col1:
    st.markdown("""
    <div class="card">
        <h2>🌊 What is InterviewAce?</h2>
        <p>
        InterviewAce is an AI-powered platform designed to help job seekers prepare 
        for interviews with confidence. It offers personalized mock interviews, 
        intelligent feedback, and adaptive coaching using powerful AI models.
        </p>
        <div class="tech-stack">
            <div class="tech-badge">Streamlit</div>
            <div class="tech-badge">Groq AI</div>
            <div class="tech-badge">Python</div>
            <div class="tech-badge">SQLite</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("assets/image.jpeg", use_container_width=True)
    
st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------- VISION SECTION ----------------
st.markdown("""
<div class="card" style="text-align:center;">
    <h2>🚀 Vision for the Future</h2>
    <p>
    We aim to evolve with AI advancements to deliver hyper-personalized 
    interview simulations, real-time behavioral analysis, and intelligent 
    career growth insights.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)