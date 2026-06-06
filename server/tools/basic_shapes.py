"""Basic Shapes MCP Tools — 6 domain-specific tools for creating primitive shapes.

Each tool generates Python code based on tested codebook patterns,
converts user-friendly mm parameters to Fusion API cm,
and executes via FusionBridge.
"""

from pydantic import Field

from server.main import mcp
from server.bridge import bridge
from server import config


# ─── create_cube ────────────────────────────────────────────────────────

@mcp.tool()
async def create_cube(
    width: float = Field(default=10, description="Width in mm"),
    height: float = Field(default=10, description="Height in mm"),
    depth: float = Field(default=10, description="Depth in mm"),
    name: str = Field(default="Cube", description="Body name"),
) -> str:
    """Create a parametric cube at the origin in Fusion 360.

    Creates an extruded rectangle on the XY plane.
    All dimensions are in millimeters (converted to cm internally).
    """
    w = width * config.MM_TO_CM
    h = height * config.MM_TO_CM
    d = depth * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
sketch.sketchCurves.sketchLines.addTwoPointRectangle(
    adsk.core.Point3D.create(0, 0, 0),
    adsk.core.Point3D.create({w}, {h}, 0)
)
profile = sketch.profiles.item(0)
extrudeFeats = rootComp.features.extrudeFeatures
extInput = extrudeFeats.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
distance = adsk.core.ValueInput.createByReal({d})
extInput.setDistanceExtent(False, distance)
extrude = extrudeFeats.add(extInput)
body = extrude.bodies.item(0)
body.name = "{name}"
print(f"Created cube: {name} ({width}x{height}x{depth}mm)")
'''
    return await bridge.execute_python(code)


# ─── create_cylinder ────────────────────────────────────────────────────

@mcp.tool()
async def create_cylinder(
    radius: float = Field(default=5, description="Radius in mm"),
    height: float = Field(default=20, description="Height in mm"),
    name: str = Field(default="Cylinder", description="Body name"),
) -> str:
    """Create a parametric cylinder at the origin in Fusion 360.

    Creates a circle on the XY plane and extrudes it upward.
    All dimensions are in millimeters.
    """
    r = radius * config.MM_TO_CM
    h = height * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
sketch.sketchCurves.sketchCircles.addByCenterRadius(
    adsk.core.Point3D.create(0, 0, 0), {r}
)
profile = sketch.profiles.item(0)
extrudeFeats = rootComp.features.extrudeFeatures
extrudeInput = extrudeFeats.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
distance = adsk.core.ValueInput.createByReal({h})
extrudeInput.setDistanceExtent(False, distance)
extrude = extrudeFeats.add(extrudeInput)
body = extrude.bodies.item(0)
body.name = "{name}"
print(f"Created cylinder: {name} (r={radius}mm, h={height}mm)")
'''
    return await bridge.execute_python(code)


# ─── create_sphere ──────────────────────────────────────────────────────

@mcp.tool()
async def create_sphere(
    radius: float = Field(default=5, description="Radius in mm"),
    name: str = Field(default="Sphere", description="Body name"),
) -> str:
    """Create a sphere at the origin in Fusion 360.

    Created by revolving a semi-circle 360 degrees (SphereFeatures has no add method).
    All dimensions are in millimeters.
    """
    r = radius * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

