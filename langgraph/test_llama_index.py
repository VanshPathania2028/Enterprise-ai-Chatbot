from langgraph.workflow import graph

state = {
    "question": "What is Machine Learning?",
    "history": []
}

result = graph.invoke(state)
print(result["answer"])