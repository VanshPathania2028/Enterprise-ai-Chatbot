import asyncio

from mcp_tools.connection import connection
from mcp_tools.client import client


async def main():

    await connection.connect()

    tools = await client.list_tools()
    print("Available_Tools:")
    print(tools)

    result = await client.call_tool(
        "calculate",
        {
            "expression": "100+200"
        }
    )
    print(result)

    await connection.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

