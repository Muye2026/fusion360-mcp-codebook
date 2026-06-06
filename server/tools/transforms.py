"""Transforms MCP Tools — 4 domain-specific tools for transform operations.

Each tool generates Python code based on tested codebook patterns,
and executes via FusionBridge.
"""

import math
from pydantic import Field

from server.app import mcp
from server.bridge import bridge
from server import config


# ─── circular_pattern ──────────────────────────────────────────────────

@mcp.tool()
async def circular_pattern(
    body_index: int = Field(default=0, description="Index of the body to pattern (0-based)"),
    quantity: int = Field(default=4, description="Number of instances"),
    total_angle_deg: float = Field(default=360, description="Total angle in degrees"),
) -> str:
    """Create a circular pattern of a body around the Z axis in Fusion 360.

    Patterns the body (not feature) using circularPatternFeatures.
    """
    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    entities_coll = adsk.core.ObjectCollection.createWithArray([body])
    z_axis = rootComp.zConstructionAxis
    circPatterns = rootComp.features.circularPatternFeatures
    circInput = circPatterns.createInput(entities_coll, z_axis)
    circInput.quantity = adsk.core.ValueInput.createByReal({quantity})
    circInput.totalAngle = adsk.core.ValueInput.createByString('{total_angle_deg} deg')
    circInput.isSymmetric = False
    circPattern = circPatterns.add(circInput)
    print(f"Circular pattern created: {quantity}x at {total_angle_deg} deg")
'''
    return await bridge.execute_python(code)


# ─── rectangular_pattern ───────────────────────────────────────────────

@mcp.tool()
async def rectangular_pattern(
    body_index: int = Field(default=0, description="Index of the body to pattern (0-based)"),
    qty1: int = Field(default=2, description="Number of instances in direction 1"),
    qty2: int = Field(default=2, description="Number of instances in direction 2"),
    dist1: float = Field(default=20, description="Spacing in direction 1 in mm"),
    dist2: float = Field(default=20, description="Spacing in direction 2 in mm"),
) -> str:
    """Create a rectangular pattern of a body in Fusion 360.

    Uses X and Y construction axes as directions. Distance uses PatternDistanceType.SpacingPatternDistanceType.
    All dimensions are in millimeters.
    """
    d1_cm = dist1 * config.MM_TO_CM
    d2_cm = dist2 * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    entities_coll = adsk.core.ObjectCollection.createWithArray([body])
    x_axis = rootComp.xConstructionAxis
    y_axis = rootComp.yConstructionAxis
    rectPatterns = rootComp.features.rectangularPatternFeatures
    rectInput = rectPatterns.createInput(
        entities_coll,
        x_axis,
        adsk.core.ValueInput.createByReal({qty1}),
        adsk.core.ValueInput.createByReal({d1_cm}),
        adsk.fusion.PatternDistanceType.SpacingPatternDistanceType
    )
    rectInput.setDirectionTwo(
        y_axis,
        adsk.core.ValueInput.createByReal({qty2}),
        adsk.core.ValueInput.createByReal({d2_cm})
    )
    rectPattern = rectPatterns.add(rectInput)
    print(f"Rectangular pattern created: {qty1}x{qty2} at ({dist1},{dist2})mm spacing")
'''
    return await bridge.execute_python(code)


# ─── mirror_bodies ─────────────────────────────────────────────────────

@mcp.tool()
async def mirror_bodies(
    body_index: int = Field(default=0, description="Index of the body to mirror (0-based)"),
    mirror_plane: str = Field(default="YZ", description="Mirror plane: 'XY', 'XZ', or 'YZ'"),
) -> str:
    """Mirror a body across a construction plane in Fusion 360.

    Wraps body in ObjectCollection before passing to mirrorFeatures.createInput().
    """
    plane_map = {"XY": "xYConstructionPlane", "XZ": "xZConstructionPlane", "YZ": "yZConstructionPlane"}
    plane_attr = plane_map.get(mirror_plane, "yZConstructionPlane")

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    entities_coll = adsk.core.ObjectCollection.create()
    entities_coll.add(body)
    plane = rootComp.{plane_attr}
    mirrorFeats = rootComp.features.mirrorFeatures
    mirrorInput = mirrorFeats.createInput(entities_coll, plane)
    mirror = mirrorFeats.add(mirrorInput)
    print(f"Mirror created: body {body.name} across {mirror_plane} plane")
'''
    return await bridge.execute_python(code)


# ─── rotate_body ────────────────────────────────────────────────────────

@mcp.tool()
async def rotate_body(
    body_index: int = Field(default=0, description="Index of the body to rotate (0-based)"),
    angle_deg: float = Field(default=45, description="Rotation angle in degrees"),
    axis: str = Field(default="Z", description="Rotation axis: 'X', 'Y', or 'Z'"),
) -> str:
    """Rotate a body around an axis in Fusion 360.

    Uses MoveFeatures with Matrix3D.setToRotation(). Angle is in degrees.
    """
    axis_vec = {"X": "1, 0, 0", "Y": "0, 1, 0", "Z": "0, 0, 1"}
    axis_str = axis_vec.get(axis, "0, 0, 1")
    angle_rad = angle_deg * math.pi / 180.0

    code = f'''import adsk.core, adsk.fusion, math
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    axis = adsk.core.Vector3D.create({axis_str})
    origin = adsk.core.Point3D.create(0, 0, 0)
    matrix = adsk.core.Matrix3D.create()
    matrix.setToRotation({angle_rad}, axis, origin)
    bodies_coll = adsk.core.ObjectCollection.create()
    bodies_coll.add(body)
    moveFeats = rootComp.features.moveFeatures
    moveInput = moveFeats.createInput(bodies_coll, matrix)
    move = moveFeats.add(moveInput)
    print(f"Rotated body {body.name} by {angle_deg} deg around {axis} axis")
'''
    return await bridge.execute_python(code)
