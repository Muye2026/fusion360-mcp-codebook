"""Fusion 360 MCP Codebook Server — main entry point.

A domain-specific MCP Server that wraps tested Fusion 360 API code snippets
as AI-callable tools. Runs as a standalone process and communicates with
frankhommers/autodesk-fusion-mcp via MCP Client.
"""

from mcp.server.fastmcp import FastMCP

from . import config

# Create the FastMCP server instance
mcp = FastMCP(
    "Fusion 360 Codebook",
    stateless_http=True,
    json_response=True,
    host=config.HOST,
    port=config.PORT,
)


# Import and register all tool modules
# Each module uses `from server.main import mcp` to register its tools
from .tools import basic_shapes  # noqa: F401
from .tools import features  # noqa: F401
from .tools import transforms  # noqa: F401
from .tools import surfaces  # noqa: F401
from .tools import assembly  # noqa: F401
from .tools import export  # noqa: F401
from .tools import passthrough  # noqa: F401


def main():
    """Start the MCP server."""
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
