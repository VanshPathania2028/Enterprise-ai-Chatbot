from llama_index.core import VectorStoreIndex
from llama_index.core.schema import Document

from llama_index.config import EMBED_MODEL

def build_index(text):
    document = Document(text=text)

    index = VectorStoreIndex.from_documents(
        [document],
        embed_model=EMBED_MODEL
    )
    return index
