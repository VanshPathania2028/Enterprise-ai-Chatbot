import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core.schema import Document

def ingest_text(text):
    client = chromadb.PersistentClient(
        path="vectorstore/chroma_db"
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

    document = Document(text=text)

    index = VectorStoreIndex.from_documents(
        [document],
        storage_context=storage_context
    )

    return index