# === Function: combine_bodies ===
# Description: Combine (join/cut/intersect) multiple bodies
# Parameters: target_body, tool_bodies (list), operation (Join/Cut/Intersect)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/CombineFeatures_createInput.htm

import adsk.core, adsk.fusion

def combine_bodies(target_body, tool_bodies, operation=adsk.fusion.FeatureOperations.JoinFeatureOperation):
    """
    Combine (join/cut/intersect) multiple bodies.
    
    Args:
        target_body: BRepBody (blank body)
        tool_bodies: List of BRepBody objects (tool bodies)
        operation: FeatureOperations (JoinFeatureOperation, CutFeatureOperation, IntersectFeatureOperation)
    
    Returns:
        adsk.fusion.CombineFeature: The created combine feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create ObjectCollection for tool bodies
    tool_coll = adsk.core.ObjectCollection.create()
    for body in tool_bodies:
        tool_coll.add(body)
    
    # Create combine feature
    combineFeats = rootComp.features.combineFeatures
    combineInput = combineFeats.createInput(target_body, tool_coll)
    combineInput.operation = operation
    combine = combineFeats.add(combineInput)
    
    print(f"Combine feature created: {combine.name}")
    return combine

# Example usage (commented out - requires pre-existing bodies):
# body1 = rootComp.bRepBodies.item(0)
# body2 = rootComp.bRepBodies.item(1)
# combine_bodies(body1, [body2], adsk.fusion.FeatureOperations.JoinFeatureOperation)
