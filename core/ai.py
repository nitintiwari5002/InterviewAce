import requests

# Small, fast default model
DEFAULT_MODEL = "phi3:mini"

OLLAMA_URL = "http://localhost:11434/api/generate"

def ollama_prompt(
    prompt: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int | None = 512,
    temperature: float = 0.6,
):
    """
    Returns (text, error). If error is not None, text may be None.
    Uses shorter timeout and optional token limit for speed.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }
    if max_tokens is not None:
        payload["options"]["num_predict"] = max_tokens

    try:
        resp = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300,  # keep UI snappy
        )
        if not resp.ok:
            return None, f"Ollama error: {resp.status_code}"

        data = resp.json()
        return data.get("response", "").strip(), None

    except requests.exceptions.Timeout:
        return None, "Ollama timed out. Please try again with a shorter input."

    except Exception as e:
        return None, f"Ollama connection error: {e}"
