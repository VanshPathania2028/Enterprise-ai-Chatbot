import re

def classify_question(question: str):

    q = question.lower()

    if  any(word in q for word in [
        "calculate",
        "add",
        "subtract",
        "multiply",
        "divide"
    ]):
        return "tool"

    if any(word in q for word in [
        "relationship",
        "connected",
        "belongs",
        "service_target"
    ]):
        return "graphrag"

    if any(word in q in word in [
        "document",
        "pdf",
        "notes",
        "uploaded",
        "summarize"
    ]):
        return "rag"

    return "unknown"