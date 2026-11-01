import os
import re
import requests
import streamlit as st

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-120b"
DEFAULT_MAX_NEW_TOKENS = 8192
REQUEST_TIMEOUT_SECONDS = 120

MODE_CONFIG = {
    "general": {
        "system": (
            "You are an expert resume writer and career coach. "
            "Give practical, concise, ATS-friendly advice."
        ),
    },
    "questions": {
        "system": (
            "You are an expert interviewer. Follow the user's requested "
            "output format carefully. Generate clear, relevant interview "
            "questions and answers when requested."
        ),
    },
    "analysis": {
        "system": (
            "You are an expert resume reviewer and career coach. "
            "Give structured, concise, actionable feedback."
        ),
    },
}

THINK_BLOCK_PATTERN = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def remove_think_blocks(text: str) -> str:
    """Remove reasoning blocks if the model produces them."""
    if not text:
        return ""
    return THINK_BLOCK_PATTERN.sub("", text).strip()


def clean_prompt(text: str) -> str:
    """Normalize input text."""
    if not text:
        return ""
    return str(text).strip()


def _get_groq_settings():
    """Read Groq credentials from Streamlit Secrets or environment variables."""
    try:
        api_key = st.secrets.get("GROQ_API_KEY", "")
        model = st.secrets.get("GROQ_MODEL", "")
    except Exception:
        api_key = ""
        model = ""

    api_key = api_key or os.getenv("GROQ_API_KEY", "")
    model = model or os.getenv("GROQ_MODEL", "") or DEFAULT_MODEL

    if not api_key:
        raise RuntimeError(
            "Groq API key is not configured. Add GROQ_API_KEY to "
            "Streamlit Secrets or set it as an environment variable."
        )
    return api_key, model


def local_chat(
    user_prompt: str,
    mode: str = "general",
    max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS,
) -> str:
    """Keep the legacy function name while sending requests directly to Groq."""
    user_prompt = clean_prompt(user_prompt)
    if not user_prompt:
        return ""

    api_key, model = _get_groq_settings()
    config = MODE_CONFIG.get(mode, MODE_CONFIG["general"])

    try:
        max_tokens = max(1, int(max_new_tokens))
    except (TypeError, ValueError):
        max_tokens = DEFAULT_MAX_NEW_TOKENS

    response = requests.post(
        GROQ_API_URL,
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": config["system"]},
                {"role": "user", "content": user_prompt},
            ],
            "max_completion_tokens": max_tokens,
        },
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    if not response.ok:
        try:
            detail = response.json().get("error", {}).get("message")
        except (ValueError, AttributeError):
            detail = response.text[:500]
        raise RuntimeError(
            f"Groq API error ({response.status_code}): "
            f"{detail or 'Request failed.'}"
        )

    result = response.json()
    choices = result.get("choices") or []
    if not choices:
        raise RuntimeError("Groq API returned an empty response.")

    answer = (choices[0].get("message") or {}).get("content", "")
    return remove_think_blocks(answer)


def _safe_chat(
    user_prompt: str,
    mode: str = "general",
    max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS,
):
    """Return (response, error), matching the existing app's calling convention."""
    try:
        return local_chat(
            user_prompt,
            mode=mode,
            max_new_tokens=max_new_tokens,
        ), None
    except Exception as exc:
        return None, str(exc)


def improve_summary(summary: str):
    summary = clean_prompt(summary)
    if not summary:
        return "", None

    prompt_text = f"""
Improve the following resume summary.

Make it:
- ATS-friendly
- Concise
- Impactful
- Keyword-rich
- Professional
- Specific to the candidate's experience

Do not invent qualifications or experience.

Current summary:
{summary}
"""
    return _safe_chat(prompt_text, mode="general", max_new_tokens=256)


def generate_bullets(role: str, text: str):
    role = clean_prompt(role)
    text = clean_prompt(text)
    if not text:
        return "", None

    prompt_text = f"""
Convert the following experience into strong resume bullet points.

Target role:
{role}

Original experience:
{text}

Rules:
- Start each bullet with a strong action verb.
- Focus on accomplishments rather than responsibilities.
- Quantify impact only when the provided information supports it.
- Never invent metrics.
- Keep bullets concise.
- Make them ATS-friendly.
- Do not number the bullets.
"""
    return _safe_chat(prompt_text, mode="general", max_new_tokens=384)


def resume_score(resume_text: str):
    resume_text = clean_prompt(resume_text)
    if not resume_text:
        return "", None

    prompt_text = f"""
Evaluate the following resume.

Resume:
{resume_text}

Provide:

ATS Score: X/100

Strengths:
- ...

Weaknesses:
- ...

Improvements:
- ...

Evaluate:
- Keyword relevance
- Skills
- Experience
- Achievements
- Formatting and content quality
- ATS compatibility

Do not invent information.
"""
    return _safe_chat(prompt_text, mode="analysis", max_new_tokens=512)


def match_keywords(resume: str, job_desc: str):
    resume = clean_prompt(resume)
    job_desc = clean_prompt(job_desc)
    if not resume or not job_desc:
        return "", None

    prompt_text = f"""
Compare this resume against this job description.

RESUME:
{resume}

JOB DESCRIPTION:
{job_desc}

Provide:

Missing Keywords:
- ...

Matching Keywords:
- ...

Skills Missing From Resume:
- ...

Suggestions:
- ...

Only recommend keywords that are genuinely relevant to the job.
Do not suggest falsely claiming experience.
"""
    return _safe_chat(prompt_text, mode="analysis", max_new_tokens=512)


def prompt(
    text: str,
    mode: str = "general",
    max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS,
):
    """Generic interface used by the rest of InterviewAce; returns (response, error)."""
    return _safe_chat(text, mode=mode, max_new_tokens=max_new_tokens)


def get_model_info() -> dict:
    """Return configured Groq model details without exposing the API key."""
    try:
        _, model = _get_groq_settings()
        configured = True
    except Exception:
        model = os.getenv("GROQ_MODEL", DEFAULT_MODEL)
        configured = False

    return {
        "device": "Groq Cloud API",
        "dtype": "Managed by Groq",
        "model": model,
        "model_path": model,
        "parameters": "Managed by Groq",
        "api_configured": configured,
        "provider": "Groq",
    }
