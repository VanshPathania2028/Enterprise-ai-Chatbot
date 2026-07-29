"""Test the mcp_server.py module loads and the tools work."""
import sys
import importlib.util

# Load mcp_server.py
spec = importlib.util.spec_from_file_location('mcp_server', 'mcp_server.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

print("OK: mcp_server.py loaded")

# Test calculator
result = mod.calculator("2+3")
print(f"OK: calculator('2+3') = {result}")
assert result == "5", f"Expected '5', got {result}"

# Test file_reader
content = mod.read_file_tool("requirements.txt")
print(f"OK: read_file_tool('requirements.txt') = {repr(content[:50])}...")
assert len(content) > 0, "Expected content"

# Test execute_tool
result = mod.execute_tool("calculator", "10*5")
print(f"OK: execute_tool('calculator', '10*5') = {result}")
assert result == "50", f"Expected '50', got {result}"

result = mod.execute_tool("file_reader", "requirements.txt")
print(f"OK: execute_tool('file_reader', 'requirements.txt') = content present")
assert len(result) > 0

# Test unknown tool
result = mod.execute_tool("nonexistent", "")
print(f"OK: execute_tool('nonexistent') = {result[:30]}...")

print("ALL TESTS PASSED!")

