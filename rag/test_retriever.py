from rag.retriever import retrieve
question = "What is Artificial Intelligence?"
results = retrieve(question)
print("\nRetrieved Chunks:\n")
for i, chunk in enumerate(results, start=1):
    print(f"Chunk {i}")
    print("-" * 40)
    print(chunk)
    print()