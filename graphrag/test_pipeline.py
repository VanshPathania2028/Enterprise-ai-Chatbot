from graphrag.ingest import ingest_document
from graphrag.pipeline import graphrag_chat

ingest_document(
    "documents/E-PHARMACY & DIGITAL HEALTH PLATFORM  STRATEGIC OVERVIEW.pdf"
)
print(
    graphrag_chat(
        "OpenAI"
    )
)

question = "Who developed GPT-4?"
response = graphrag_chat(question)
print(response)