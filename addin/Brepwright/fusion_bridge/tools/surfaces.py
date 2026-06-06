"""Surfaces tools — direct Fusion API calls."""

import adsk.core
import adsk.fusion

MM_TO_CM = 0.1


def _get_root():
    app = adsk.core.Application.get()
    return app.activeProduct.rootComponent


def _find_body(body_name):
    rootComp = _get_root()
    for i in range(rootComp.bRepBodies.count):
        body = rootComp.bRepBodies.item(i)
        if body.name == body_name:
            return body
    raise ValueError(f'Body "{body_name}" not found')


def create_sweep(args):
    """Create a sweep tube by sweeping a circular profile along a straight path."""
    r = args.get("profile_radius", 5) * MM_TO_CM
    length = args.get("path_length", 100) * MM_TO_CM
    name = args.get("name", "SweepTube")

    rootComp = _get_root()
    # Profile on YZ plane
    profileSketch = rootComp.sketches.add(rootComp.yZConstructionPlane)
    profileSketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), r
    )
    profile = profileSketch.profiles.item(0)
    # Path on XY plane
    pathSketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    pathLine = pathSketch.sketchCurves.sketchLines.addByTwoPoints(
        adsk.core.Point3D.create(0, r, 0),
        adsk.core.Point3D.create(length, r, 0),
    )
    path = adsk.fusion.Path.create(pathLine, adsk.fusion.ChainedCurveOptions.tangentChainedCurves)
    # Sweep
    sweepFeats = rootComp.features.sweepFeatures
    sweepInput = sweepFeats.createInput(profile, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    sweepInput.orientation = adsk.fusion.SweepOrientationTypes.PerpendicularOrientationType
    sweep = sweepFeats.add(sweepInput)
    body = sweep.bodies.item(0)
    body.name = name
    return f"Created sweep: {name} (r={args.get('profile_radius', 5)}mm, l={args.get('path_length', 100)}mm)"


def patch_surface(args):
    """Create a patch surface from a circular profile."""
    r = args.get("radius", 5) * MM_TO_CM
    name = args.get("name", "Patch")

    rootComp = _get_root()
    sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    sketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), r
    )
    profile = sketch.profiles.item(0)

    patchFeats = rootComp.features.patchFeatures
    patchInput = patchFeats.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    patch = patchFeats.add(patchInput)
    body = patch.bodies.item(0)
    body.name = name
    return f"Created patch: {name} (r={args.get('radius', 5)}mm)"


def offset_surface(args):
    """Create an offset surface from a face."""
    body_name = args["body_name"]
    distance = args.get("distance", 2) * MM_TO_CM
    face_index = args.get("face_index", 0)

    body = _find_body(body_name)
    rootComp = _get_root()
    face = body.faces.item(face_index)

    faces = adsk.core.ObjectCollection.create()
    faces.add(face)

    offsetFeats = rootComp.features.offsetFeatures
    offsetInput = offsetFeats.createInput(faces, adsk.core.ValueInput.createByReal(distance), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    offsetFeats.add(offsetInput)
    return f"Offset surface: d={args.get('distance', 2)}mm from {body_name}"


def thicken_surface(args):
    """Thicken a surface body."""
    body_name = args["body_name"]
    thickness = args.get("thickness", 2) * MM_TO_CM
    symmetric = args.get("symmetric", True)

    body = _find_body(body_name)
    rootComp = _get_root()

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)

    thickenFeats = rootComp.features.thickenFeatures
    thickenInput = thickenFeats.createInput(
        bodies, adsk.core.ValueInput.createByReal(thickness), symmetric,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    thickenFeats.add(thickenInput)
    return f"Thickened {body_name}: t={args.get('thickness', 2)}mm"


def stitch_surface(args):
    """Stitch multiple surface bodies."""
    body_names = args["body_names"]
    tolerance = args.get("tolerance", 0.01) * MM_TO_CM

    rootComp = _get_root()
    bodies = adsk.core.ObjectCollection.create()
    for name in body_names:
        bodies.add(_find_body(name))

    stitchFeats = rootComp.features.stitchFeatures
    stitchInput = stitchFeats.createInput(
        bodies, adsk.core.ValueInput.createByReal(tolerance),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    stitchFeats.add(stitchInput)
    return f"Stitched {len(body_names)} surfaces"


def trim_surface(args):
    """Trim a surface body using a construction plane."""
    body_name = args["body_name"]
    plane_name = args.get("trim_plane", "XY")

    body = _find_body(body_name)
    rootComp = _get_root()

    plane_map = {
        "XY": rootComp.xYConstructionPlane,
        "XZ": rootComp.xZConstructionPlane,
        "YZ": rootComp.yZConstructionPlane,
    }
    trim_tool = plane_map.get(plane_name, rootComp.xYConstructionPlane)

    trimFeats = rootComp.features.trimFeatures
    trimInput = trimFeats.createInput(trim_tool)
    # Select all cells to keep
    cells = trimInput.bRepCells
    for i in range(cells.count):
        cells.item(i).isSelected = True
    trimFeats.add(trimInput)
    return f"Trimmed {body_name} with {plane_name} plane"
