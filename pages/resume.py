import streamlit as st

st.set_page_config(page_title="ATS Resume Builder", layout="centered")
st.title("📄 ATS Friendly Resume Builder")

# -------------------- FORM -------------------- #

career_level = st.selectbox("Career Level", ["Fresher", "Experienced"])

with st.form("resume_form"):

    st.subheader("Personal Information")
    full_name = st.text_input("Full Name *")
    role = st.text_input("Job Title *")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    website = st.text_input("LinkedIn / Portfolio")

    st.subheader("Professional Summary")
    profile = st.text_area("Summary", height=100)

    # Experience / Projects
    exp_heading = "Projects" if career_level == "Fresher" else "Work Experience"
    st.subheader(exp_heading)

    num_exp = st.number_input("Number of entries", 1, 5, 1)
    experience_list = []

    for i in range(num_exp):
        st.markdown(f"**Entry {i+1}**")
        position = st.text_input("Title", key=f"pos_{i}")
        company = st.text_input("Company", key=f"comp_{i}")
        duration = st.text_input("Duration", key=f"dur_{i}")
        description = st.text_area(
            "Description (use separate lines for bullet points)",
            key=f"desc_{i}",
            height=80
        )

        experience_list.append({
            "position": position,
            "company": company,
            "duration": duration,
            "description": description
        })

    # Education
    st.subheader("Education")
    num_edu = st.number_input("Number of education entries", 1, 3, 1)
    education_list = []

    for i in range(num_edu):
        st.markdown(f"**Education {i+1}**")
        school = st.text_input("University", key=f"school_{i}")
        degree = st.text_input("Degree", key=f"degree_{i}")
        year = st.text_input("Year", key=f"year_{i}")

        education_list.append({
            "school": school,
            "degree": degree,
            "year": year
        })

    # Skills
    st.subheader("Skills")
    skills = st.text_input("Comma separated skills (Python, SQL, React)")

    submitted = st.form_submit_button("Generate Resume")


# -------------------- RESUME GENERATION -------------------- #

if submitted:

    if not full_name or not role:
        st.error("Full Name and Job Title are required.")
    else:

        skills_list = [s.strip() for s in skills.split(",") if s.strip()]

        resume_html = f"""
        <html>
        <head>
        <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.5;
            color: black;
            padding: 40px;
        }}
        h1 {{
            font-size: 22px;
            margin-bottom: 4px;
        }}
        h2 {{
            font-size: 15px;
            margin-top: 18px;
            border-bottom: 1px solid black;
        }}
        p {{
            margin: 4px 0;
        }}
        ul {{
            margin-top: 4px;
            margin-bottom: 8px;
        }}
        </style>
        </head>
        <body>

        <h1>{full_name}</h1>
        <p><b>{role}</b></p>
        <p>{phone} | {email} | {website}</p>

        <h2>Professional Summary</h2>
        <p>{profile}</p>

        <h2>{exp_heading}</h2>
        """

        # Experience Section
        for exp in experience_list:
            resume_html += f"""
            <p><b>{exp['position']}</b> - {exp['company']}</p>
            <p><i>{exp['duration']}</i></p>
            <ul>
            """

            bullets = exp["description"].split("\n")
            for bullet in bullets:
                if bullet.strip():
                    resume_html += f"<li>{bullet.strip()}</li>"

            resume_html += "</ul>"

        # Education Section
        resume_html += "<h2>Education</h2>"
        for edu in education_list:
            resume_html += f"""
            <p><b>{edu['degree']}</b></p>
            <p>{edu['school']} | {edu['year']}</p>
            """

        # Skills Section
        resume_html += "<h2>Skills</h2>"
        resume_html += "<p>" + ", ".join(skills_list) + "</p>"

        resume_html += "</body></html>"

        st.markdown("---")
        st.subheader("Preview")
        st.components.v1.html(resume_html, height=900)

        st.download_button(
            "Download Resume (HTML)",
            data=resume_html,
            file_name=f"{full_name.replace(' ', '_')}_ATS_Resume.html",
            mime="text/html"
        )
