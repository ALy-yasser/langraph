from mcp.server.fastmcp import FastMCP


mcp = FastMCP("maths")


@mcp.tool()
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
async def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b


@mcp.tool()
async def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


@mcp.tool()
async def divide(a: int, b: int) -> int:
    """Divide two numbers"""
    return a / b


# The transport="stdio" argument tells the server to:
# Use standard input/output (stdin and stdout) to receive and respond to tool function calls

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
