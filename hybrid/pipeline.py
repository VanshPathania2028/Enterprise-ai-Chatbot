import time
from rag.pipeline import rag_chat
from graphrag.pipeline import graphrag_chat
from llama_index.pipeline import llama_index_chat
from llm.provider import generate_response
from reranker.rerank import rerank
from memory.store import memory
from logs.logger import logger



def hybrid_chat(question):

    start_time = time.time()

    try:

        logger.info(f"Hybrid Question: {question}")
        rag_result = rag_chat(question)
        logger.info(f"RAG Result: {rag_result}")

        # GraphRAG depends on Neo4j. Keep the chatbot available when the
        # graph database is unavailable or its credentials need attention.
        try:
            graph_result = graphrag_chat(question)
            logger.info(f"GraphRAG result: {graph_result}")
        except Exception:
            logger.exception(
                "GraphRAG is unavailable; continuing with the remaining retrieval pipelines."
            )
            graph_result = ""

        # LlamaIndex may require separately configured embedding providers.
        # Do not prevent a normal RAG + Ollama answer when it is unavailable.
        try:
            llama_result = llama_index_chat(question)
            logger.info(f"LlamaIndex Result: {llama_result}")
        except Exception:
            logger.exception(
                "LlamaIndex is unavailable; continuing with the remaining retrieval pipelines."
            )
            llama_result = ""

        results = [result for result in (rag_result, graph_result, llama_result) if result]
        best_results = rerank(question, results)
        context = "\n\n".join(best_results)

        logger.info("Reranking completed successfully.")
        history = memory.get_history()
        history_text = "".join(
            f"{item['role']}: {item['message']}\n" for item in history
        )

        prompt = f"""
You are an intelligent AI assistant.

Use both the previous conversation and the retrieved context to answer the user's question.

Conversation History:
{history_text}

Retrieved Context:
{context}

Current_Question:
{question}

Provide a clear, accurate and complete answer.
"""

        answer = generate_response(prompt)
        memory.add("user", question)
        memory.add("assistant", answer)
        logger.info(f"Final Answer: {answer}")
        elapsed = time.time() - start_time
        logger.info(f"Response Time: {elapsed:.2f} seconds")
        return answer

    except Exception as e:

        logger.error(f"Hybrid Pipeline Error: {str(e)}")
        return "An error occured while processing your request."


    
 


  
