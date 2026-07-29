from langgraph.classifier import classify_question

questions = [
    "Calculate" 45*78,
    "Summarize my PDF",
    "What is the service target of Indian e-pharmacy market?",
    "What is Artificial Intekkigence?"
]

for q in questions:
    print(q)
    print("Route:", classify_question(q))
    print("-" * 40)