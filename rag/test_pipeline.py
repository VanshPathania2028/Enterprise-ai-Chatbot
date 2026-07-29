from rag.pipeline import rag_chat
question = input("Ask a question: ")
response = rag_chat(question)
print("\nAnswer:\n")
print(response)