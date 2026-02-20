import streamlit as st

st.set_page_config(page_title="About - InterviewAce", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.main {
    background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 100%);
}

/* HERO SECTION */
.hero {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 6rem 2rem;
    border-radius: 0 0 40px 40px;
    text-align: center;
    color: white;
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}

.hero h1 {
    font-size: clamp(2.5rem, 6vw, 4rem);
    font-weight: 800;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.3rem;
    opacity: 0.95;
}

/* CONTENT WRAPPER */
.section {
    max-width: 1200px;
    margin: auto;
    padding: 5rem 2rem;
}

/* GLASS CARD */
.card {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(20px);
    padding: 3rem;
    border-radius: 28px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 25px 60px rgba(0,0,0,0.12);
}

.card h2 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
    color: #2d3748;
}

.card p {
    font-size: 1.1rem;
    color: #4a5568;
    line-height: 1.8;
}

/* TECH BADGES */
.tech-stack {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 2rem;
}

.tech-badge {
    padding: 0.7rem 1.4rem;
    border-radius: 50px;
    font-weight: 600;
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    box-shadow: 0 6px 20px rgba(102,126,234,0.4);
    transition: 0.3s ease;
}

.tech-badge:hover {
    transform: scale(1.08);
}

/* IMAGE STYLING */
.dev-photo {
    border-radius: 24px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.15);
    transition: 0.3s ease;
}

.dev-photo:hover {
    transform: scale(1.03);
}

/* CTA BUTTON */
.cta-btn {
    margin-top: 2rem;
    padding: 1rem 2.5rem;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1rem;
    border: none;
    color: white;
    background: linear-gradient(45deg, #667eea, #764ba2);
    cursor: pointer;
    transition: 0.3s ease;
}

.cta-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(102,126,234,0.5);
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .section {
        padding: 3rem 1.2rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>The Story Behind InterviewAce</h1>
    <p>Bridging ancient wisdom with cutting-edge AI</p>
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
            <div class="tech-badge">Groq - qwen3 32B</div>
            <div class="tech-badge">Python</div>
            <div class="tech-badge">Computer Vision</div>
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