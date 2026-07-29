from langgraph.graph import StateGraph, END
from langgraph.state import ChatState
from langgraph.nodes import (
    llm_node,
    rag_node,
    graphrag_node,
    llamaindex_node,
    tool_node
)
from langgraph.router import route_question


graph = StateGraph(ChatState)
graph.add_node("llm", llm_node)
graph.add_node("rag", rag_node)
graph.add_node("graphrag", graphrag_node)
graph.add_node("tool", tool_node)
graph.add_node("llamaindex", llamaindex_node)
graph.add_node("hybrid", hybrid_node)
def router(state):
    return route_question(state["question"])


graph.set_conditional_entry_point(
    router,
    {
        "llm": "llm",
        "rag": "rag",
        "graphrag": "graphrag",
        "llamaindex" : "llamaindex",
        "hybrid" : "hybrid",
        "tool": "tool",
    },
)
graph.add_edge("llm", END)
graph.add_edge("rag", END)
graph.add_edge("graphrag", END)
graph.add_edge("tool", END)
graph.add_edge("llamaindex", END)
graph.add_edge("hybird", END)
graph = graph.compile()
