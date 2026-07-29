import sys
import os

# Add project root so mcp_server module can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mcp_server import execute_tool

print(execute_tool("calculator", "456*87"))
print(execute_tool("file_reader", "requirements.txt"))
