from langgraph.workflow import graph
from langgraph.memory import memory
from memory.store import memory


while True:
    question = input("\nAsk a question: ")

    if question.lower() == "exit":
        break

    if question.lower() == "clear":
        memory.clear()
        print("Conversation Cleared.")
        continue
    result = graph.invoke(
        {
            "question": question,
            "history": memory.get_history()
        }
    )
    print("\nAnswer:")
    print("\nBot:",result["answer"])