from llama_index.index_builder import build_index
from llama_index.ingest import ingest_text
from llama_index.pipeline import llama_index_chat

text = """
Artificial Intelligence enable computers
to learn from data and solve problems.

Machine Learning is a subset of Artificial Intelligence.

Deep Learning is a subset of Machine Learning.
"""
print("Creating Index...")

ingest_text(text)
print("Index created successfully.")
question = "What is Machine Learning?"
print("\nQuestion:", question)

response = llama_index_chat(question)
print("\nAnswer:")
print(response)