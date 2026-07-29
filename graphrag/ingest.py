from rag.loader import load_pdf
from rag.chunking import chunk_text
from graphrag.extractor import extract_entities
from graphrag.builder import build_graph

def ingest_document(pdf_path):
    print("Loading PDF...")
    text = load_pdf(pdf_path)
    print("Chunking document...")
    chunks = chunk_text(text)
    print(f"Total Chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks):
        print(f"Processing Chunk {index + 1}")
        graph = extract_entities(chunk)
        build_graph(graph)

    print("GraphRAG Ingestion complete")