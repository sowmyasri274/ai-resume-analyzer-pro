import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import re

st.set_page_config(
    page_title="AI Resume Analyzer PRO",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer PRO")

# ---------------- SKILL DATABASE ----------------

SKILLS_DB = [
    "python",
    "java",
    "c++",
    "html",
    "css",
    "javascript",
    "sql",
    "machine learning",
    "deep learning",
    "streamlit",
    "flask",
    "django",
    "react",
    "node",
    "git",
    "github",
    "vscode",
    "data structures & algorithms"
]

# ---------------- PDF TEXT EXTRACTION ----------------

def extract_text(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text.lower()

# ---------------- SKILL EXTRACTION ----------------

def extract_skills(text):
    text = text.lower()

    found = []

    if "python" in text:
        found.append("python")

    if "java" in text:
        found.append("java")

    if "c++" in text:
        found.append("c++")

    if "html" in text:
        found.append("html")

    if "css" in text:
        found.append("css")

    if "javascript" in text:
        found.append("javascript")

    if "sql" in text:
        found.append("sql")

    if "github" in text:
        found.append("github")

    if re.search(r"\bgit\b", text):
        found.append("git")

    if "react" in text:
        found.append("react")

    if "node" in text or "nodejs" in text:
        found.append("node")

    if "vs code" in text or "vscode" in text:
        found.append("vscode")

    if (
        "data structures" in text
        or "algorithms" in text
        or "dsa" in text
    ):
        found.append("data structures & algorithms")

    if "machine learning" in text:
        found.append("machine learning")

    if "deep learning" in text:
        found.append("deep learning")

    if "streamlit" in text:
        found.append("streamlit")

    if "flask" in text:
        found.append("flask")

    if "django" in text:
        found.append("django")

    return found

# ---------------- ATS SCORE ----------------

def advanced_score(text, skills):

    score = 0

    # Skills (Max 30)
    score += min(len(skills) * 3, 30)

    # Projects (Max 20)
    project_words = [
        "project",
        "developed",
        "built",
        "designed",
        "implemented",
        "created"
    ]

    project_score = 0

    for word in project_words:
        project_score += text.count(word)

    score += min(project_score * 2, 20)

    # Certifications (Max 15)
    cert_words = [
        "aws",
        "google",
        "salesforce",
        "cisco",
        "forage",
        "certificate",
        "certification"
    ]

    cert_score = 0

    for word in cert_words:
        if word in text:
            cert_score += 1

    score += min(cert_score * 2, 15)

    # Education
    if "b.tech" in text or "bachelor" in text:
        score += 10

    # GitHub
    if "github" in text:
        score += 5

    # LinkedIn
    if "linkedin" in text:
        score += 5

    # Sections
    sections = [
        "education",
        "technical skills",
        "projects",
        "certifications",
        "achievements"
    ]

    section_score = 0

    for section in sections:
        if section in text:
            section_score += 2

    score += section_score

    return min(score, 100)

# ---------------- CHART ----------------

def show_score_chart(score):

    df = pd.DataFrame({
        "Category": ["ATS Score"],
        "Score": [score]
    })

    st.bar_chart(df.set_index("Category"))

# ---------------- ROLE PREDICTION ----------------

def predict_role(skills):

    if "machine learning" in skills or "deep learning" in skills:
        return "AI / ML Engineer"

    elif (
        "sql" in skills
        and "python" in skills
        and "machine learning" not in skills
    ):
        return "Data Analyst"

    elif (
        "java" in skills
        or "c++" in skills
    ):
        return "Software Development Engineer"

    return "General Software Engineer"

# ---------------- UI ----------------

st.subheader("📤 Upload Resume")

uploaded_file = st.file_uploader(
    "📤 Upload your Resume (PDF only)",
    type=["pdf"]
)

if uploaded_file is not None:

    text = extract_text(uploaded_file)

    st.markdown("### 📌 Extracted Resume")
    st.write(text)

    skills = extract_skills(text)

    st.markdown("### 💡 Detected Skills")
    st.write(skills)

    word_count = len(text.split())

    st.markdown("### 📈 Resume Statistics")
    st.write(f"Total Words: {word_count}")
    st.write(f"Detected Skills: {len(skills)}")

    role = predict_role(skills)

    st.markdown("### 🎯 Predicted Career Role")
    st.success(role)

    score = advanced_score(text, skills)

    st.markdown("### 📊 ATS Score")

    if score >= 80:
        st.success(f"🟢 Strong Resume - {score}/100")
    elif score >= 60:
        st.warning(f"🟡 Average Resume - {score}/100")
    else:
        st.error(f"🔴 Weak Resume - {score}/100")

    show_score_chart(score)

    st.progress(score / 100)

    required_skills = [
        "python",
        "java",
        "c++",
        "sql",
        "data structures & algorithms"
    ]

    missing_skills = []

    for skill in required_skills:
        if skill not in skills:
            missing_skills.append(skill)

    st.markdown("### 💡 Missing Skills")

    if missing_skills:
        for skill in missing_skills:
            st.write("❌", skill)
    else:
        st.success("Excellent! No critical skills missing.")

    st.markdown("### 🚀 Recommended Skills")

    recommendations = [
        "sql",
        "git",
        "github",
        "react",
        "streamlit"
    ]

    for skill in recommendations:
        if skill not in skills:
            st.write("➕", skill)