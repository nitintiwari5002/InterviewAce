import streamlit as st

# Page Configuration
Home = st.Page("pages/home.py", title="Home")
Features = st.Page("pages/features.py", title="Features")
About = st.Page("pages/about_us.py", title="About")

pg = st.navigation([Home, Features, About], position="top")

# 🚀 Run Navigation (automatically handles page switching)
pg.run()