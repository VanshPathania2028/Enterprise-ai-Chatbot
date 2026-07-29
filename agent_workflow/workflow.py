from langgraph.graph import StateGraph, END
from agent_workflow.state import ChatState
from agent_workflow.nodes import llm_node

workflow = StateGraph(ChatState)
workflow.add_node("chat", llm_node)
workflow.set_entry_point("chat")
workflow.add_edge("chat", END)
graph = workflow.compile()

