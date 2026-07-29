"""
MCP server for Enterprise AI Chatbot.

This server registers tool implementations (calculator, file_reader, database)
as MCP-compatible tools using the FastMCP framework.
"""
import sys

from mcp.server.fastmcp import FastMCP
from tools.calculator import calculate
from tools.file_reader import read_file
from tools.database import query_database

mcp = FastMCP("Enterprise AI Chatbot")

TOOL_REGISTRY = {
    "calculator": calculate,
    "file_reader": read_file,
    "database": query_database,
}


def execute_tool(tool_name: str, *args, **kwargs):
    """
    Execute a tool by name and return its result.
    Used by test_server.py and the tool router.
    """
    tool_func = TOOL_REGISTRY.get(tool_name)
    if not tool_func:
        return (
            f"Error: Unknown tool '{tool_name}'."
            f" Available tools: {', '.join(TOOL_REGISTRY.keys())}"
        )
    return tool_func(*args, **kwargs)


@mcp.tool()
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    """
    return calculate(expression)


@mcp.tool()
def read_file_tool(path: str) -> str:
    """
    Read a text file.
    """
    return read_file(path)


@mcp.tool()
def query_database_tool(query: str) -> str:
    """
    Execute a SQLite query.
    """
    return query_database(query)


if __name__ == "__main__":
    # The MCP stdio protocol reserves stdout for JSON-RPC messages.
    print("Enterprise AI Chatbot MCP Server started.", file=sys.stderr)

    mcp.run()
