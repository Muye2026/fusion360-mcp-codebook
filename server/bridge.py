"""FusionBridge — communicates with frankhommers MCP Server via MCP Client."""

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from . import config


class FusionBridge:
    """Encapsulates communication with the upstream frankhommers MCP Server.

    Each call creates a new MCP Client session (stateless, simple, reliable).
    """

    def __init__(self, upstream_url: str | None = None):
        self.upstream_url = upstream_url or config.UPSTREAM_URL

    async def execute_python(self, code: str) -> str:
        """Execute Python code in the live Fusion 360 session via frankhommers.

        Args:
            code: Python code string to execute. Has access to adsk.core and adsk.fusion.

        Returns:
            The result text from frankhommers, or an error message.
        """
        try:
            async with streamable_http_client(self.upstream_url) as (read_stream, write_stream, _):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("execute_python", {"code": code})
                    # Extract text content from result
                    if result.content:
                        parts = []
                        for item in result.content:
                            if hasattr(item, "text"):
                                parts.append(item.text)
                        return "\n".join(parts) if parts else str(result)
                    return str(result)
        except Exception as e:
            return f"[FusionBridge Error] Failed to reach frankhommers at {self.upstream_url}: {e}"

    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """Call an arbitrary tool on the upstream frankhommers MCP Server.

        Args:
            tool_name: Name of the frankhommers tool to call.
            arguments: Arguments to pass to the tool.

        Returns:
            The result text, or an error message.
        """
        try:
            async with streamable_http_client(self.upstream_url) as (read_stream, write_stream, _):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, arguments)
                    if result.content:
                        parts = []
                        for item in result.content:
                            if hasattr(item, "text"):
                                parts.append(item.text)
                        return "\n".join(parts) if parts else str(result)
                    return str(result)
        except Exception as e:
            return f"[FusionBridge Error] Failed to call {tool_name}: {e}"

    async def health_check(self) -> bool:
        """Check if the upstream frankhommers MCP Server is reachable.

        Returns:
            True if reachable, False otherwise.
        """
        try:
            async with streamable_http_client(self.upstream_url) as (read_stream, write_stream, _):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    return True
        except Exception:
            return False


# Global singleton instance
bridge = FusionBridge()
