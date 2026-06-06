# === Function: stitch_surface ===
# Description: Stitch multiple surface bodies together
# Parameters: bodies (list), tolerance (mm), operation
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/StitchFeatures_createInput.htm

import adsk.core, adsk.fusion

def stitch_surface(bodies, tolerance=0.1, 
                   operation=adsk.fusion.FeatureOperations.NewBodyFeatureOperation):
    """
    Stitch multiple surface bodies together.
    
    Args:
        bodies: List of surface bodies (open BRepBodies) to stitch
        tolerance: Stitching tolerance (mm, default 0.1)
        operation: FeatureOperations (for closed solid results only)
    
    Returns:
        adsk.fusion.StitchFeature: The created stitch feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create ObjectCollection from bodies
    bodies_coll = adsk.core.ObjectCollection.create()
    for body in bodies:
        bodies_coll.add(body)
    
    # Create stitch feature
    stitchFeats = rootComp.features.stitchFeatures
    stitchInput = stitchFeats.createInput(bodies_coll, 
                                        adsk.core.ValueInput.createByReal(tolerance),
                                        operation)
    stitch = stitchFeats.add(stitchInput)
    
    print(f"Stitch feature created: {stitch.name}")
    return stitch

# Example usage (commented out - requires pre-existing surface bodies):
# body1 = rootComp.bRepBodies.item(0)
# body2 = rootComp.bRepBodies.item(1)
# stitch_surface([body1, body2])
