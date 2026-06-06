# === Function: thicken_surface ===
# Description: Thicken a surface/patch body to create a solid
# Parameters: bodies (list), thickness (mm), is_symmetric (bool), operation
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ThickenFeatures_createInput.htm

import adsk.core, adsk.fusion

def thicken_surface(bodies, thickness, is_symmetric=False, 
                    operation=adsk.fusion.FeatureOperations.NewBodyFeatureOperation):
    """
    Thicken surface/patch bodies to create solid bodies.
    
    Args:
        bodies: List of surface bodies or faces to thicken
        thickness: Thickness value (mm)
        is_symmetric: Add thickness symmetrically (default False)
        operation: FeatureOperations (NewBodyFeatureOperation or NewComponentFeatureOperation)
    
    Returns:
        adsk.fusion.ThickenFeature: The created thicken feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create ObjectCollection from bodies
    bodies_coll = adsk.core.ObjectCollection.create()
    for body in bodies:
        bodies_coll.add(body)
    
    # Create thicken feature
    thickenFeats = rootComp.features.thickenFeatures
    thickenInput = thickenFeats.createInput(bodies_coll,
                                           adsk.core.ValueInput.createByReal(thickness),
                                           is_symmetric,
                                           operation)
    thicken = thickenFeats.add(thickenInput)
    
    print(f"Thicken feature created: {thicken.name}")
    return thicken

# Example usage (commented out - requires pre-existing surface body):
# surface_body = rootComp.bRepBodies.item(0)
# thicken_surface([surface_body], 2)
