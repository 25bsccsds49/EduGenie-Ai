from gemini_client import generate_text


def answer_question(question: str) -> str:

    return generate_text(

        question.strip(),

        system_instruction=(
            "You are EduGenie, an educational "
            "question-answering assistant. "
            "Answer the student's question "
            "accurately and concisely. "
            "For academic topics, explain "
            "the reasoning when useful. "
            "If you are uncertain, say so "
            "rather than inventing facts."
        ),

        temperature=0.2,

        max_output_tokens=900,
    )