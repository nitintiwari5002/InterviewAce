import streamlit as st
import base64
from io import BytesIO
from PIL import Image
from xhtml2pdf import pisa  # HTML -> PDF (pure Python)

st.set_page_config(page_title="Resume Builder", layout="wide")
st.markdown("## 📄 Professional Resume Builder (Modern Sidebar)")

# ---------- Image to Base64 ----------
def image_to_base64(image_file):
    """Convert uploaded image to base64 string for embedding in HTML."""
    if image_file is None:
        return None
    img = Image.open(image_file).convert("RGB")
    img = img.resize((180, 180), Image.Resampling.LANCZOS)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# ---------- HTML Generator (Modern Sidebar) ----------
def generate_modern_sidebar_resume(data, photo_base64=None):
    """Generate HTML for modern left-sidebar resume layout (single template)."""

    hobbies_html = "".join(
        f'<div class="hobby">• {h}</div>' for h in data["hobbies"]
    )

    education_html = "".join(
        f"""
        <div class="education-item">
            <div class="edu-name">{edu['school']}</div>
            <div class="edu-meta">{edu['degree']} • {edu['year']}</div>
            <div class="edu-details">{edu['details']}</div>
        </div>
        """
        for edu in data["education"]
    )

    experience_html = "".join(
        f"""
        <div class="work-item">
            <div class="work-title">{work['position']}</div>
            <div class="work-company">{work['company']} • {work['duration']}</div>
            <div class="work-description">{work['description']}</div>
        </div>
        """
        for work in data["experience"]
    )

    skills_html = "".join(
        f"""
        <div class="skill-item">
            <div class="skill-label">{skill['name']}</div>
            <div class="skill-bar">
                <div class="skill-fill" style="width: {skill['level']}%"></div>
            </div>
        </div>
        """
        for skill in data["skills"]
    )

    if photo_base64:
        profile_img_html = f'<img src="data:image/png;base64,{photo_base64}" class="profile-img" alt="Profile" />'
    else:
        profile_img_html = '<div class="profile-img-placeholder"></div>'

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{data['name']} - Resume</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            html, body {{
                width: 100%;
                height: 100%;
            }}
            body {{
                font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
                background: #f0f2f5;
                padding: 20px 0;
            }}
            .container {{
                display: flex;
                width: 100%;
                max-width: 1000px;
                margin: 20px auto;
                background: #ffffff;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);
                border-radius: 2px;
                overflow: hidden;
            }}
            .sidebar {{
                background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
                padding: 50px 35px;
                width: 32%;
                border-right: 1px solid #dee2e6;
            }}
            .main {{
                padding: 50px 45px;
                flex: 1;
                overflow-wrap: break-word;
            }}
            .profile-img {{
                width: 140px;
                height: 140px;
                border-radius: 50%;
                border: 4px solid #4a90e2;
                margin-bottom: 25px;
                object-fit: cover;
                box-shadow: 0 4px 12px rgba(74, 144, 226, 0.25);
            }}
            .profile-img-placeholder {{
                width: 140px;
                height: 140px;
                border-radius: 50%;
                background: linear-gradient(135deg, #d0d8e0, #e0e8f0);
                border: 4px solid #4a90e2;
                margin-bottom: 25px;
                box-shadow: 0 4px 12px rgba(74, 144, 226, 0.15);
            }}
            .name {{
                font-size: 26px;
                font-weight: 700;
                color: #1a1a1a;
                margin-bottom: 6px;
            }}
            .title {{
                font-size: 12px;
                color: #666;
                text-transform: uppercase;
                letter-spacing: 2px;
                font-weight: 600;
                margin-bottom: 32px;
                padding-bottom: 18px;
                border-bottom: 2px solid rgba(74, 144, 226, 0.2);
            }}
            .main-name {{
                font-size: 36px;
                font-weight: 700;
                color: #1a1a1a;
                margin-bottom: 8px;
            }}
            .main-subtitle {{
                font-size: 13px;
                color: #888;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
                margin-bottom: 35px;
                padding-bottom: 20px;
                border-bottom: 2px solid #e9ecef;
            }}
            .section-title {{
                font-size: 11px;
                font-weight: 700;
                color: #4a90e2;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                margin-top: 30px;
                margin-bottom: 16px;
            }}
            .contact-item {{
                font-size: 11px;
                color: #555;
                margin-bottom: 11px;
                line-height: 1.6;
                word-break: break-word;
            }}
            .contact-label {{
                font-weight: 700;
                color: #2c2c2c;
                display: inline-block;
                min-width: 70px;
            }}
            .profile-text {{
                font-size: 12px;
                color: #555;
                line-height: 1.7;
                margin-top: 8px;
            }}
            .hobby {{
                font-size: 11px;
                color: #666;
                margin-bottom: 8px;
            }}
            .education-item {{
                margin-bottom: 24px;
            }}
            .edu-name {{
                font-weight: 700;
                font-size: 12px;
                color: #1a1a1a;
                margin-bottom: 4px;
            }}
            .edu-meta {{
                font-size: 10px;
                color: #888;
                margin-bottom: 6px;
                font-style: italic;
            }}
            .edu-details {{
                font-size: 11px;
                color: #666;
                line-height: 1.6;
            }}
            .work-item {{
                margin-bottom: 26px;
            }}
            .work-title {{
                font-weight: 700;
                font-size: 12px;
                color: #1a1a1a;
                margin-bottom: 4px;
            }}
            .work-company {{
                font-size: 10px;
                color: #888;
                margin-bottom: 8px;
                font-weight: 600;
            }}
            .work-description {{
                font-size: 11px;
                color: #666;
                line-height: 1.65;
            }}
            .skill-item {{
                margin-bottom: 14px;
            }}
            .skill-label {{
                font-size: 11px;
                font-weight: 700;
                color: #2c2c2c;
                margin-bottom: 6px;
            }}
            .skill-bar {{
                width: 100%;
                height: 6px;
                background: #e9ecef;
                border-radius: 3px;
                overflow: hidden;
            }}
            .skill-fill {{
                height: 100%;
                background: linear-gradient(90deg, #4a90e2, #357abd);
                border-radius: 3px;
            }}
            @page {{
                size: A4;
                margin: 0;
            }}
            @media print {{
                body {{
                    padding: 0;
                    background: #ffffff;
                }}
                .container {{
                    box-shadow: none;
                    border-radius: 0;
                    margin: 0;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="sidebar">
                {profile_img_html}
                <div class="name">{data['name']}</div>
                <div class="title">{data['title']}</div>

                <div class="section-title">📞 CONTACT</div>
                <div class="contact-item"><span class="contact-label">PHONE</span><br>{data['phone']}</div>
                <div class="contact-item" style="margin-top: 10px;"><span class="contact-label">EMAIL</span><br>{data['email']}</div>
                <div class="contact-item" style="margin-top: 10px;"><span class="contact-label">WEBSITE</span><br>{data['website']}</div>

                <div class="section-title">🎯 PROFILE</div>
                <div class="profile-text">{data['profile']}</div>

                <div class="section-title">🎨 HOBBIES</div>
                {hobbies_html}
            </div>

            <div class="main">
                <div class="main-name">{data['name']}</div>
                <div class="main-subtitle">{data['title']}</div>

                <div class="section-title">{data['experience_heading']}</div>
                {experience_html}

                <div class="section-title">🎓 EDUCATION</div>
                {education_html}

                <div class="section-title">🔧 SKILLS</div>
                {skills_html}
            </div>
        </div>
    </body>
    </html>
    """
    return html

# ---------- HTML -> PDF (xhtml2pdf) ----------
def html_to_pdf_bytes(html_content: str) -> bytes | None:
    """Convert HTML string to PDF bytes using xhtml2pdf."""
    pdf_buffer = BytesIO()
    result = pisa.CreatePDF(src=html_content, dest=pdf_buffer)
    if result.err:
        return None
    return pdf_buffer.getvalue()

# ---------- Main App ----------
st.markdown("### 🎯 Build Your Resume")
career_level = st.selectbox("Career Level", ["Fresher", "Experienced"])  # new feature

with st.form("resume_form", clear_on_submit=False):
    # Photo
    st.markdown("#### 📸 Upload Your Photo")
    col_photo, col_preview = st.columns([1, 3])
    photo_base64 = None
    with col_photo:
        photo_file = st.file_uploader("Choose photo (JPG/PNG)", type=["jpg", "jpeg", "png"])
        if photo_file:
            photo_base64 = image_to_base64(photo_file)
    with col_preview:
        if photo_file:
            st.image(photo_file, width=120, caption="Preview")

    # Basic info
    st.markdown("#### 👤 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name *", value="Jordan Mitchell")
        role = st.text_input("Job Title *", value="UI/UX Designer")
    with col2:
        phone = st.text_input("Phone", value="+1-212-555-0155")
        email = st.text_input("Email", value="jordan@example.com")

    website = st.text_input("Website / Portfolio", value="www.yourportfolio.com")

    default_profile_fresher = (
        "Enthusiastic and quick-learning fresher with strong fundamentals and hands-on project "
        "experience, eager to contribute to real-world products."
    )
    default_profile_experienced = (
        "Experienced professional with a proven track record of delivering high-quality products, "
        "leading projects end-to-end, and collaborating with cross‑functional teams."
    )
    profile = st.text_area(
        "Professional Summary",
        value=default_profile_fresher if career_level == "Fresher" else default_profile_experienced,
        height=80,
    )

    # Experience / Projects
    exp_heading = "Projects / Internships" if career_level == "Fresher" else "Work Experience"
    st.markdown(f"#### 💼 {exp_heading}")
    num_exp_default = 2 if career_level == "Experienced" else 1
    num_exp = st.number_input("Number of entries", 1, 5, num_exp_default)
    experience_list = []

    for i in range(num_exp):
        with st.expander(f"{exp_heading} {i+1}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                default_position = "Software Engineering Intern" if career_level == "Fresher" else "Software Engineer"
                position = st.text_input(
                    "Title / Role",
                    value=default_position if i == 0 else "",
                    key=f"position_{i}",
                )
                default_company = "ABC Corp Internship" if career_level == "Fresher" else "ABC Corp"
                company = st.text_input(
                    "Company / Organization",
                    value=default_company if i == 0 else "",
                    key=f"company_{i}",
                )
            with col2:
                duration = st.text_input(
                    "Duration",
                    value="Jan 2024 – Present" if i == 0 else "",
                    key=f"duration_{i}",
                )
            default_desc_fresher = (
                "Worked on academic / side projects using modern technologies, "
                "implemented features, and collaborated with team members."
            )
            default_desc_experienced = (
                "Designed, implemented, and optimized features in production systems, "
                "improving performance and user experience."
            )
            description = st.text_area(
                "Description",
                value=default_desc_fresher if career_level == "Fresher" else default_desc_experienced,
                height=70,
                key=f"desc_{i}",
            )
            experience_list.append(
                {
                    "position": position,
                    "company": company,
                    "duration": duration,
                    "description": description,
                }
            )

    # Education
    st.markdown("#### 🎓 Education")
    num_edu = st.number_input("Number of education entries", 1, 3, 1)
    education_list = []
    for i in range(num_edu):
        with st.expander(f"Education {i+1}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                school = st.text_input("School / University", value="College of Engineering", key=f"school_{i}")
                degree = st.text_input("Degree", value="BTech Computer Engineering", key=f"degree_{i}")
            with col2:
                year = st.text_input("Year", value="2026", key=f"year_{i}")
            details = st.text_input("Details", value="CGPA: 8.5 / 10", key=f"details_{i}")
            education_list.append(
                {"school": school, "degree": degree, "year": year, "details": details}
            )

    # Skills
    st.markdown("#### 🔧 Skills")
    num_skills = st.number_input("Number of skills", 1, 8, 5)
    skills_list = []
    for i in range(num_skills):
        c1, c2 = st.columns([3, 1])
        with c1:
            skill_name = st.text_input(f"Skill {i+1}", value=f"Skill {i+1}", key=f"skill_{i}")
        with c2:
            level = st.slider(f"Level {i+1}", 0, 100, 80, key=f"level_{i}")
        skills_list.append({"name": skill_name, "level": level})

    # Hobbies
    st.markdown("#### 🎯 Hobbies")
    hobbies_raw = st.text_input(
        "Hobbies (comma separated)", value="Coding, Reading, Music", key="hobbies"
    )
    hobbies = [h.strip() for h in hobbies_raw.split(",") if h.strip()]

    submitted = st.form_submit_button("✨ Generate Resume")

# ---------- After submit ----------
if submitted:
    if not full_name or not role:
        st.error("Please fill at least Name and Job Title.")
    else:
        resume_data = {
            "name": full_name,
            "title": role,
            "phone": phone,
            "email": email,
            "website": website,
            "profile": profile,
            "education": education_list,
            "experience": experience_list,
            "skills": skills_list,
            "hobbies": hobbies,
            "experience_heading": "Projects / Internships" if career_level == "Fresher" else "Work Experience",
        }

        html_content = generate_modern_sidebar_resume(resume_data, photo_base64)
        pdf_bytes = html_to_pdf_bytes(html_content)

        st.markdown("---")
        st.markdown("### 📥 Download")

        col1, col2 = st.columns(2)
        with col1:
            if pdf_bytes:
                st.download_button(
                    "📄 Download PDF",
                    data=pdf_bytes,
                    file_name=f"{full_name.replace(' ', '_')}_Resume.pdf",
                    mime="application/pdf",
                )
            else:
                st.error("PDF generation failed. Check xhtml2pdf installation.")

        with col2:
            st.download_button(
                "🌐 Download HTML",
                data=html_content,
                file_name=f"{full_name.replace(' ', '_')}_Resume.html",
                mime="text/html",
            )

        st.markdown("---")
        st.markdown("### 👁️ Preview")
        st.components.v1.html(html_content, height=1200, scrolling=True)
