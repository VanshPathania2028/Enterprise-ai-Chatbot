from mcp.server.fastmcp import FastMCP

from utils.logger import logger

# Create MCP Server
mcp = FastMCP("Enterprise AI Chatbot MCP Server")


@mcp.tool()
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    """

    logger.info(f"MCP Tool Executed: calculator")
    logger.info(f"Expression: {expression}")

    try:
        result = eval(expression)

        logger.info(f"Result: {result}")

        return str(result)

    except Exception as e:

        logger.exception("Calculator Tool Error")

        return str(e)


@mcp.tool()
def chatbot(question: str) -> str:
    """
    Chat with the AI model.
    """

    logger.info("MCP Tool Executed: chatbot")
    logger.info(f"Question: {question}")

    try:

        from llm.ollama_client import generate_response

        answer = generate_response(question)

        logger.info("Chatbot response generated successfully.")

        return answer

    except Exception:

        logger.exception("Chatbot Tool Error")

        raise


@mcp.tool()
def graph_search(entity: str):
    """
    Search Neo4j Graph.
    """

    logger.info("MCP Tool Executed: graph_search")
    logger.info(f"Entity: {entity}")

    try:

        from graphrag.retriever import graph_search

        result = graph_search(entity)

        logger.info(f"Graph returned {len(result)} records.")

        return result

    except Exception:

        logger.exception("Graph Search Error")

        raise


@mcp.tool()
def health():
    """
    MCP Health Check.
    """

    logger.info("Health endpoint called.")

    return {
        "status": "healthy",
        "server": "Enterprise MCP",
        "llm": "Ollama",
        "graph": "Neo4j",
        "vectorstore": "ChromaDB"
    }


if __name__ == "__main__":

    logger.info("Starting MCP Server...")

    mcp.run()