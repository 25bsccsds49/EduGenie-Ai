from functools import lru_cache

from google import genai
from google.genai import types

from config import settings


@lru_cache(maxsize=1)
def get_client():
    """
    Create and cache the Gemini API client.
    """

    if not settings.gemini_configured:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Please add GEMINI_API_KEY to the .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key,
        http_options=types.HttpOptions(
            timeout=60000
        ),
    )


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.4,
    max_output_tokens: int = 2048,
    response_schema=None,
) -> str:
    """
    Generate text using Google Gemini.
    """

    if not prompt or not prompt.strip():
        raise ValueError(
            "Prompt cannot be empty."
        )

    client = get_client()

    config_kwargs = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }

    if system_instruction:
        config_kwargs["system_instruction"] = (
            system_instruction
        )

    if response_schema is not None:
        config_kwargs["response_mime_type"] = (
            "application/json"
        )

        config_kwargs["response_schema"] = (
            response_schema
        )

    try:

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                **config_kwargs
            ),
        )

    except Exception as exc:

        raise RuntimeError(
            f"Gemini API request failed: {exc}"
        ) from exc

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()
