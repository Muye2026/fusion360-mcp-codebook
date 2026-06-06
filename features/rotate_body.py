# === Function: rotate_body ===
# Description: Rotate bodies around an axis by a given angle
# Parameters: bodies (list), angle (degrees), axis (Vector3D), origin (Point3D)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# Best practice: Use MoveFeatures with Matrix3D.setToRotation(angleRad, axis, origin)

import adsk.core, adsk.fusion
import math

def rotate_body(bodies, angle_deg, axis=None, origin=None):
    """
    Rotate bodies around an axis by a given angle.
    
    Args:
        bodies: List of BRepBody objects to rotate
        angle_deg (float): Rotation angle in degrees (positive = CCW when looking from axis tip)
        axis (Vector3D): Rotation axis vector (default Z axis)
        origin (Point3D): Rotation origin point (default origin)
    
    Returns:
        adsk.fusion.MoveFeature: The created move feature
    
    API Note:
        Rotation uses MoveFeatures with Matrix3D.setToRotation().
        Unlike translation (which uses matrix.translation = vector property),
        rotation correctly uses the setToRotation() method.
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Default: rotate around Z axis at origin
    if axis is None:
        axis = adsk.core.Vector3D.create(0, 0, 1)
    if origin is None:
        origin = adsk.core.Point3D.create(0, 0, 0)
    
    # Convert degrees to radians
    angle_rad = angle_deg * math.pi / 180.0
    
    # Create rotation matrix
    matrix = adsk.core.Matrix3D.create()
    matrix.setToRotation(angle_rad, axis, origin)
    
    # Create ObjectCollection from bodies
    bodies_coll = adsk.core.ObjectCollection.create()
    for body in bodies:
        bodies_coll.add(body)
    
    # Create move feature with rotation matrix
    moveFeats = rootComp.features.moveFeatures
    moveInput = moveFeats.createInput(bodies_coll, matrix)
    move = moveFeats.add(moveInput)
    
    return move

# Example: rotate first body 45 degrees around Z axis (commented - requires pre-existing body)
# body = rootComp.bRepBodies.item(0)
# rotate_body([body], 45)
