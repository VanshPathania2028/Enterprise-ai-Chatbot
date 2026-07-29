from rag.retriever import retrieve
from llm.provider import generate_response

def rag_chat(question: str):
    retrieved_chunks = retrieve(question)
    context = "\n\n".join(retrieved_chunks)
    prompt = f"""
You are an AI assistant.
Answer ONLY using the information provided in the context below.
If the answer is not present in the context, reply:
"I couldn't find this information in the provided documents."
 
 ----------------------------------
 Context:
 {context}
------------------------------------

Question:
{question}

Answer:
"""
    return generate_response(prompt)