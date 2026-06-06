# === Function: move_body ===
# Description: Move bodies by translation or rotation
# Parameters: bodies (list), translation (Vector3D) or rotation (Matrix3D)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/MoveFeatures_createInput.htm

import adsk.core, adsk.fusion

def move_body(bodies, transform):
    """
    Move bodies by applying a transform (translation or rotation).
    
    Args:
        bodies: List of BRepBody objects to move
        transform: Matrix3D defining the transform (translation or rotation)
    
    Returns:
        adsk.fusion.MoveFeature: The created move feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create ObjectCollection from bodies
    bodies_coll = adsk.core.ObjectCollection.create()
    for body in bodies:
        bodies_coll.add(body)
    
    # Create move feature
    moveFeats = rootComp.features.moveFeatures
    moveInput = moveFeats.createInput(bodies_coll, transform)
    move = moveFeats.add(moveInput)
    
    print(f"Move feature created: {move.name}")
    return move

def move_body_by_translation(bodies, x=0, y=0, z=0):
    """
    Move bodies by translation (simplified wrapper).
    
    Args:
        bodies: List of BRepBody objects to move
        x, y, z: Translation distances (mm)
    
    Returns:
        adsk.fusion.MoveFeature: The created move feature
    """
    translation = adsk.core.Vector3D.create(x, y, z)
    matrix = adsk.core.Matrix3D.create()
    matrix.translation = translation
    return move_body(bodies, matrix)

# Example usage (commented out - requires pre-existing body):
# body = rootComp.bRepBodies.item(0)
# move_body_by_translation([body], 10, 0, 0)
