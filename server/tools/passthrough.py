"""Passthrough MCP Tools — direct access to Fusion 360 Python API.

Provides execute_python and capture_viewport as universal tools.
execute_python is the primary "do anything" tool — for operations not covered
by the domain-specific tools (basic_shapes, features, etc.), use this to run
arbitrary adsk.core / adsk.fusion code directly in the live Fusion 360 session.
"""

from pydantic import Field

from server.app import mcp
from server.bridge import bridge


# ─── execute_python (universal tool) ──────────────────────────────

@mcp.tool()
async def execute_python(
    code: str = Field(
        description=(
            "Python code to execute in the live Fusion 360 session. "
            "Has access to adsk.core and adsk.fusion modules. "
            "Use print() for output. Units: cm (divide mm by 10). "
            "Example: 'import adsk.core; app = adsk.core.Application.get(); "
            "print(app.name)'"
        ),
    ),
) -> str:
    """Execute arbitrary Python code directly in the live Fusion 360 session.

    This is the universal fallback tool — it can do ANYTHING the Fusion 360
    API supports. For common operations (create cube, extrude, fillet, etc.)
    prefer the domain-specific tools first. Use this for:
      - Complex multi-step modeling scripts
      - Operations not covered by dedicated tools
      - Debugging and diagnostics

    Key API notes (Fusion 360 Python API):
      - Use bRepBodies (not bodies), sketchCurves.sketchLines (not lines)
      - rootComponent (singular, not rootComponents)
      - Units are centimeters internally (mm / 10)
      - print() output is captured and returned
    """
    return await bridge.execute_python(code)


# ─── capture_viewport ─────────────────────────────────────────────

@mcp.tool()
async def capture_viewport(
    width: int = Field(default=800, description="Image width in pixels"),
    height: int = Field(default=600, description="Image height in pixels"),
) -> str:
    """Capture a screenshot of the current Fusion 360 viewport.

    Uses Fusion API's viewport.saveAsScreenshot() via execute_python.
    Returns the file path of the saved image.
    """
    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
viewport = app.activeViewport
filepath = "/tmp/fusion_viewport.png"
viewport.saveAsScreenshot(filepath, {width}, {height})
print(f"Screenshot saved: {{filepath}}")
'''
    return await bridge.execute_python(code)
