from gemini_client import generate_text


def get_learning_recommendations(
    topic: str
) -> str:

    return generate_text(

        f"""
Create a personalized learning path for:

{topic.strip()}

Include:

1. Beginner foundations

2. Intermediate concepts

3. Advanced concepts

4. A practical mini-project
   or exercise

5. Suggested learning resources
   including resource type and
   what to look for

6. A realistic timeline

7. A short checklist for
   self-assessment

Make the plan adaptable for
a learner starting from
beginner level.
""",

        system_instruction=(
            "You are an educational mentor. "
            "Produce structured, practical "
            "learning guidance. "
            "Do not invent exact URLs or "
            "claim a resource exists unless "
            "you are certain. "
            "Resource names may be "
            "described by type."
        ),

        temperature=0.5,

        max_output_tokens=1800,
    )