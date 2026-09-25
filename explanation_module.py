from functools import lru_cache

from config import settings
from gemini_client import generate_text


@lru_cache(maxsize=1)
def _load_local_pipeline():

    if not settings.local_explainer_enabled:
        return None

    try:

        from transformers import pipeline

        return pipeline(
            "text2text-generation",
            model=settings.local_explainer_model,
            device=-1,
        )

    except Exception:

        # Local model is optional.
        # Gemini will be used as fallback.
        return None


def explain_concept(topic: str) -> str:

    topic = topic.strip()

    local = _load_local_pipeline()

    # -----------------------------------------------------
    # Try local LaMini-Flan-T5 model
    # -----------------------------------------------------

    if local is not None:

        prompt = (
            "Explain the following educational concept "
            "in very simple language. "
            "Use short paragraphs and one small example. "
            "Avoid unnecessary jargon.\n\n"
            f"Concept: {topic}"
        )

        try:

            result = local(
                prompt,
                max_new_tokens=220,
                do_sample=False
            )

            if (
                result
                and result[0].get("generated_text")
            ):

                return result[0][
                    "generated_text"
                ].strip()

        except Exception:

            pass

    # -----------------------------------------------------
    # Gemini fallback
    # -----------------------------------------------------

    return generate_text(

        f"""
Explain this educational concept
for a beginner:

{topic}

Use:
- simple language
- a clear analogy or example
- a short recap
""",

        system_instruction=(
            "You are EduGenie, a patient "
            "educational tutor. "
            "Prioritize clarity and correctness. "
            "If the topic is ambiguous, "
            "state the assumption you made."
        ),

        temperature=0.3,

        max_output_tokens=700,
    )
