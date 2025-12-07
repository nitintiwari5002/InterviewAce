import streamlit as st

st.image("assets/Mini (2).png", width=250)
st.title("About InterviewAce")

st.write(
    "InterviewAce is an AI-powered interview preparation and evaluation platform. "
    "It helps candidates practice realistic interviews and provides companies with "
    "structured tools to generate and assess interview questions."
)

st.subheader("Our Mission")
st.write(
    "To make interview preparation more accessible, personalized, and data-driven "
    "for students, professionals, and companies."
)

st.subheader("Key Highlights")
st.markdown(
    """
- Local AI via Ollama for privacy-friendly analysis.
- Real-time interview question generation.
- Actionable feedback to improve communication and technical depth.
"""
)

# ---- TEAM SECTION ----
st.markdown("## Our Team")

# Team Leader
c1, c2 = st.columns([1, 2])
with c1:
    st.image("assets/me.jpg", width=220)
with c2:
    st.markdown("### Team Leader")
    st.markdown("_Streamlit & Ollama Integration_")
    st.markdown(
        "Designs the overall UI and application flow, builds the Streamlit pages, "
        "and integrates Ollama to generate and analyze interview questions for users and companies."
    )

st.markdown("---")

# Software Tester
c1, c2 = st.columns([1, 2])
with c1:
    st.image("assets/Sahil.jpeg", width=220)
with c2:
    st.markdown("### Software Tester")
    st.markdown("_Test Design & Execution_")
    st.markdown(
        "Creates and runs manual and automated test cases, verifies each feature, and "
        "ensures that InterviewAce behaves reliably for both candidates and recruiters."
    )

st.markdown("---")

# Database Administrator
c1, c2 = st.columns([1, 2])
with c1:
    st.image("assets/Soham.jpeg", width=220)
with c2:
    st.markdown("### Database Administrator")
    st.markdown("_SQLite Database Management_")
    st.markdown(
        "Designs and maintains the SQLite database schema, manages user and company records, "
        "and keeps interview data structured and easy to query for future features."
    )

st.markdown("---")

# Figma Designer
c1, c2 = st.columns([1, 2])
with c1:
    st.image("assets/Atharva.jpeg", width=220)
with c2:
    st.markdown("### Figma Designer")
    st.markdown("_UI/UX Design_")
    st.markdown(
        "Creates the visual design and user experience flows using Figma, ensuring "
        "that InterviewAce is intuitive and engaging for users."
    )

st.markdown("---")
