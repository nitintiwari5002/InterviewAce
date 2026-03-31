import streamlit as st

# Page Configuration
Home = st.Page("pages/home.py", title="Home")
Features = st.Page("pages/features.py", title="Features")
Resume = st.Page("pages/resume.py", title="Resume")

pg = st.navigation([Home, Features, Resume], position="top")

# 🚀 Run Navigation
pg.run()
