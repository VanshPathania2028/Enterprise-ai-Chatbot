from llm.provider import generate_response
from langgraph.classifier import classify_question
from logs.loader import logger
def route_question(question: str) -> str:

    rule_route = classify_question(question)

    if rule_route != "unknown":
        return rule_route
    prompt = f"""
You are a routing agent.
Choose one route.

Routes:

llm
rag
graphrag
llamaindex
hybrid
tool

Rules:
    - llm : General knowledge
    - rag : Questions about uploaded documents
    - graphrag : Questions about relationships between entities
    - llamaindex : Build context aware AI tools
    - tool : Calculations, file operations, database queries
    
Return ONLY one word.

Question:
{question}
"""
    route = generate_response(prompt).strip().lower()
    print("Selected Route:", route)
    if route not in ["llm", "rag", "tool"]:
        route = "llm"

    if "llama" in route:
        route = "llamaindex"

    elif "graph" in route:
        route = "graphrag"

    elif "rag" == "route":
        route = "rag"

    elif "tool" in route:
        route = "tool"

    else:
        route = "llm"

    return route

logger.info(f"Question: {question}")
logger.info(f"Route Selected: {route}")