"""Export MCP Tools — 4 domain-specific tools for export operations.

Each tool generates Python code based on tested codebook patterns,
and executes via FusionBridge.
"""

from pydantic import Field

from server.main import mcp
from server.bridge import bridge


# ─── export_step ────────────────────────────────────────────────────────

@mcp.tool()
async def export_step(
    filepath: str = Field(default="/tmp/export.step", description="Output file path"),
    body_index: int = Field(default=-1, description="Body index to export (-1 for entire component)"),
) -> str:
    """Export the current design (or a specific body) to a STEP file in Fusion 360.

    Uses createSTEPExportOptions(filepath, component) for component export.
    """
    if body_index >= 0:
        export_code = f'''body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    exportMgr = design.exportManager
    stepOptions = exportMgr.createSTEPExportOptions("{filepath}", rootComp)
    result = exportMgr.execute(stepOptions)
    if result:
        print(f"STEP export succeeded: {filepath}")
    else:
        print("ERROR: STEP export failed")'''
    else:
        export_code = f'''exportMgr = design.exportManager
stepOptions = exportMgr.createSTEPExportOptions("{filepath}", rootComp)
result = exportMgr.execute(stepOptions)
if result:
    print(f"STEP export succeeded: {filepath}")
else:
    print("ERROR: STEP export failed")'''

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

{export_code}
'''
    return await bridge.execute_python(code)


# ─── export_stl ────────────────────────────────────────────────────────

@mcp.tool()
async def export_stl(
    filepath: str = Field(default="/tmp/export.stl", description="Output file path"),
    body_index: int = Field(default=0, description="Index of the body to export (0-based). STL exports BRepBody, not Component."),
) -> str:
    """Export a body to an STL file in Fusion 360.

    IMPORTANT: createSTLExportOptions requires a BRepBody object, NOT a Component.
    Pass rootComp.bRepBodies.item(index) instead of rootComp.
    """
    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    exportMgr = design.exportManager
    stlOptions = exportMgr.createSTLExportOptions(body, "{filepath}")
    result = exportMgr.execute(stlOptions)
    if result:
        print(f"STL export succeeded: {filepath} (body: {body.name})")
    else:
        print("ERROR: STL export failed")
'''
    return await bridge.execute_python(code)


# ─── export_iges ────────────────────────────────────────────────────────

@mcp.tool()
async def export_iges(
    filepath: str = Field(default="/tmp/export.iges", description="Output file path"),
) -> str:
    """Export the current design to an IGES file in Fusion 360.

    Uses createIGESExportOptions(filepath, component), same pattern as STEP.
    """
    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

exportMgr = design.exportManager
igesOptions = exportMgr.createIGESExportOptions("{filepath}", rootComp)
result = exportMgr.execute(igesOptions)
if result:
    print(f"IGES export succeeded: {filepath}")
else:
    print("ERROR: IGES export failed")
'''
    return await bridge.execute_python(code)


# ─── mass_properties ───────────────────────────────────────────────────

@mcp.tool()
async def mass_properties(
    body_index: int = Field(default=0, description="Index of the body to query (0-based)"),
) -> str:
    """Get physical properties (mass, volume, area, density) of a body in Fusion 360.

    Uses body.physicalProperties to retrieve mass, volume, area, density, and center of mass.
    """
    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    props = body.physicalProperties
    if props:
        print(f"Body: {body.name}")
        print(f"Mass: {props.mass} kg")
        print(f"Volume: {props.volume} cm3")
        print(f"Area: {props.area} cm2")
        print(f"Density: {props.density} kg/cm3")
        center = props.centerOfMass
        print(f"Center of Mass: ({center.x}, {center.y}, {center.z})")
    else:
        print("ERROR: Failed to get physical properties")
'''
    return await bridge.execute_python(code)
