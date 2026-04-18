import requests
import streamlit as st
import re

# =========================
# CONFIG
# =========================
api_key = st.secrets["key"]

GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"


# =========================
# CLEAN OUTPUT
# =========================
def _remove_think_blocks(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


# =========================
# CORE API CALL
# =========================
def _groq_chat(user_prompt: str, mode: str = "general"):

    if mode == "questions":
        system_prompt = (
            "You are an expert interviewer.\n"
            "ONLY output interview questions.\n"
            "No explanations. No formatting."
        )
        temperature = 0.2

    elif mode == "analysis":
        system_prompt = (
            "You are a resume reviewer and career coach.\n"
            "Give structured, concise feedback."
        )
        temperature = 0.5

    else:
        system_prompt = (
            "You are an expert resume writer and career coach."
        )
        temperature = 0.7

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_completion_tokens": 800,
    }

    try:
        response = requests.post(
            GROQ_BASE_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()

        data = response.json()
        raw = data["choices"][0]["message"]["content"]

        return _remove_think_blocks(raw), None

    except Exception as e:
        return None, str(e)


# =========================
# PUBLIC FUNCTIONS
# =========================

def improve_summary(summary):
    prompt = f"""
    Improve this resume summary to be ATS-friendly.

    {summary}

    Keep it concise, impactful, and keyword-rich.
    """
    return _groq_chat(prompt)


def generate_bullets(role, text):
    prompt = f"""
    Convert this into strong resume bullet points.

    Role: {role}
    Text: {text}

    Rules:
    - Use action verbs
    - Add impact (numbers if possible)
    - Keep concise
    - No numbering
    """
    return _groq_chat(prompt)


def resume_score(resume_text):
    prompt = f"""
    Evaluate this resume.

    {resume_text}

    Output:
    - ATS Score /100
    - Strengths
    - Weaknesses
    - Improvements
    """
    return _groq_chat(prompt, mode="analysis")


def match_keywords(resume, job_desc):
    prompt = f"""
    Compare resume with job description.

    Resume:
    {resume}

    Job Description:
    {job_desc}

    Output:
    - Missing keywords
    - Matching keywords
    - Suggestions
    """
    return _groq_chat(prompt, mode="analysis")


def prompt(text, mode="general"):
    return _groq_chat(text, mode)
