import requests
import streamlit as st
import re

# =========================
# CONFIG
# =========================
api_key = st.secrets["key"]

GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "qwen/qwen3-32b"


# =========================
# INTERNAL HELPERS
# =========================
def _remove_think_blocks(text: str) -> str:
    """
    Removes <think>...</think> blocks produced by reasoning models
    like Qwen / DeepSeek.
    """
    if not text:
        return ""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


# =========================
# CORE GROQ CALL
# =========================
def _groq_chat(user_prompt: str, mode: str = "general"):
    """
    mode:
      - questions : STRICT interview questions only
      - analysis  : interview feedback & evaluation
      - general   : default free-form response
    """

    # ---------- SYSTEM PROMPTS ----------
    if mode == "questions":
        system_prompt = (
            "You are an expert interviewer.\n"
            "DO NOT reveal your reasoning.\n"
            "DO NOT include <think> tags or internal thoughts.\n"
            "ONLY output final interview questions.\n\n"
            "Rules:\n"
            "- Each line must be ONE complete interview question\n"
            "- Each question must end with a question mark\n"
            "- No explanations\n"
            "- No headings\n"
            "- No numbering\n"
            "- No bullet points\n"
            "- No extra text\n"
            "- Output ONLY the questions\n"
        )
        temperature = 0.2

    elif mode == "analysis":
        system_prompt = (
            "You are a senior interviewer and career coach.\n"
            "Analyze the candidate's responses and provide:\n"
            "- Strengths\n"
            "- Weaknesses\n"
            "- Concrete improvement suggestions\n"
            "Be professional, concise, and constructive."
        )
        temperature = 0.6

    else:
        system_prompt = (
            "You are an expert technical interviewer and career coach."
        )
        temperature = 0.7

    # ---------- REQUEST ----------
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
        "max_tokens": 800,
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

        raw_output = data["choices"][0]["message"]["content"]

        # 🔒 REMOVE REASONING LEAKS
        cleaned_output = _remove_think_blocks(raw_output)

        return cleaned_output, None

    except requests.exceptions.RequestException as e:
        return None, f"API Request Error: {str(e)}"

    except Exception as e:
        return None, f"Unexpected Error: {str(e)}"


# =========================
# PUBLIC API (USED BY home.py)
# =========================
def prompt(prompt_text: str, mode: str = "general"):
    """
    Safe wrapper used by home.py

    Returns:
        (response_text, error)
    """
    return _groq_chat(prompt_text, mode)