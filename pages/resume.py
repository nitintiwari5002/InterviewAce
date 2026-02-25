import streamlit as st
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Resume Builder", layout="wide")
st.title("📄 Simple Resume Builder")

# ---------- Convert Image to Base64 ----------
def image_to_base64(image_file):
    if image_file is None:
        return None
    img = Image.open(image_file).convert("RGB")
    img = img.resize((150, 150))
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ---------- HTML Generator ----------
def generate_resume_html(data, photo_base64=None):

    photo_html = ""
    if photo_base64:
        photo_html = f"""
        <div style="text-align:center;">
            <img src="data:image/png;base64,{photo_base64}" 
                 style="width:130px;height:130px;border-radius:50%;margin-bottom:15px;">
        </div>
        """

    experience_html = ""
    for exp in data["experience"]:
        experience_html += f"""
        <h3>{exp['position']} - {exp['company']}</h3>
        <p><i>{exp['duration']}</i></p>
        <p>{exp['description']}</p>
        <br>
        """

    education_html = ""
    for edu in data["education"]:
        education_html += f"""
        <h3>{edu['degree']} - {edu['school']}</h3>
        <p><i>{edu['year']}</i></p>
        <p>{edu['details']}</p>
        <br>
        """

    skills_html = ", ".join([skill["name"] for skill in data["skills"]])
    hobbies_html = ", ".join(data["hobbies"])

    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }}
            h1 {{
                margin-bottom: 5px;
            }}
            h2 {{
                border-bottom: 1px solid black;
                padding-bottom: 5px;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>

        {photo_html}

        <h1>{data['name']}</h1>
        <p><b>{data['title']}</b></p>
        <p>{data['phone']} | {data['email']} | {data['website']}</p>

        <h2>Profile</h2>
        <p>{data['profile']}</p>

        <h2>{data['experience_heading']}</h2>
        {experience_html}

        <h2>Education</h2>
        {education_html}

        <h2>Skills</h2>
        <p>{skills_html}</p>

        <h2>Hobbies</h2>
        <p>{hobbies_html}</p>

    </body>
    </html>
    """

    return html


# ---------- Career Level ----------
career_level = st.selectbox("Career Level", ["Fresher", "Experienced"])

# ---------- Form ----------
with st.form("resume_form"):

    st.subheader("Personal Information")

    photo_file = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
    photo_base64 = image_to_base64(photo_file) if photo_file else None

    full_name = st.text_input("Full Name")
    role = st.text_input("Job Title")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    website = st.text_input("Website")
    profile = st.text_area("Professional Summary")

    # ---------- Experience / Internship ----------
    exp_heading = "Internships / Projects" if career_level == "Fresher" else "Work Experience"
    st.subheader(exp_heading)

    num_exp = st.number_input("Number of entries", 1, 5, 1)

    experience_list = []

    for i in range(num_exp):
        st.markdown(f"### Entry {i+1}")
        position = st.text_input("Role / Position", key=f"pos_{i}")
        company = st.text_input("Company / Organization", key=f"comp_{i}")
        duration = st.text_input("Duration", key=f"dur_{i}")
        description = st.text_area("Description", key=f"desc_{i}")

        experience_list.append({
            "position": position,
            "company": company,
            "duration": duration,
            "description": description
        })

    # ---------- Education ----------
    st.subheader("Education")

    num_edu = st.number_input("Number of education entries", 1, 3, 1)

    education_list = []

    for i in range(num_edu):
        st.markdown(f"### Education {i+1}")
        degree = st.text_input("Degree", key=f"deg_{i}")
        school = st.text_input("College / University", key=f"sch_{i}")
        year = st.text_input("Year", key=f"year_{i}")
        details = st.text_input("Details (CGPA etc)", key=f"det_{i}")

        education_list.append({
            "degree": degree,
            "school": school,
            "year": year,
            "details": details
        })

    # ---------- Skills ----------
    st.subheader("Skills")
    skills_raw = st.text_input("Enter skills separated by comma")
    skills_list = [{"name": s.strip()} for s in skills_raw.split(",") if s.strip()]

    # ---------- Hobbies ----------
    st.subheader("Hobbies")
    hobbies_raw = st.text_input("Enter hobbies separated by comma")
    hobbies_list = [h.strip() for h in hobbies_raw.split(",") if h.strip()]

    submitted = st.form_submit_button("Generate Resume")

# ---------- After Submit ----------
if submitted:

    resume_data = {
        "name": full_name,
        "title": role,
        "phone": phone,
        "email": email,
        "website": website,
        "profile": profile,
        "experience": experience_list,
        "education": education_list,
        "skills": skills_list,
        "hobbies": hobbies_list,
        "experience_heading": exp_heading,
    }

    html_content = generate_resume_html(resume_data, photo_base64)

    st.download_button(
        "Download Resume (HTML)",
        data=html_content,
        file_name="resume.html",
        mime="text/html"
    )

    st.markdown("### Preview")
    st.components.v1.html(html_content, height=900, scrolling=True)
