from llama_index.config import EMBED_MODEL

embedding = EMBED_MODEL.get_text_embedding(
    "Artificial Intelligence"
)

print(len(embedding))