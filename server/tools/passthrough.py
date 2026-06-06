"""Passthrough MCP Tools — transparent proxy to frankhommers upstream tools.

Provides execute_python and capture_viewport as passthrough tools
for advanced users who need direct Fusion 360 API access.
"""

from pydantic import Field

from server.main import mcp
from server.bridge import bridge


# ─── execute_python (passthrough) ──────────────────────────────────────

@mcp.tool()
async def execute_python(
    code: str = Field(description="Python code to execute in the live Fusion 360 session. Has access to adsk.core and adsk.fusion modules."),
) -> str:
    """Execute arbitrary Python code in the live Fusion 360 session.

    Passthrough to frankhommers execute_python. Use for advanced operations
    not covered by the domain-specific tools. Has full access to adsk.core and adsk.fusion.
    """
    return await bridge.execute_python(code)


# ─── capture_viewport (passthrough) ────────────────────────────────────

@mcp.tool()
async def capture_viewport(
    width: int = Field(default=800, description="Image width in pixels"),
    height: int = Field(default=600, description="Image height in pixels"),
) -> str:
    """Capture a screenshot of the Fusion 360 viewport.

    Passthrough to frankhommers capture_viewport tool.
    """
    return await bridge.call_tool("capture_viewport", {"width": width, "height": height})
