"""Transforms tools — direct Fusion API calls."""

import math
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


def circular_pattern(args):
    body_name = args["body_name"]
    count = args.get("count", 4)
    angle_deg = args.get("angle_deg", 360)
    axis_name = args.get("axis", "Z")

    body = _find_body(body_name)
    rootComp = _get_root()

    axis_map = {
        "X": adsk.core.Vector3D.create(1, 0, 0),
        "Y": adsk.core.Vector3D.create(0, 1, 0),
        "Z": adsk.core.Vector3D.create(0, 0, 1),
    }
    axis = axis_map.get(axis_name, adsk.core.Vector3D.create(0, 0, 1))

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)

    circFeats = rootComp.features.circularPatternFeatures
    circInput = circFeats.createInput(bodies, axis)
    circInput.quantity = adsk.core.ValueInput.createByReal(count)
    circInput.totalAngle = adsk.core.ValueInput.createByString(f"{angle_deg} deg")
    circInput.isSymmetric = False
    circFeats.add(circInput)
    return f"Circular pattern: {count}x {body_name} around {axis_name} axis"


def rectangular_pattern(args):
    body_name = args["body_name"]
    count_x = args.get("count_x", 2)
    count_y = args.get("count_y", 2)
    spacing_x = args.get("spacing_x", 20) * MM_TO_CM
    spacing_y = args.get("spacing_y", 20) * MM_TO_CM

    body = _find_body(body_name)
    rootComp = _get_root()

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)

    rectFeats = rootComp.features.rectangularPatternFeatures
    rectInput = rectFeats.createInput(
        bodies,
        adsk.core.Vector3D.create(1, 0, 0),
        adsk.core.ValueInput.createByReal(count_x),
        adsk.core.ValueInput.createByReal(spacing_x),
        adsk.fusion.PatternDistanceType.SpacingPatternDistanceType,
    )
    rectInput.directionTwo = adsk.core.Vector3D.create(0, 1, 0)
    rectInput.quantityTwo = adsk.core.ValueInput.createByReal(count_y)
    rectInput.distanceTwo = adsk.core.ValueInput.createByReal(spacing_y)
    rectFeats.add(rectInput)
    return f"Rectangular pattern: {count_x}x{count_y} {body_name}"


def mirror_bodies(args):
    body_name = args["body_name"]
    plane_name = args.get("plane", "YZ")

    body = _find_body(body_name)
    rootComp = _get_root()

    plane_map = {
        "XY": rootComp.xYConstructionPlane,
        "XZ": rootComp.xZConstructionPlane,
        "YZ": rootComp.yZConstructionPlane,
    }
    mirror_plane = plane_map.get(plane_name, rootComp.yZConstructionPlane)

    entities = adsk.core.ObjectCollection.create()
    entities.add(body)

    mirrorFeats = rootComp.features.mirrorFeatures
    mirrorInput = mirrorFeats.createInput(entities, mirror_plane)
    mirrorFeats.add(mirrorInput)
    return f"Mirrored {body_name} across {plane_name} plane"


def rotate_body(args):
    body_name = args["body_name"]
    angle_deg = args.get("angle_deg", 45)
    axis_name = args.get("axis", "Z")

    body = _find_body(body_name)
    rootComp = _get_root()

    axis_map = {
        "X": adsk.core.Vector3D.create(1, 0, 0),
        "Y": adsk.core.Vector3D.create(0, 1, 0),
        "Z": adsk.core.Vector3D.create(0, 0, 1),
    }
    axis = axis_map.get(axis_name, adsk.core.Vector3D.create(0, 0, 1))
    origin = adsk.core.Point3D.create(0, 0, 0)

    angle_rad = angle_deg * math.pi / 180.0
    matrix = adsk.core.Matrix3D.create()
    matrix.setToRotation(angle_rad, axis, origin)

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)

    moveFeats = rootComp.features.moveFeatures
    moveInput = moveFeats.createInput(bodies, matrix)
    moveFeats.add(moveInput)
    return f"Rotated {body_name} {angle_deg}deg around {axis_name} axis"
