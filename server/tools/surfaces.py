"""Surfaces MCP Tools — 6 domain-specific tools for surface operations.

Each tool generates Python code based on tested codebook patterns,
and executes via FusionBridge.
"""

from pydantic import Field

from server.main import mcp
from server.bridge import bridge
from server import config


# ─── create_sweep ───────────────────────────────────────────────────────

@mcp.tool()
async def create_sweep(
    profile_radius: float = Field(default=5, description="Radius of the circular cross-section in mm"),
    path_length: float = Field(default=100, description="Length of the sweep path along X axis in mm"),
    name: str = Field(default="SweepTube", description="Body name"),
) -> str:
    """Create a sweep tube by sweeping a circular profile along a straight path in Fusion 360.

    Profile is on YZ plane (perpendicular to X-axis path).
    Path is created using Path.create(curve, chainedCurveOption).
    All dimensions are in millimeters.
    """
    pr = profile_radius * config.MM_TO_CM
    pl = path_length * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

profileSketch = rootComp.sketches.add(rootComp.yZConstructionPlane)
profileSketch.sketchCurves.sketchCircles.addByCenterRadius(
    adsk.core.Point3D.create(0, 0, 0), {pr}
)
profileObj = profileSketch.profiles.item(0)

pathSketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
pathLine = pathSketch.sketchCurves.sketchLines.addByTwoPoints(
    adsk.core.Point3D.create(0, {pr}, 0),
    adsk.core.Point3D.create({pl}, {pr}, 0)
)

path = adsk.fusion.Path.create(pathLine, adsk.fusion.ChainedCurveOptions.tangentChainedCurves)

sweepFeats = rootComp.features.sweepFeatures
sweepInput = sweepFeats.createInput(profileObj, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
sweepInput.orientation = adsk.fusion.SweepOrientationTypes.PerpendicularOrientationType
sweep = sweepFeats.add(sweepInput)

body = sweep.bodies.item(0)
body.name = "{name}"
print(f"Created sweep: {name} (r={profile_radius}mm, L={path_length}mm)")
'''
    return await bridge.execute_python(code)


# ─── patch_surface ─────────────────────────────────────────────────────

@mcp.tool()
async def patch_surface(
    body_index: int = Field(default=0, description="Index of the body to find edges from (0-based)"),
    face_index: int = Field(default=0, description="Index of the face to patch (0-based)"),
) -> str:
    """Create a patch surface from a face boundary in Fusion 360.

    Uses patchFeatures.createInput(boundary_curve, operation).
    """
    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    face = body.faces.item({face_index})
    if not face:
        print("ERROR: Face not found at index {face_index}")
    else:
        patchFeats = rootComp.features.patchFeatures
        patchInput = patchFeats.createInput(face, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        patch = patchFeats.add(patchInput)
        print(f"Patch created from face {face_index}")
'''
    return await bridge.execute_python(code)


# ─── offset_surface ────────────────────────────────────────────────────

@mcp.tool()
async def offset_surface(
    body_index: int = Field(default=0, description="Index of the body (0-based)"),
    face_index: int = Field(default=0, description="Index of the face to offset (0-based)"),
    distance: float = Field(default=2, description="Offset distance in mm (positive = normal direction)"),
) -> str:
    """Offset a face by a distance in Fusion 360.

    Creates a new surface body from the offset. Distance is in millimeters.
    """
    d = distance * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    face = body.faces.item({face_index})
    if not face:
        print("ERROR: Face not found at index {face_index}")
    else:
        faces_coll = adsk.core.ObjectCollection.create()
        faces_coll.add(face)
        offsetFeats = rootComp.features.offsetFeatures
        offsetInput = offsetFeats.createInput(faces_coll, adsk.core.ValueInput.createByReal({d}), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        offset = offsetFeats.add(offsetInput)
        print(f"Offset created: {distance}mm from face {face_index}")
'''
    return await bridge.execute_python(code)


# ─── thicken_surface ───────────────────────────────────────────────────

@mcp.tool()
async def thicken_surface(
    body_index: int = Field(default=0, description="Index of the surface body to thicken (0-based)"),
    thickness: float = Field(default=2, description="Thickness in mm"),
    is_symmetric: bool = Field(default=False, description="Add thickness symmetrically"),
) -> str:
    """Thicken a surface body to create a solid in Fusion 360.

    Uses thickenFeatures.createInput(). Thickness is in millimeters.
    """
    t = thickness * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    bodies_coll = adsk.core.ObjectCollection.create()
    bodies_coll.add(body)
    thickenFeats = rootComp.features.thickenFeatures
    thickenInput = thickenFeats.createInput(bodies_coll, adsk.core.ValueInput.createByReal({t}), {str(is_symmetric)}, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    thicken = thickenFeats.add(thickenInput)
    print(f"Thicken created: {thickness}mm on body {body.name}")
'''
    return await bridge.execute_python(code)


# ─── stitch_surface ─────────────────────────────────────────────────────

@mcp.tool()
async def stitch_surface(
    body_indices: list = Field(description="List of surface body indices to stitch (0-based)"),
    tolerance: float = Field(default=0.1, description="Stitching tolerance in mm"),
) -> str:
    """Stitch multiple surface bodies together in Fusion 360.

    Uses stitchFeatures.createInput(). Tolerance is in millimeters.
    """
    t = tolerance * config.MM_TO_CM
    indices_str = str(body_indices)

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

bodies_coll = adsk.core.ObjectCollection.create()
for idx in {indices_str}:
    b = rootComp.bRepBodies.item(idx)
    if b:
        bodies_coll.add(b)

if bodies_coll.count < 2:
    print("ERROR: Need at least 2 bodies to stitch")
else:
    stitchFeats = rootComp.features.stitchFeatures
    stitchInput = stitchFeats.createInput(bodies_coll, adsk.core.ValueInput.createByReal({t}), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    stitch = stitchFeats.add(stitchInput)
    print(f"Stitch created: {len(body_indices)} bodies, tolerance={tolerance}mm")
'''
    return await bridge.execute_python(code)


# ─── trim_surface ──────────────────────────────────────────────────────

@mcp.tool()
async def trim_surface(
    body_index: int = Field(default=0, description="Index of the surface body to trim (0-based)"),
    trim_plane: str = Field(default="YZ", description="Trim tool plane: 'XY', 'XZ', or 'YZ'"),
    keep_all_cells: bool = Field(default=True, description="Keep all cells after trimming"),
) -> str:
    """Trim a surface with a construction plane in Fusion 360.

    Selects cells on trimInput.bRepCells before adding the feature.
    """
    plane_map = {"XY": "xYConstructionPlane", "XZ": "xZConstructionPlane", "YZ": "yZConstructionPlane"}
    plane_attr = plane_map.get(trim_plane, "yZConstructionPlane")

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    trim_tool = rootComp.{plane_attr}
    trimFeats = rootComp.features.trimFeatures
    trimInput = trimFeats.createInput(trim_tool)
    cells = trimInput.bRepCells
    if {str(keep_all_cells)}:
        for i in range(cells.count):
            cells.item(i).isSelected = True
    else:
        if cells.count > 0:
            cells.item(0).isSelected = True
    trim = trimFeats.add(trimInput)
    print(f"Trim created: body {body.name} with {trim_plane} plane")
'''
    return await bridge.execute_python(code)
