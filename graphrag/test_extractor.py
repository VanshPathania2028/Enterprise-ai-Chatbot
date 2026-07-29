from graphrag.extractor import extract_entities
from graphrag.builder import build_graph
text = """
Python was created by Guido van Rossum.
OpenAI developed GPT-4.
Sam Altman  is the CEO of OpenAI.
"""

graph = extract_entities(text)
build_graph(graph)
print("Graph created Successfully")