import requests

from config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)

from rag.ingest import search_documents


def build_context(chunks):
    context_parts = []

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):
        source = chunk.get(
            "source",
            "unknown",
        )

        content = chunk.get(
            "content",
            "",
        )

        context_parts.append(
            (
                f"Source {index}: {source}\n"
                f"{content}"
            )
        )

    return "\n\n".join(context_parts)


def rag_chat(message: str):
    chunks = search_documents(
        message,
        number_of_results=4,
    )

    context = build_context(chunks)

    if not context.strip():
        context = (
            "No relevant uploaded document "
            "context was found."
        )

    prompt = f"""
You are an enterprise AI assistant.

Answer the user's question using the provided document context.

Rules:
1. Use the document context as the primary source when it is relevant.
2. If the context is missing or unrelated to the question, answer using your
   general knowledge instead of refusing the question.
3. Clearly distinguish document-based facts from general knowledge when that
   distinction matters.
4. Do not claim that a fact came from an uploaded document unless it did.
5. Mention the source filename when useful.
6. Give a clear and concise answer.

Document context:

{context}

User question:

{message}

Answer:
""".strip()

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    answer = data.get(
        "response",
        "",
    ).strip()

    if not answer:
        raise ValueError(
            "Ollama returned an empty response."
        )

    return {
        "answer": answer,
        "sources": [
            {
                "filename": chunk.get(
                    "source",
                    "unknown",
                ),
                "chunk": chunk.get(
                    "chunk",
                ),
            }
            for chunk in chunks
        ],
    }
