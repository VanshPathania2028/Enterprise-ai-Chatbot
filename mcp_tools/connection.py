import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class MCPConnection:

    def __init__(self):
        self.session = None
        self.read_stream = None
        self.write_stream = None
        self._manager = None

    async def connect(self):

        server = StdioServerParameters(
            command=sys.executable,
            args=[str(Path(__file__).resolve().parents[1] / "mcp_server.py")],
            cwd=Path(__file__).resolve().parents[1],
        )

        self._manager = stdio_client(server)

        self.read_stream, self.write_stream = await self._manager.__aenter__()

        self.session = ClientSession(
            self.read_stream,
            self.write_stream
        )

        await self.session.__aenter__()

        await self.session.initialize()

        print("Connected to MCP Server.")

    async def disconnect(self):

        if self.session:
            await self.session.__aexit__(None, None, None)

        if self._manager:
            await self._manager.__aexit__(None, None, None)

        print("Disconnected from MCP Server.")


connection = MCPConnection()

