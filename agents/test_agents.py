from agents.planner import planner_agent
from agents.retriever import retrieval_agent
from agents.answer_agent import answer_agent

question = "What is Machine Learning?"
plan = planner_agent(question)

print("Selected Route:", plan["route"])

context = retrieval_agent(
    plan["route"],
    question
)

print("\nRetrieved Context:\n")
print(context)

answer = answer_agent(
        question,
        context
)

print("\nFinal Answer:\n")
print(answer)