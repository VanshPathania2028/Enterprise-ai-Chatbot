from llm.provider import generate_response

def select_tool(question: str) -> str:
    prompt = f"""
You are an AI tool router.

Available tools:

1. Calculator
    - Mathematical calculations
    - Arithmetic
    - Percentages
    
2. file_reader
 - Read text files
 - Read documents
 3. database
    - SQL queries
    - Database lookups
    
Return ONLY one word.

Calculator
file_reader
database

Question:
{question}

Answer:
"""

    tool = generate_response(prompt).strip().lower()
    return tool