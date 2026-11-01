import streamlit as st
from components.navbar import render_navbar

st.set_page_config(
    page_title="Features - InterviewAce",
    page_icon="✨",
    layout="wide"
)

render_navbar("blog")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --navy: #182338;
    --gold: #c9a45c;
    --cream: #f7f5f0;
    --muted: #667085;
    --line: #e7e2d8;
}
html, body, [class*="css"] { font-family: "DM Sans", sans-serif; }
.stApp {
    background:
      radial-gradient(circle at 10% 0%, rgba(201,164,92,.14), transparent 28%),
      radial-gradient(circle at 90% 10%, rgba(24,35,56,.08), transparent 25%),
      linear-gradient(180deg,#fbfaf7,#f2f0e9);
}
.block-container {
    max-width: 100% !important;
    width: 100% !important;
    padding: 1.2rem 3.7vw 4rem !important;
}
.hero {
    text-align: center;
    padding: 3.4rem 1.5rem;
    border-radius: 30px;
    background: linear-gradient(135deg,#182338,#2b3955);
    color: white;
    box-shadow: 0 22px 60px rgba(24,35,56,.16);
    margin-bottom: 1.8rem;
}
.eyebrow {
    text-transform: uppercase;
    letter-spacing: .18em;
    font-size: .75rem;
    font-weight: 700;
    color: #ead8ad;
}
.hero h1 {
    font-family: "Playfair Display", serif;
    font-size: clamp(2.5rem,6vw,4.2rem);
    color: white;
    margin: .55rem 0 .75rem;
}
.hero p {
    max-width: 780px;
    margin: auto;
    color: #e9edf4;
    font-size: 1.05rem;
    line-height: 1.7;
}
.section-heading {
    font-family: "Playfair Display", serif;
    color: var(--navy);
    font-size: clamp(1.6rem,3vw,2.1rem);
    margin: 1.2rem 0 .35rem;
}
.section-intro { color: var(--muted); margin-bottom: 1rem; }
div.stButton > button {
    width: 100%;
    min-height: 66px;
    border: 1px solid var(--line);
    border-radius: 16px;
    background: white;
    color: var(--navy);
    font-weight: 800;
    font-size: 1rem;
    box-shadow: 0 8px 22px rgba(24,35,56,.07);
    transition: .22s ease;
}
div.stButton > button:hover {
    transform: translateY(-4px);
    border-color: var(--gold);
    color: var(--navy);
    box-shadow: 0 16px 32px rgba(24,35,56,.13);
}
div.stButton > button:focus {
    border-color: var(--gold);
    color: var(--navy);
}
.learning-card {
    height: 100%;
    background: rgba(255,255,255,.94);
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 1.5rem;
    margin: .4rem 0 1rem;
    box-shadow: 0 10px 28px rgba(24,35,56,.07);
    transition: transform .22s ease, box-shadow .22s ease;
}
.learning-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 38px rgba(24,35,56,.13);
}
.learning-card h3 { color: var(--navy); margin: .2rem 0 .55rem; }
.learning-card p, .learning-card li { color: var(--muted); line-height: 1.65; }
.level-tag {
    display: inline-block;
    padding: .3rem .7rem;
    border-radius: 30px;
    background: #f5eddd;
    color: #795c25;
    font-size: .76rem;
    font-weight: 800;
}
.stExpander {
    background: rgba(255,255,255,.9);
    border: 1px solid var(--line);
    border-radius: 15px;
}
.stExpander summary p { color: var(--navy) !important; font-weight: 700; }
.tip-box {
    background: white;
    border: 1px solid var(--line);
    border-left: 5px solid var(--gold);
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    margin-top: 1.2rem;
}
.tip-box h3 { color: var(--navy); }
.tip-box li { color: var(--muted); line-height: 1.8; }
@media(max-width: 750px) {
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="eyebrow">Learn • Practice • Grow</div>
    <h1>Your Interview Preparation Hub</h1>
    <p>Explore career-focused courses, sharpen your coding skills, and prepare for HR interviews — all in one place.</p>
</div>
""", unsafe_allow_html=True)

if "features_section" not in st.session_state:
    st.session_state.features_section = "courses"

st.markdown('<div class="section-heading">Explore the Learning Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="section-intro">Choose a category to discover guided topics and preparation resources.</div>', unsafe_allow_html=True)

course_col, coding_col, hr_col = st.columns(3)
with course_col:
    if st.button("📚  Courses", key="features_courses"):
        st.session_state.features_section = "courses"
with coding_col:
    if st.button("💻  Coding Preparation", key="features_coding"):
        st.session_state.features_section = "coding"
with hr_col:
    if st.button("🤝  HR Interview Prep", key="features_hr"):
        st.session_state.features_section = "hr"

section = st.session_state.features_section

if section == "courses":
    st.markdown('<div class="section-heading">📚 Explore Courses</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-intro">Build a strong foundation with these popular technical learning paths.</div>', unsafe_allow_html=True)

    courses = [
        ("🐍", "Python Programming", "Syntax, data types, functions, OOP, modules, file handling and practical projects.", "Beginner → Advanced"),
        ("☕", "Java Programming", "Core Java, object-oriented programming, collections, exceptions and basic application development.", "Beginner → Advanced"),
        ("🌐", "Web Development", "HTML, CSS, JavaScript, responsive layouts, DOM basics and front-end projects.", "Beginner → Intermediate"),
        ("🗄️", "SQL & Databases", "Queries, joins, grouping, subqueries, database design and relational concepts.", "Beginner → Intermediate"),
        ("⚙️", "C / C++ Programming", "Programming fundamentals, pointers, memory concepts, STL and object-oriented programming.", "Beginner → Advanced"),
        ("📱", " app Development", "Explore application fundamentals, UI design, APIs and project structure.", "Beginner → Intermediate"),
        ("🧠", "Data Structures & Algorithms", "Arrays, strings, linked lists, stacks, queues, trees, graphs and algorithm analysis.", "Intermediate → Advanced"),
        ("📊", "Data Science Foundations", "Python for data, data cleaning, visualization, statistics and introductory machine learning.", "Beginner → Intermediate"),
    ]
    cols = st.columns(2)
    for i, (icon, title, description, level) in enumerate(courses):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="learning-card">
                <span class="level-tag">{level}</span>
                <h3>{icon} {title}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)

elif section == "coding":
    st.markdown('<div class="section-heading">💻 Coding Interview Preparation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-intro">Get comfortable with the problem types that often come up in technical interviews.</div>',
        unsafe_allow_html=True
    )

    coding_cards = [
        ("📦", "Arrays & Strings",
         "Practise working with lists of values and text. Start with reversing strings, finding duplicates and solving two-sum style problems.",
         "Core topic"),
        ("🔗", "Linked Lists",
         "Learn how nodes connect and how to update links safely. Work on reversing a list, finding its middle and detecting cycles.",
         "Core topic"),
        ("📚", "Stacks & Queues",
         "Understand last-in-first-out and first-in-first-out structures. Try balanced brackets, next-greater-element and queue implementation problems.",
         "Core topic"),
        ("🌳", "Trees & Graphs",
         "Build confidence with hierarchical and connected data. Practise tree traversals, level-order search, BFS and DFS.",
         "Intermediate"),
        ("🔍", "Searching & Sorting",
         "Know when to use a linear scan, binary search or a sorting algorithm. Be ready to explain how your approach performs as input grows.",
         "Core topic"),
        ("🧩", "Dynamic Programming",
         "Break larger problems into smaller repeated decisions. Begin with Fibonacci and climbing stairs before moving to coin change and knapsack.",
         "Advanced"),
        ("⚙️", "Recursion & Backtracking",
         "Learn to solve a problem by reducing it to smaller cases. Practise subsets, permutations and simple maze or path problems.",
         "Intermediate"),
        ("⏱️", "Complexity & Problem Solving",
         "Compare possible solutions, estimate time and space complexity, and explain why you chose one approach over another.",
         "Essential skill"),
    ]

    coding_cols = st.columns(2)
    for i, (icon, title, description, level) in enumerate(coding_cards):
        with coding_cols[i % 2]:
            st.markdown(f"""
            <div class="learning-card">
                <span class="level-tag">{level}</span>
                <h3>{icon} {title}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tip-box">
        <h3>📝 Before you submit a solution</h3>
        <ul>
            <li>Check that you have handled empty input and other edge cases.</li>
            <li>Try a small example by hand to make sure the logic holds.</li>
            <li>Be ready to talk through your approach and its complexity.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif section == "hr":
    st.markdown('<div class="section-heading">🤝 HR Interview Preparation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-intro">Prepare for the conversations that help an interviewer understand how you work, communicate and approach a role.</div>',
        unsafe_allow_html=True
    )

    hr_cards = [
        ("👋", "Your Introduction",
         "Put together a short introduction covering your background, relevant experience, key skills and what you are looking for next.",
         "Getting started"),
        ("🎯", "Strengths & Areas to Improve",
         "Choose strengths you can support with real examples. When discussing an area to improve, explain what you are doing about it.",
         "Common questions"),
        ("🏢", "Why This Company?",
         "Learn what the organisation does, understand the role and connect your interests to the work the team is doing.",
         "Company research"),
        ("🤝", "Teamwork & Collaboration",
         "Prepare examples of working with others, sharing responsibility, resolving disagreements and helping a team reach a goal.",
         "Behavioural"),
        ("🧭", "Challenges & Problem Solving",
         "Think of a genuine challenge you faced. Explain the situation, what you were responsible for, the action you took and the result.",
         "Behavioural"),
        ("⏳", "Deadlines & Pressure",
         "Describe how you prioritise tasks, communicate when plans change and stay organised when several things need attention.",
         "Workplace skills"),
        ("💼", "Career Goals & Motivation",
         "Be ready to talk about what interests you in the role, what you hope to learn and the direction you would like your career to take.",
         "Career planning"),
        ("❓", "Questions for the Interviewer",
         "Prepare a few useful questions about the role, the team, expectations for the first few months and the next steps in the process.",
         "Closing well"),
    ]

    hr_cols = st.columns(2)
    for i, (icon, title, description, category) in enumerate(hr_cards):
        with hr_cols[i % 2]:
            st.markdown(f"""
            <div class="learning-card">
                <span class="level-tag">{category}</span>
                <h3>{icon} {title}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tip-box">
        <h3>💡 A simple way to prepare</h3>
        <ul>
            <li>Use examples from projects, internships, college or previous jobs.</li>
            <li>Keep answers focused; give enough detail without going off topic.</li>
            <li>For experience-based questions, the STAR structure can help keep your answer clear.</li>
            <li>Practise saying your answers aloud so they sound natural rather than memorised.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:2.5rem; padding:1.2rem; color:#667085;">
    <strong style="color:#182338;">InterviewAce Learning Hub</strong><br>
    Learn with purpose. Practice with confidence. Succeed with InterviewAce.
</div>
""", unsafe_allow_html=True)
