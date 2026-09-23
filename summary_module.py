from gemini_client import generate_text


def summarize_text(text: str) -> str:

    return generate_text(

        f"""
Summarize the following educational
passage for quick revision:

{text.strip()}
""",

        system_instruction=(
            "You are an educational summarizer. "
            "Preserve the important facts, "
            "definitions, relationships and "
            "conclusions. "
            "Remove repetition. "
            "Use a short title and concise "
            "bullet points when appropriate."
        ),

        temperature=0.2,

        max_output_tokens=1200,
    )