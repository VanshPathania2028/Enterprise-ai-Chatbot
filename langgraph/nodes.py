from chatbot.chatbot import chat
from rag.pipeline import rag_chat
from langgraph.router import route_question
from langgraph.memory import memory
from mcp_tools.tool_executor import execute
from llm.provider import generate_response
from graphrag.pipeline import graphrag_chat
from llama_index.pipeline import llama_index_chat
from hybrid.pipeline import hybrid_chat

def router_node(state):
    question = state["question"]
    route = route_question(question)

    return {
        "route": route
    }


def llm_node(state):
    answer = generate_response(
        state["question"]
    )
    return {
        "answer": answer
    }


def rag_node(state):
    answer = rag_chat(state["question"])
    return {"answer": answer}


def graphrag_node(state):
    answer = graphrag_chat(state["question"])
    return {"answer": answer}


def tool_node(state):
    question = state["question"]

    arguments = {}

    if "calculate" in question.lower():

        arguments["expression"] = (
            question.lower()
            .replace("calculate", "")
            .strip()
        )

    elif "read" in question.lower():

        arguments["path"] = (
            question
            .replace("read", "")
            .strip()
        )

    elif "select" in question.lower():

        arguments["query"] = question

    answer = execute(question, arguments)

    return {
        "answer": str(answer)
    }

def llamaindex_node(state):

    answer = llamaindex_chat(
        state["question"]
    )
    return{
        "answer" : answer
    }

def hybrid_node(state):
    answer = hybrid_chat(
        state=["question"]
    )
    return {"answer" : answer}