import asyncio
from mcp_tools.client import client
from mcp_tools.router import select_tool


def execute(question, arguments):

    async def run():
        tools = await client.list_tools()
        tool_name = select_tool(question)
        result = await client.call_tool(tool_name, arguments)
        return result

    return asyncio.run(run())

