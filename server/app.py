"""Shared FastMCP server instance — avoids circular import issues.

All tool modules should import `mcp` from here, not from `server.main`.
This ensures every module references the exact same MCP object.
"""

from mcp.server.fastmcp import FastMCP
from . import config

# Global singleton — the one true mcp instance
mcp = FastMCP(
    "Muye Fusion Gateway",
    stateless_http=True,
    json_response=True,
    host=config.HOST,
    port=config.PORT,
)
