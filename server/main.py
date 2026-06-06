"""Muye Fusion Gateway — main entry point.

A MCP Gateway that bridges AI clients (WorkBuddy, Claude Desktop, etc.)
to Fusion 360 via FusionMCP (fozzfut).

Architecture: 35+ hand-crafted domain tools + execute_python passthrough.
The hand-crafted tools cover common operations (basic shapes, features,
transforms, surfaces, assembly, export). For anything else, use
execute_python to run arbitrary Fusion 360 Python API code.

Transport: Streamable HTTP on :8000/mcp
Upstream: FusionMCP HTTP JSON on :7432
"""

from .app import mcp

# Import and register all tool modules
# Each module uses `from server.app import mcp` to register its tools
from .tools import basic_shapes  # noqa: F401  — create_cube, create_cylinder, etc.
from .tools import features       # noqa: F401  — extrude, fillet, chamfer, hole, etc.
from .tools import transforms     # noqa: F401  — move, rotate, scale, mirror, etc.
from .tools import surfaces       # noqa: F401  — offset, thicken, sweep, loft, etc.
from .tools import assembly       # noqa: F401  — component, joint, contact_set
from .tools import export         # noqa: F401  — STEP, STL, IGES export
from .tools import passthrough    # noqa: F401  — execute_python, capture_viewport


def main():
    """Start the MCP server."""
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
