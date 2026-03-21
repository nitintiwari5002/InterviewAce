import streamlit as st
from core.ai import improve_summary, generate_bullets, resume_score, match_keywords
import pdfkit
import tempfile

st.set_page_config(page_title="AI Resume Builder", layout="wide")

st.title("🚀 AI Resume Builder (ATS + Modern)")

# =========================
# SESSION STATE
# =========================
if "generated_html" not in st.session_state:
    st.session_state.generated_html = ""

if "skill_sections" not in st.session_state:
    st.session_state.skill_sections = []

# =========================
# INPUT SECTION
# =========================
st.subheader("👤 Personal Information")

name = st.text_input("Full Name", key="name")
title = st.text_input("Job Title", key="title")
phone = st.text_input("Phone", key="phone")
email = st.text_input("Email", key="email")
linkedin = st.text_input("LinkedIn", key="linkedin")
github = st.text_input("GitHub", key="github")

mode = st.radio("Resume Mode", ["ATS (Simple)", "Modern (Styled)"])
layout = st.radio("Layout (Modern Only)", ["One Column", "Two Column"])

# =========================
# SUMMARY
# =========================
st.subheader("🧠 Professional Summary")

summary = st.text_area("Write your summary", key="summary")

if st.button("✨ Improve Summary"):
    res, _ = improve_summary(summary)
    if res:
        summary = res
        st.success("Improved!")
        st.write(res)

# =========================
# EXPERIENCE
# =========================
st.subheader("💼 Experience")

experience = st.text_area("Enter experience (each point new line)", key="experience")

if st.button("⚡ Generate Bullet Points"):
    res, _ = generate_bullets(title, experience)
    if res:
        experience = res
        st.success("Improved!")
        st.write(res)

# =========================
# PROJECTS
# =========================
st.subheader("🚀 Projects")

projects = st.text_area(
    "Format: Title | Tech | Bullet1, Bullet2",
    key="projects"
)

# =========================
# EDUCATION
# =========================
st.subheader("🎓 Education")

education = st.text_area(
    "Enter each education detail on new line",
    key="education"
)

# =========================
# SKILLS (DYNAMIC)
# =========================
st.subheader("🛠 Technical Skills")

col1, col2 = st.columns(2)

with col1:
    skill_header = st.text_input("Skill Category", key="skill_header")

with col2:
    skill_values = st.text_input("Skills (comma separated)", key="skill_values")

if st.button("➕ Add Skill Section"):
    if skill_header and skill_values:
        st.session_state.skill_sections.append((skill_header, skill_values))
        st.success(f"Added {skill_header}")

# Display added skills
for header, values in st.session_state.skill_sections:
    st.write(f"**{header}:** {values}")

# =========================
# CERTIFICATIONS
# =========================
st.subheader("📜 Certifications")

certifications = st.text_input("Comma separated", key="certifications")

# =========================
# HELPERS
# =========================
def to_list(text):
    return [line.strip() for line in text.split("\n") if line.strip()]

def format_list(items):
    return "<ul>" + "".join([f"<li>{i}</li>" for i in items]) + "</ul>" if items else ""

def format_projects(projects_text):
    html = ""
    for line in projects_text.split("\n"):
        if not line.strip():
            continue

        parts = line.split("|")
        title = parts[0].strip() if len(parts) > 0 else ""
        tech = parts[1].strip() if len(parts) > 1 else ""
        desc = parts[2].strip() if len(parts) > 2 else ""

        bullets = [d.strip() for d in desc.split(",") if d.strip()]

        if title:
            html += f"<p><b>{title}</b>" + (f" | {tech}" if tech else "") + "</p>"

        html += format_list(bullets)

    return html

def format_skills_sections(skill_sections):
    html = ""
    for header, skills in skill_sections:
        skills_list = [s.strip() for s in skills.split(",") if s.strip()]
        if header and skills_list:
            html += f"<p><b>{header}:</b> {', '.join(skills_list)}</p>"
    return html

def generate_pdf(html):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdfkit.from_string(html, tmp.name)
        return tmp.name

