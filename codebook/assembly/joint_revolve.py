# === Function: joint_revolve ===
# Description: Create a revolute (hinge) joint between two occurrences using vertices at origin
# Parameters: occ1_index (int), occ2_index (int), axis_direction (JointDirections)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# Best practice: setAsRevoluteJointMotion takes JointDirections enum, not Vector3D

import adsk.core, adsk.fusion

def joint_revolve(occ1_index=0, occ2_index=1, axis_direction=adsk.fusion.JointDirections.ZAxisJointDirection):
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    # Get occurrences
    occ1 = rootComp.occurrences.item(occ1_index)
    occ2 = rootComp.occurrences.item(occ2_index)
    comp1 = occ1.component
    comp2 = occ2.component

    # Find vertices near origin in each body
    body1 = comp1.bRepBodies.item(0)
    body2 = comp2.bRepBodies.item(0)

    v1 = None
    v2 = None
    for v in body1.vertices:
        p = v.geometry
        if abs(p.x) < 0.1 and abs(p.y) < 0.1 and abs(p.z) < 0.1:
            v1 = v
            break

    for v in body2.vertices:
        p = v.geometry
        if abs(p.x) < 0.1 and abs(p.y) < 0.1 and abs(p.z) < 0.1:
            v2 = v
            break

    if not v1 or not v2:
        return None

    # Create JointGeometry using BRepVertex
    # createByPoint accepts ConstructionPoint, SketchPoint, or BRepVertex
    jointGeom1 = adsk.fusion.JointGeometry.createByPoint(v1)
    jointGeom2 = adsk.fusion.JointGeometry.createByPoint(v2)

    # Create joint input
    joints = rootComp.joints
    jointInput = joints.createInput(jointGeom1, jointGeom2)

    # Set as revolute joint
    # setAsRevoluteJointMotion takes JointDirections enum (not Vector3D!)
    jointInput.setAsRevoluteJointMotion(axis_direction)

    # Add joint
    joint = joints.add(jointInput)

    return joint

joint_revolve(0, 1, adsk.fusion.JointDirections.ZAxisJointDirection)
