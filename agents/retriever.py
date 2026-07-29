from rag.pipeline import rag_chat
from graphrag.pipeline import graphrag_chat
from llama_index.pipeline import llama_index_chat
from hybrid.pipeline import hybrid_chat

def retrieval_agent(route, question):

    if route == "rag":
        return rag_chat(question)

    elif route == "graphrag":
        return graphrag_chat(question)

    elif route == "llamaindex":
        return llama_index_chat(question)

    elif route == "hybrid":
        return hybrid_chat(question)

    return None
