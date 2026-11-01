
import streamlit as st
import base64
from pathlib import Path


# =========================================================
# NAVBAR CSS
# =========================================================

NAVBAR_CSS = """
<style>

/* Hide Streamlit's default header */
div[data-testid="stToolbar"],
header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
}

/* Main navbar */
.st-key-interviewace-navbar {
    width: 100%;
    box-sizing: border-box;
    background: linear-gradient(
        110deg,
        #111d32 0%,
        #243957 55%,
        #17263d 100%
    ) !important;
    border: 1px solid rgba(201, 164, 92, 0.42) !important;
    border-radius: 20px;
    padding: 18px 28px !important;
    margin-bottom: 30px;
    min-height: 82px;
    box-shadow: 0 16px 38px rgba(17, 29, 49, 0.22);
}

/* Navbar columns */
.st-key-interviewace-navbar [data-testid="stHorizontalBlock"] {
    align-items: center;
    gap: 12px;
}

.st-key-interviewace-navbar [data-testid="column"] {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 4px !important;
}

/* Common navigation link styling */
.st-key-interviewace-navbar
[data-testid="stPageLink-NavLink"] {
    width: 100%;
    min-height: 52px !important;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 12px !important;
    border-radius: 12px !important;
    border: 1px solid transparent !important;
    background: rgba(255, 255, 255, 0.035) !important;
    font-family: "DM Sans", Arial, sans-serif;
    font-size: 0.95rem !important;
    font-weight: 800 !important;
    text-decoration: none !important;
    white-space: nowrap;
    opacity: 1 !important;
    transition: all 0.2s ease;
}

/* HOME - Light blue */
.st-key-nav-home [data-testid="stPageLink-NavLink"],
.st-key-nav-home [data-testid="stPageLink-NavLink"] * {
    color: #7DD3FC !important;
    -webkit-text-fill-color: #7DD3FC !important;
    opacity: 1 !important;
}

/* BLOG - Mint green */
.st-key-nav-blog [data-testid="stPageLink-NavLink"],
.st-key-nav-blog [data-testid="stPageLink-NavLink"] * {
    color: #86EFAC !important;
    -webkit-text-fill-color: #86EFAC !important;
    opacity: 1 !important;
}

/* ABOUT US - Lavender */
.st-key-nav-about [data-testid="stPageLink-NavLink"],
.st-key-nav-about [data-testid="stPageLink-NavLink"] * {
    color: #C4B5FD !important;
    -webkit-text-fill-color: #C4B5FD !important;
    opacity: 1 !important;
}

/* RESUME BUILDER - Gold */
.st-key-nav-resume [data-testid="stPageLink-NavLink"],
.st-key-nav-resume [data-testid="stPageLink-NavLink"] * {
    color: #FCD34D !important;
    -webkit-text-fill-color: #FCD34D !important;
    opacity: 1 !important;
}

/* Hover effect */
.st-key-interviewace-navbar
[data-testid="stPageLink-NavLink"]:hover {
    background: #F0D99F !important;
    border-color: #F0D99F !important;
    transform: translateY(-3px);
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.20);
}

/* Hover text becomes dark */
.st-key-interviewace-navbar
[data-testid="stPageLink-NavLink"]:hover,
.st-key-interviewace-navbar
[data-testid="stPageLink-NavLink"]:hover * {
    color: #172238 !important;
    -webkit-text-fill-color: #172238 !important;
}

/* Brand section */
.ia-brand-outside {
    display: flex;
    align-items: center;
    gap: 22px;
    margin: 0 0 16px 4px;
    padding: 8px 0;
}

/* LOGO - enlarged, with no square container */
.ia-brand-image {
    width: 220px;
    height: 175px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
    flex-shrink: 0;
    overflow: visible;
}

.ia-brand-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
}

.ia-brand-image span {
    font-size: 2.5rem;
    font-weight: 900;
    color: #172238;
}

/* Brand name */
.ia-brand-title {
    color: #172238 !important;
    font-family: "DM Sans", Arial, sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    line-height: 1.2;
}

.ia-brand-title span {
    color: #A77D2D !important;
}

.ia-brand-subtitle {
    margin-top: 5px;
    color: #475467 !important;
    font-family: "DM Sans", Arial, sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
}

/* SAME FULL-WIDTH LAYOUT ON EVERY PAGE */
.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(201,164,92,.14),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(24,35,56,.08),
            transparent 25%
        ),
        linear-gradient(180deg, #fbfaf7, #f1efe8) !important;
}

/* Use the available screen width */
.stApp [data-testid="stAppViewBlockContainer"] {
    max-width: 100% !important;
    width: 100% !important;
    padding-left: 3.7vw !important;
    padding-right: 3.7vw !important;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
}

/* Consistent font */
html, body, [class*="css"] {
    font-family: "DM Sans", Arial, sans-serif;
}

/* Consistent content spacing */
.stApp [data-testid="stVerticalBlock"] {
    gap: 1.2rem;
}

/* Consistent card appearance */
.card, .feature, .panel, .vision {
    border-radius: 22px;
    box-shadow: 0 12px 32px rgba(24,35,56,.09);
    transition: transform .22s ease, box-shadow .22s ease;
}

.card:hover, .feature:hover, .panel:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 40px rgba(24,35,56,.15);
}

/* Tablet */
@media (max-width: 900px) {
    .st-key-interviewace-navbar {
        padding: 12px !important;
    }

    .st-key-interviewace-navbar
    [data-testid="stPageLink-NavLink"] {
        font-size: 0.78rem !important;
        padding: 0 6px !important;
    }

    .ia-brand-image {
        width: 145px;
        height: 115px;
    }

    .ia-brand-title {
        font-size: 1.9rem;
    }
}

/* Mobile */
@media (max-width: 650px) {
    .st-key-interviewace-navbar {
        border-radius: 14px;
        padding: 8px !important;
    }

    .st-key-interviewace-navbar
    [data-testid="column"] {
        padding: 2px !important;
    }

    .st-key-interviewace-navbar
    [data-testid="stPageLink-NavLink"] {
        min-height: 40px !important;
        font-size: 0.65rem !important;
        padding: 0 3px !important;
    }

    .ia-brand-outside {
        gap: 12px;
    }
}

/* Small mobile */
@media (max-width: 480px) {
    .stApp [data-testid="stAppViewBlockContainer"] {
        padding-left: 4vw !important;
        padding-right: 4vw !important;
    }

    .ia-brand-image {
        width: 95px;
        height: 85px;
    }

    .ia-brand-title {
        font-size: 1.35rem;
    }

    .ia-brand-subtitle {
        font-size: 0.60rem;
    }

    .st-key-interviewace-navbar
    [data-testid="stPageLink-NavLink"] {
        font-size: 0.56rem !important;
    }
}

</style>
"""


