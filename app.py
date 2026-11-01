import streamlit as st

Home = st.Page("pages/home.py", title="Home")
Blog = st.Page("pages/features.py", title="Features")
About = st.Page("pages/about_us.py", title="About")
Resume = st.Page("pages/resume.py", title="Resume")

pg = st.navigation([Home, Blog, About, Resume], position="hidden")
pg.run()