import chromadb

from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext

def load_index():
    client = chromadb.PersistentClient(
        path="vectorstore/chroma/db"
    )
    
    collection = client.get_or_create_collection(
        "documents"
    )

    vector_store = ChromaVectorStore(
        chroma_collection=collection
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store
    )

    return index
