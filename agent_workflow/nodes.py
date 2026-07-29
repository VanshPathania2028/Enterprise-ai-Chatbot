from chatbot.chatbot import chat
from rag.pipeline import rag_chat

def llm_node(state):
    question = state["question"]
    answer = chat(question)
    return {
        "answer": answer
    }

def rag_node(state):
    question = state["question"]
    answer = rag_chat(question)
    return {
        "answer": answer
    }

