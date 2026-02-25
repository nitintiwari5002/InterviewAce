import streamlit as st
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Resume Builder", layout="wide")
st.markdown("## 📄 Professional Resume Builder")

# ---------- Image to Base64 ----------
def image_to_base64(image_file):
    if image_file is None:
        return None
    img = Image.open(image_file).convert("RGB")
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


# ---------- Improved Modern Resume Template ----------
def generate_resume_html(data, photo_base64=None):

    hobbies_html = "".join(f"<li>{h}</li>" for h in data["hobbies"])

    education_html = "".join(
        f"""
        <div class="item">
            <div class="item-header">
                <span class="item-title">{edu['degree']}</span>
                <span class="item-date">{edu['year']}</span>
            </div>
            <div class="item-sub">{edu['school']}</div>
            <div class="item-desc">{edu['details']}</div>
        </div>
        """
        for edu in data["education"]
    )

    experience_html = "".join(
        f"""
        <div class="item">
            <div class="item-header">
                <span class="item-title">{exp['position']}</span>
                <span class="item-date">{exp['duration']}</span>
            </div>
            <div class="item-sub">{exp['company']}</div>
            <div class="item-desc">{exp['description']}</div>
        </div>
        """
        for exp in data["experience"]
    )

    skills_html = "".join(
        f"""
        <div class="skill">
            <span>{skill['name']}</span>
            <div class="bar">
                <div class="fill" style="width:{skill['level']}%"></div>
            </div>
        </div>
        """
        for skill in data["skills"]
    )

    profile_img_html = (
        f'<img src="data:image/png;base64,{photo_base64}" class="profile-img" />'
        if photo_base64
        else ""
    )

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>

@page {{
    size: A4;
    margin: 0;
}}

body {{
    font-family: Arial, sans-serif;
    margin: 0;
    background: #f4f6f9;
}}

.resume {{
    width: 210mm;
    min-height: 297mm;
    margin: auto;
    background: white;
    display: flex;
}}

.sidebar {{
    width: 30%;
    background: #1e293b;
    color: white;
    padding: 30px 20px;
}}

.main {{
    width: 70%;
    padding: 40px;
}}

.profile-img {{
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 20px;
    border: 3px solid white;
}}

.name {{
    font-size: 26px;
    font-weight: bold;
}}

.title {{
    font-size: 14px;
    margin-bottom: 25px;
    opacity: 0.8;
}}

.section-title {{
    font-size: 14px;
    font-weight: bold;
    margin-top: 30px;
    margin-bottom: 15px;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 5px;
}}

.sidebar .section-title {{
    border-color: white;
}}

.item {{
    margin-bottom: 18px;
}}

.item-header {{
    display: flex;
    justify-content: space-between;
    font-weight: bold;
}}

.item-sub {{
    font-size: 13px;
    color: #555;
}}

.item-desc {{
    font-size: 13px;
    margin-top: 5px;
    color: #444;
}}

.skill {{
    margin-bottom: 10px;
}}

.bar {{
    width: 100%;
    height: 6px;
    background: #ddd;
    border-radius: 3px;
}}

.fill {{
    height: 6px;
    background: #3b82f6;
    border-radius: 3px;
}}

ul {{
    padding-left: 18px;
    margin: 0;
}}

.contact {{
    font-size: 13px;
    margin-bottom: 8px;
}}

.profile-text {{
    font-size: 13px;
    line-height: 1.5;
}}

</style>
</head>

<body>

<div class="resume">

    <div class="sidebar">
        {profile_img_html}
        <div class="name">{data['name']}</div>
        <div class="title">{data['title']}</div>

        <div class="section-title">CONTACT</div>
        <div class="contact">{data['phone']}</div>
        <div class="contact">{data['email']}</div>
        <div class="contact">{data['website']}</div>

        <div class="section-title">SKILLS</div>
        {skills_html}

        <div class="section-title">HOBBIES</div>
        <ul>{hobbies_html}</ul>
    </div>

    <div class="main">
        <div class="section-title">PROFILE</div>
        <div class="profile-text">{data['profile']}</div>

        <div class="section-title">{data['experience_heading']}</div>
        {experience_html}

        <div class="section-title">EDUCATION</div>
        {education_html}
    </div>

</div>

</body>
</html>
"""
    return html


# ---------- Main App ----------
st.markdown("### 🎯 Build Your Resume")

with st.form("resume_form"):

    photo = st.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"])
    photo_base64 = image_to_base64(photo) if photo else None

    name = st.text_input("Full Name", "Jordan Mitchell")
    title = st.text_input("Job Title", "Software Engineer")
    phone = st.text_input("Phone", "+91 9876543210")
    email = st.text_input("Email", "jordan@email.com")
    website = st.text_input("Website", "www.portfolio.com")
    profile = st.text_area("Professional Summary")

    experience = [{
        "position": st.text_input("Position"),
        "company": st.text_input("Company"),
        "duration": st.text_input("Duration"),
        "description": st.text_area("Description")
    }]

    education = [{
        "degree": st.text_input("Degree"),
        "school": st.text_input("School"),
        "year": st.text_input("Year"),
        "details": st.text_input("Details")
    }]

    skills = [{
        "name": st.text_input("Skill"),
        "level": st.slider("Skill Level", 0, 100, 80)
    }]

    hobbies = st.text_input("Hobbies (comma separated)", "Coding, Reading")
    hobbies_list = [h.strip() for h in hobbies.split(",")]

    submitted = st.form_submit_button("Generate Resume")


if submitted:
    data = {
        "name": name,
        "title": title,
        "phone": phone,
        "email": email,
        "website": website,
        "profile": profile,
        "experience": experience,
        "education": education,
        "skills": skills,
        "hobbies": hobbies_list,
        "experience_heading": "Work Experience"
    }

    html = generate_resume_html(data, photo_base64)

    st.download_button(
        "🌐 Download HTML Resume",
        data=html,
        file_name="resume.html",
        mime="text/html"
    )

    st.markdown("### 👁️ Preview")
    st.components.v1.html(html, height=1000, scrolling=True)