sketch = rootComp.sketches.add(rootComp.xZConstructionPlane)
axisLine = sketch.sketchCurves.sketchLines.addByTwoPoints(
    adsk.core.Point3D.create(0, {-r}, 0),
    adsk.core.Point3D.create(0, {r}, 0)
)
arc = sketch.sketchCurves.sketchArcs.addByThreePoints(
    adsk.core.Point3D.create({-r}, 0, 0),
    adsk.core.Point3D.create(0, {r}, 0),
    adsk.core.Point3D.create({r}, 0, 0)
)
sketch.sketchCurves.sketchLines.addByTwoPoints(
    adsk.core.Point3D.create({-r}, 0, 0),
    adsk.core.Point3D.create({r}, 0, 0)
)
profile = sketch.profiles.item(0)
revFeats = rootComp.features.revolveFeatures
revInput = revFeats.createInput(profile, axisLine, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
revInput.setAngleExtent(False, adsk.core.ValueInput.createByString('360 deg'))
revolve = revFeats.add(revInput)
body = revolve.bodies.item(0)
body.name = "{name}"
print(f"Created sphere: {name} (r={radius}mm)")
'''
    return await bridge.execute_python(code)


# ─── create_cone ────────────────────────────────────────────────────────

@mcp.tool()
async def create_cone(
    radius: float = Field(default=5, description="Base radius in mm"),
    height: float = Field(default=10, description="Height in mm"),
    name: str = Field(default="Cone", description="Body name"),
) -> str:
    """Create a parametric cone at the origin in Fusion 360.

    Created by revolving a triangle profile 360 degrees around the Y axis.
    All dimensions are in millimeters.
    """
    r = radius * config.MM_TO_CM
    h = height * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

sketch = rootComp.sketches.add(rootComp.yZConstructionPlane)
lines = sketch.sketchCurves.sketchLines
p0 = adsk.core.Point3D.create(0, 0, 0)
p1 = adsk.core.Point3D.create(0, {r}, 0)
p2 = adsk.core.Point3D.create(0, 0, {h})
lines.addByTwoPoints(p0, p1)
lines.addByTwoPoints(p1, p2)
lines.addByTwoPoints(p2, p0)
profile = sketch.profiles.item(0)
revolveFeats = rootComp.features.revolveFeatures
revolveInput = revolveFeats.createInput(
    profile,
    sketch.sketchCurves.sketchLines.item(0),
    adsk.fusion.FeatureOperations.NewBodyFeatureOperation
)
revolveInput.setAngleExtent(False, adsk.core.ValueInput.createByReal(360))
revolve = revolveFeats.add(revolveInput)
body = revolve.bodies.item(0)
body.name = "{name}"
print(f"Created cone: {name} (r={radius}mm, h={height}mm)")
'''
    return await bridge.execute_python(code)


# ─── create_torus ────────────────────────────────────────────────────────

@mcp.tool()
async def create_torus(
    major_radius: float = Field(default=10, description="Distance from center to tube center in mm"),
    minor_radius: float = Field(default=3, description="Tube radius in mm"),
    name: str = Field(default="Torus", description="Body name"),
) -> str:
    """Create a parametric torus at the origin in Fusion 360.

    Created by sweeping a circular profile along a circular path.
    IMPORTANT: RevolveFeatures cannot create a torus (ASM_PATH_TANGENT error) — must use SweepFeatures.
    All dimensions are in millimeters.
    """
    R = major_radius * config.MM_TO_CM
    r = minor_radius * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

pathSketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
pathCircle = pathSketch.sketchCurves.sketchCircles.addByCenterRadius(
    adsk.core.Point3D.create(0, 0, 0), {R}
)
path = adsk.fusion.Path.create(pathCircle, adsk.fusion.ChainedCurveOptions.noChainedCurves)

profileSketch = rootComp.sketches.add(rootComp.xZConstructionPlane)
profileCircle = profileSketch.sketchCurves.sketchCircles.addByCenterRadius(
    adsk.core.Point3D.create({R}, 0, 0), {r}
)
profile = profileSketch.profiles.item(0)

sweepFeats = rootComp.features.sweepFeatures
sweepInput = sweepFeats.createInput(profile, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
sweep = sweepFeats.add(sweepInput)
body = sweep.bodies.item(0)
body.name = "{name}"
print(f"Created torus: {name} (R={major_radius}mm, r={minor_radius}mm)")
'''
    return await bridge.execute_python(code)


# ─── create_loft ────────────────────────────────────────────────────────

@mcp.tool()
async def create_loft(
    radius1: float = Field(default=3, description="Bottom circle radius in mm"),
    radius2: float = Field(default=1.5, description="Top circle radius in mm"),
    height: float = Field(default=5, description="Distance between profiles in mm"),
    name: str = Field(default="Loft", description="Body name"),
) -> str:
    """Create a loft feature between two circular profiles in Fusion 360.

    Creates two circles on offset planes and lofts between them.
    All dimensions are in millimeters.
    """
    r1 = radius1 * config.MM_TO_CM
    r2 = radius2 * config.MM_TO_CM
    h = height * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

planes = rootComp.constructionPlanes
planeInput = planes.createInput()
planeInput.setByOffset(rootComp.xYConstructionPlane, adsk.core.ValueInput.createByReal({h}))
offsetPlane = planes.add(planeInput)

sketch1 = rootComp.sketches.add(rootComp.xYConstructionPlane)
sketch1.sketchCurves.sketchCircles.addByCenterRadius(
    adsk.core.Point3D.create(0, 0, 0), {r1}
)
profile1 = sketch1.profiles.item(0)

sketch2 = rootComp.sketches.add(offsetPlane)
sketch2.sketchCurves.sketchCircles.addByCenterRadius(
    adsk.core.Point3D.create(0, 0, 0), {r2}
)
profile2 = sketch2.profiles.item(0)

loftFeats = rootComp.features.loftFeatures
loftInput = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
loftInput.loftSections.add(profile1)
loftInput.loftSections.add(profile2)
loftInput.isSolid = True
loft = loftFeats.add(loftInput)
body = loft.bodies.item(0)
body.name = "{name}"
print(f"Created loft: {name} (r1={radius1}mm, r2={radius2}mm, h={height}mm)")
'''
    return await bridge.execute_python(code)
