from mcp_tools.tool_executor import execute
from logs.logger import logger
def tool_agent(question):
    arguments = {}

    if "calculate" in question.lower():

        arguments["expression"] = (
            question
            .replace("calculate", "")
            .strip()
        )

    return execute(question, arguments)

    logger.info(f"Executing Tool for: {question}")
    logger.info(f"Final Answer: {answer}")
