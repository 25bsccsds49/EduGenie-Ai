import json
from typing import List

from pydantic import BaseModel, Field

from gemini_client import generate_text


# ---------------------------------------------------------
# Quiz question model
# ---------------------------------------------------------

class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str


# ---------------------------------------------------------
# Quiz model
# ---------------------------------------------------------

class Quiz(BaseModel):

    questions: List[QuizQuestion] = Field(
        min_length=3,
        max_length=3
    )


# ---------------------------------------------------------
# Generate quiz
# ---------------------------------------------------------

def generate_quiz(
    source_text: str
) -> dict:

    prompt = f"""
Create exactly 3 multiple-choice
questions from the educational text below.

Requirements:

- Exactly 3 questions.
- Exactly 4 options per question.
- Only one option is correct.
- correct_answer must exactly match
  one of the four option strings.
- Include a short explanation
  for each answer.
- Keep questions relevant to
  the supplied text.
- Return JSON only.

Educational text:

{source_text.strip()}
"""

    raw = generate_text(

        prompt,

        system_instruction=(
            "You generate assessment "
            "content for students. "
            "Do not add Markdown fences "
            "around JSON."
        ),

        temperature=0.4,

        max_output_tokens=1800,

        response_schema=Quiz,
    )

    # -----------------------------------------------------
    # Validate Gemini JSON
    # -----------------------------------------------------

    try:

        data = Quiz.model_validate_json(
            raw
        )

    except Exception:

        # Defensive fallback
        cleaned = clean_json_block(raw)

        data = Quiz.model_validate_json(
            cleaned
        )

    return data.model_dump()


# ---------------------------------------------------------
# Clean Markdown JSON fences
# ---------------------------------------------------------

def clean_json_block(
    value: str
) -> str:

    value = value.strip()

    if value.startswith("```"):

        lines = value.splitlines()

        if (
            lines
            and lines[0].startswith("```")
        ):

            lines = lines[1:]

        if (
            lines
            and lines[-1].strip() == "```"
        ):

            lines = lines[:-1]

        value = "\n".join(
            lines
        ).strip()

    # Make sure it is valid JSON
    json.loads(value)

    return value