# =========================
# GENERATE RESUME
# =========================
if st.button("🚀 Generate Resume"):

    exp_html = format_list(to_list(experience))
    edu_html = format_list(to_list(education))
    proj_html = format_projects(projects)
    skills_html = format_skills_sections(st.session_state.skill_sections)
    cert_html = format_list([c.strip() for c in certifications.split(",") if c.strip()])

    contact_parts = [title, phone, email, linkedin, github]
    contact_line = " | ".join([c for c in contact_parts if c])

    # =========================
    # ATS VERSION
    # =========================
    if mode == "ATS (Simple)":

        html = f"""
        <html>
        <body>

        <h1>{name}</h1>
        <p>{contact_line}</p>

        {f"<h2>Professional Summary</h2><p>{summary}</p>" if summary else ""}
        {f"<h2>Skills</h2>{skills_html}" if skills_html else ""}
        {f"<h2>Experience</h2>{exp_html}" if exp_html else ""}
        {f"<h2>Projects</h2>{proj_html}" if proj_html else ""}
        {f"<h2>Education</h2>{edu_html}" if edu_html else ""}
        {f"<h2>Certifications</h2>{cert_html}" if cert_html else ""}

        </body>
        </html>
        """

    # =========================
    # MODERN VERSION
    # =========================
    else:

        if layout == "One Column":
            html = f"""
            <html>
            <head>
            <style>
            body {{ font-family: Arial; margin:40px; }}
            h1 {{ text-align:center; }}
            .section {{ margin-top:20px; }}
            .title {{ font-weight:bold; border-bottom:1px solid #ccc; }}
            </style>
            </head>
            <body>

            <h1>{name}</h1>
            <p style="text-align:center;">{contact_line}</p>

            {f"<div class='section'><div class='title'>SUMMARY</div><p>{summary}</p></div>" if summary else ""}
            {f"<div class='section'><div class='title'>SKILLS</div>{skills_html}</div>" if skills_html else ""}
            {f"<div class='section'><div class='title'>EXPERIENCE</div>{exp_html}</div>" if exp_html else ""}
            {f"<div class='section'><div class='title'>PROJECTS</div>{proj_html}</div>" if proj_html else ""}
            {f"<div class='section'><div class='title'>EDUCATION</div>{edu_html}</div>" if edu_html else ""}
            {f"<div class='section'><div class='title'>CERTIFICATIONS</div>{cert_html}</div>" if cert_html else ""}

            </body>
            </html>
            """

        else:
            html = f"""
            <html>
            <head>
            <style>
            body {{ font-family: Arial; margin:30px; }}
            .container {{ display:flex; }}
            .left {{ width:30%; padding-right:20px; }}
            .right {{ width:70%; }}
            .section {{ margin-top:20px; }}
            .title {{ font-weight:bold; border-bottom:1px solid #ccc; }}
            </style>
            </head>

            <body>

            <h1>{name}</h1>
            <p>{contact_line}</p>

            <div class="container">

                <div class="left">
                    {f"<div class='section'><div class='title'>SKILLS</div>{skills_html}</div>" if skills_html else ""}
                    {f"<div class='section'><div class='title'>CERTIFICATIONS</div>{cert_html}</div>" if cert_html else ""}
                    {f"<div class='section'><div class='title'>EDUCATION</div>{edu_html}</div>" if edu_html else ""}
                </div>

                <div class="right">
                    {f"<div class='section'><div class='title'>SUMMARY</div><p>{summary}</p></div>" if summary else ""}
                    {f"<div class='section'><div class='title'>EXPERIENCE</div>{exp_html}</div>" if exp_html else ""}
                    {f"<div class='section'><div class='title'>PROJECTS</div>{proj_html}</div>" if proj_html else ""}
                </div>

            </div>

            </body>
            </html>
            """

    st.session_state.generated_html = html
    st.success("✅ Resume Generated!")

# =========================
# PREVIEW + DOWNLOAD
# =========================
if st.session_state.generated_html:

    st.subheader("📄 Preview")
    st.components.v1.html(st.session_state.generated_html, height=800)

    st.download_button("📥 Download HTML", st.session_state.generated_html, "resume.html")

    try:
        pdf_file = generate_pdf(st.session_state.generated_html)
        with open(pdf_file, "rb") as f:
            st.download_button("📄 Download PDF", f, "resume.pdf")
    except:
        st.warning("⚠️ Install wkhtmltopdf for PDF support")

# =========================
# ATS TOOLS
# =========================
st.subheader("📊 ATS Tools")

if st.session_state.generated_html:

    if st.button("📊 Check ATS Score"):
        res, _ = resume_score(st.session_state.generated_html)
        if res:
            st.markdown(res)

    job_desc = st.text_area("Paste Job Description")

    if st.button("🎯 Match Job"):
        res, _ = match_keywords(st.session_state.generated_html, job_desc)
        if res:
            st.markdown(res)