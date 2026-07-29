from llama_index.retriever import load_index

def llama_index_chat(question):

    index = load_index()
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return str(question)