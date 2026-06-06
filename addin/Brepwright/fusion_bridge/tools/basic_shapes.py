"""Basic Shapes tools — direct Fusion API calls (no code generation)."""

import adsk.core
import adsk.fusion

MM_TO_CM = 0.1


def _get_root():
    """Get the root component of the active design."""
    app = adsk.core.Application.get()
    design = app.activeProduct
    return design.rootComponent


def create_cube(args):
    """Create a parametric cube at the origin."""
    w = args.get("width", 10) * MM_TO_CM
    h = args.get("height", 10) * MM_TO_CM
    d = args.get("depth", 10) * MM_TO_CM
    name = args.get("name", "Cube")

    rootComp = _get_root()
    sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(w, h, 0),
    )
    profile = sketch.profiles.item(0)
    extFeats = rootComp.features.extrudeFeatures
    extInput = extFeats.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(d))
    extrude = extFeats.add(extInput)
    body = extrude.bodies.item(0)
    body.name = name
    return f"Created cube: {name} ({args.get('width', 10)}x{args.get('height', 10)}x{args.get('depth', 10)}mm)"


def create_cylinder(args):
    """Create a parametric cylinder at the origin."""
    r = args.get("radius", 5) * MM_TO_CM
    h = args.get("height", 20) * MM_TO_CM
    name = args.get("name", "Cylinder")

    rootComp = _get_root()
    sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    sketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), r
    )
    profile = sketch.profiles.item(0)
    extFeats = rootComp.features.extrudeFeatures
    extInput = extFeats.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(h))
    extrude = extFeats.add(extInput)
    body = extrude.bodies.item(0)
    body.name = name
    return f"Created cylinder: {name} (r={args.get('radius', 5)}mm, h={args.get('height', 20)}mm)"


def create_sphere(args):
    """Create a sphere by revolving a semi-circle."""
    r = args.get("radius", 5) * MM_TO_CM
    name = args.get("name", "Sphere")

    rootComp = _get_root()
    sketch = rootComp.sketches.add(rootComp.xZConstructionPlane)
    # Semi-circle arc + closing line
    arc = sketch.sketchCurves.sketchArcs.addByThreePoints(
        adsk.core.Point3D.create(-r, 0, 0),
        adsk.core.Point3D.create(0, r, 0),
        adsk.core.Point3D.create(r, 0, 0),
    )
    line = sketch.sketchCurves.sketchLines.addByTwoPoints(
        arc.startSketchPoint, arc.endSketchPoint
    )
    profile = sketch.profiles.item(0)
    revFeats = rootComp.features.revolveFeatures
    revInput = revFeats.createInput(
        profile, line, adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    revInput.setAngleExtent(False, adsk.core.ValueInput.createByString("360 deg"))
    revolve = revFeats.add(revInput)
    body = revolve.bodies.item(0)
    body.name = name
    return f"Created sphere: {name} (r={args.get('radius', 5)}mm)"


def create_cone(args):
    """Create a cone by revolving a triangle."""
    r = args.get("radius", 5) * MM_TO_CM
    h = args.get("height", 10) * MM_TO_CM
    name = args.get("name", "Cone")

    rootComp = _get_root()
    sketch = rootComp.sketches.add(rootComp.yZConstructionPlane)
    lines = sketch.sketchCurves.sketchLines
    p0 = adsk.core.Point3D.create(0, 0, 0)
    p1 = adsk.core.Point3D.create(0, r, 0)
    p2 = adsk.core.Point3D.create(0, 0, h)
    l1 = lines.addByTwoPoints(p0, p1)
    lines.addByTwoPoints(p1, p2)
    lines.addByTwoPoints(p2, p0)
    profile = sketch.profiles.item(0)
    revFeats = rootComp.features.revolveFeatures
    revInput = revFeats.createInput(
        profile, l1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    revInput.setAngleExtent(False, adsk.core.ValueInput.createByReal(360))
    revolve = revFeats.add(revInput)
    body = revolve.bodies.item(0)
    body.name = name
    return f"Created cone: {name} (r={args.get('radius', 5)}mm, h={args.get('height', 10)}mm)"


def create_torus(args):
    """Create a torus by sweeping a circular profile along a circular path."""
    R = args.get("major_radius", 10) * MM_TO_CM
    r = args.get("minor_radius", 3) * MM_TO_CM
    name = args.get("name", "Torus")

    rootComp = _get_root()
    # Path: circle on XY plane
    pathSketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    pathCircle = pathSketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), R
    )
    path = adsk.fusion.Path.create(pathCircle, adsk.fusion.ChainedCurveOptions.noChainedCurves)
    # Profile: circle on XZ plane
    profileSketch = rootComp.sketches.add(rootComp.xZConstructionPlane)
    profileSketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(R, 0, 0), r
    )
    profile = profileSketch.profiles.item(0)
    sweepFeats = rootComp.features.sweepFeatures
    sweepInput = sweepFeats.createInput(
        profile, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    sweep = sweepFeats.add(sweepInput)
    body = sweep.bodies.item(0)
    body.name = name
    return f"Created torus: {name} (R={args.get('major_radius', 10)}mm, r={args.get('minor_radius', 3)}mm)"


def create_loft(args):
    """Create a loft between two circular profiles."""
    r1 = args.get("radius1", 3) * MM_TO_CM
    r2 = args.get("radius2", 1.5) * MM_TO_CM
    h = args.get("height", 5) * MM_TO_CM
    name = args.get("name", "Loft")

    rootComp = _get_root()
    # Offset plane
    planes = rootComp.constructionPlanes
    planeInput = planes.createInput()
    planeInput.setByOffset(rootComp.xYConstructionPlane, adsk.core.ValueInput.createByReal(h))
    offsetPlane = planes.add(planeInput)
    # Bottom profile
    sketch1 = rootComp.sketches.add(rootComp.xYConstructionPlane)
    sketch1.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), r1
    )
    profile1 = sketch1.profiles.item(0)
    # Top profile
    sketch2 = rootComp.sketches.add(offsetPlane)
    sketch2.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), r2
    )
    profile2 = sketch2.profiles.item(0)
    # Loft
    loftFeats = rootComp.features.loftFeatures
    loftInput = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    loftInput.loftSections.add(profile1)
    loftInput.loftSections.add(profile2)
    loftInput.isSolid = True
    loft = loftFeats.add(loftInput)
    body = loft.bodies.item(0)
    body.name = name
    return f"Created loft: {name} (r1={args.get('radius1', 3)}mm, r2={args.get('radius2', 1.5)}mm, h={args.get('height', 5)}mm)"
