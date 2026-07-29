from pathlib import Path

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


CHROMA_DIRECTORY = "chroma_db"
COLLECTION_NAME = "enterprise_documents"

client = chromadb.PersistentClient(
    path=CHROMA_DIRECTORY
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    # The model is part of the local runtime cache. Avoid a startup-time
    # Hugging Face request, which otherwise makes uploads fail offline.
    local_files_only=True,
)


def extract_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def split_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 100,
):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def ingest_pdf(file_path: str):
    path = Path(file_path)

    text = extract_pdf_text(file_path)

    if not text.strip():
        raise ValueError(
            "No readable text was found in the PDF."
        )

    chunks = split_text(text)

    embeddings = embedding_model.encode(
        chunks
    ).tolist()

    document_ids = [
        f"{path.name}_{index}"
        for index in range(len(chunks))
    ]

    metadata = [
        {
            "source": path.name,
            "original_filename": path.name,
            "chunk": index,
        }
        for index in range(len(chunks))
    ]

    collection.add(
        ids=document_ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata,
    )

    return {
        "filename": path.name,
        "chunks_added": len(chunks),
    }


def delete_document_from_vectorstore(
    filename: str,
):
    results = collection.get(
        where={
            "source": filename,
        }
    )

    document_ids = results.get("ids", [])

    if document_ids:
        collection.delete(
            ids=document_ids
        )

    return {
        "filename": filename,
        "chunks_deleted": len(document_ids),
    }

def search_documents(
    query: str,
    number_of_results: int = 4,
):
    query_embedding = embedding_model.encode(
        [query]
    ).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=number_of_results,
    )

    documents = results.get(
        "documents",
        [[]],
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]],
    )[0]

    retrieved_chunks = []

    for index, document in enumerate(documents):
        metadata = {}

        if index < len(metadatas):
            metadata = metadatas[index] or {}

        retrieved_chunks.append(
            {
                "content": document,
                "source": metadata.get(
                    "source",
                    "unknown",
                ),
                "chunk": metadata.get(
                    "chunk",
                    index,
                ),
            }
        )

    return retrieved_chunks
