from agent_workflow.workflow import graph

result = graph.invoke(
    {
        "question": "What is Artificial Intelligence?"
    }
)
print(result["answer"])