# =========================================================
# BRAND LOGO
# =========================================================

def get_brand_html():
    """Render the InterviewAce logo and brand name above the navbar."""

    logo_path = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "Mini (2).png"
    )

    if logo_path.is_file():
        encoded = base64.b64encode(
            logo_path.read_bytes()
        ).decode("ascii")

        logo = (
            f'<img src="data:image/png;base64,{encoded}" '
            f'alt="InterviewAce logo">'
        )
    else:
        logo = "<span>IA</span>"

    return (
        '<div class="ia-brand-outside">'
            '<div class="ia-brand-image">'
                f'{logo}'
            '</div>'
            '<div>'
                '<div class="ia-brand-title">'
                    'Interview<span>Ace</span>'
                '</div>'
                '<div class="ia-brand-subtitle">'
                    'AI Career Assistant'
                '</div>'
            '</div>'
        '</div>'
    )


# =========================================================
# NAVIGATION BAR
# =========================================================

def render_navbar(_active_page="home"):
    """Render the shared navbar and visually mark the current page."""

    st.markdown(NAVBAR_CSS, unsafe_allow_html=True)

    active_key = str(_active_page or "home").strip().lower().replace(" ", "-")
    if active_key not in {"home", "blog", "about", "resume"}:
        active_key = "home"

    st.markdown(
        f"""
        <style>
        .st-key-nav-{active_key} [data-testid="stPageLink-NavLink"] {{
            background: rgba(201, 164, 92, .20) !important;
            border: 1px solid rgba(201, 164, 92, .85) !important;
            box-shadow: inset 0 -3px 0 #c9a45c;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Brand logo and name
    st.markdown(get_brand_html(), unsafe_allow_html=True)

    # Main navigation bar
    with st.container(key="interviewace-navbar"):
        home_col, blog_col, about_col, resume_col = st.columns(
            [1.0, 1.15, 1.55, 1.25],
            gap="medium"
        )

        with home_col:
            with st.container(key="nav-home"):
                st.page_link(
                    "pages/home.py",
                    label="⌂  Home",
                    use_container_width=True
                )

        # Blog navigation
        with blog_col:
            with st.container(key="nav-blog"):
                st.page_link(
                    "pages/features.py",
                    label="✦  Blog",
                    use_container_width=True
                )
        with about_col:
            with st.container(key="nav-about"):
                st.page_link(
                    "pages/about_us.py",
                    label="◎  About Us",
                    use_container_width=True
                )

        with resume_col:
            with st.container(key="nav-resume"):
                st.page_link(
                    "pages/resume.py",
                    label="▣  Resume Builder",
                    use_container_width=True
                )
