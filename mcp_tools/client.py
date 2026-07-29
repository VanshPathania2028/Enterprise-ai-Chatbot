import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class MCPClient:

    SERVER_PARAMS = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    async def list_tools(self):

        async with stdio_client(self.SERVER_PARAMS) as (read_stream, write_stream):

            async with ClientSession(read_stream, write_stream) as session:

                await session.initialize()

                tools = await session.list_tools()

                return [tool.name for tool in tools.tools]

    async def call_tool(self, tool_name, arguments):

        async with stdio_client(self.SERVER_PARAMS) as (read_stream, write_stream):

            async with ClientSession(read_stream, write_stream) as session:

                await session.initialize()

                return await session.call_tool(tool_name, arguments)


client = MCPClient()

