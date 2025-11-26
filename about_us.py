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
    h1, h5 {
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        text-shadow: 0 2px 4px #2c5364;
    }
    h1 {
        color: #6a3093;
        font-size: 2.3rem;
    }
    h5 {
        color: #ffeb70;
        font-size: 1.2rem;
    }
    .purple-list li {
        color: lightpink;
        font-size: 1.22rem;
        margin-bottom: 8px;
        list-style-type: circle;
    }
    </style>
    <div class='full-navbar'>InterviewAce</div>
""", unsafe_allow_html=True)

# --- Logo and Title ---
st.image("assets/Mini (2).png", width=250)
st.header("About InterviewAce")

st.markdown(
    "<h5>InterviewAce was created by a team of experienced engineers and educators who understand the challenges of technical interviews.</h5>", 
    unsafe_allow_html=True
)
st.markdown(
    "<h5>Our platform leverages cutting-edge AI technology to provide personalized, adaptive interview experiences that help engineering students build confidence and master the skills needed to succeed in their dream jobs.</h5>", 
    unsafe_allow_html=True
)
st.markdown("---")

# --- Team List ---
st.markdown(
    """
    <ul class="purple-list">
        <li>Founded by experienced engineers</li>
        <li>Focused on student success</li>
        <li>Privacy-first approach</li>
        <li>Open-source AI technology</li>
    </ul>
    """, 
    unsafe_allow_html=True
)