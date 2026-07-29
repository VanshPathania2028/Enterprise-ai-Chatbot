from embeddings.embedding_model import create_embeddings
from vectorstore.db import search_documents

def retrieve(query):
    query_embedding = create_embeddings([query])[0]
    documents = search_documents(query_embedding)
    return documents
