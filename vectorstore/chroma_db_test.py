from rag.loader import load_pdf
from rag.chunking import chunk_text
from embeddings.embedding_model import create_embeddings
from vectorstore.chroma_db import add_documents

text = load_pdf("documents/E-PHARMACY & DIGITAL HEALTH PLATFORM  STRATEGIC OVERVIEW.pdf")
chunks = chunk_text(text)
embeddings = create_embeddings(chunks)
add_documents(chunks, embeddings)
print("Documents stored successfully!")