from chatbot.prompts import SYSTEM_PROMPT
from llm.provider import generate_response


def chat(user_message: str):
    prompt = f"""
    {SYSTEM_PROMPT}
User:
{user_message}
"""
    return generate_response(prompt)