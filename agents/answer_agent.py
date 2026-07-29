from llm.provider import generate_response

def answer_agent(question, context):
    prompt = f"""
You are an AI assistant.

Use the following context to answer the uesr's question.

Context:
{context}

Question:
{question}
"""

    return generate_response(prompt)