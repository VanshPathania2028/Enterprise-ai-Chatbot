from graphrag.retriever import graph_search
from llm.provider import generate_response
from graphrag.question_parser import extract_entity


def graphrag_chat(question: str):

    """
    Answer a question using GraphRAG.
    """

    entity = extract_entity(question)

    graph_results = graph_search(entity)
    entity = question

    graph = graph_search(entity)

    if not graph_results:
        return "No relevant information found in the knowledge graph."

    context = ""

    for record in graph_results:
        context += {
            f"{record['source']}"
            f"{record['relation']}"
            f"{record['target']}\n"
        }

    prompt = f"""
You are an AI assistant.

Use ONLY the graph information below to answer the user's question.

Graph Information:
{context}

Question:
{question}

Answer:
"""

    answer = generate_response(prompt)

    return answer