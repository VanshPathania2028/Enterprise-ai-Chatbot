from llm.provider import generate_response

def extract_entity(question: str):

    prompt = f"""
Extract the main entity from the question.

Return ONLY the entity.

Question:
{question}
"""

    return generate_response(prompt).strip()