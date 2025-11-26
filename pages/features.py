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
        font-size: 1.18rem;
        color: #fff;
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
        "<div class='feature-box'><b>AI-powered Interviews</b><br>Practice with intelligent, adaptive mock interviews and detailed feedback.</div>", 
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<div class='feature-box'><b>Real-time Analytics</b><br>Track your performance and pinpoint areas for improvement instantly.</div>", 
        unsafe_allow_html=True
    )

st.markdown("---")
