from embeddings.embedding_model import create_embeddings
embeddings = create_embeddings([
    "Demand is growing due to",
    "AI adoption in healthcare is  also"
])
print(len(embeddings))
print(len(embeddings[0]))