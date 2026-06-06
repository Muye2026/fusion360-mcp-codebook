# === Function: offset_surface ===
# Description: Offset faces by a distance
# Parameters: faces (list), distance (mm), operation (NewBody/NewComponent)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/OffsetFeatures_createInput.htm

import adsk.core, adsk.fusion

def offset_surface(faces, distance, operation=adsk.fusion.FeatureOperations.NewBodyFeatureOperation):
    """
    Offset faces by a specified distance.
    
    Args:
        faces: List of BRepFace objects to offset
        distance: Offset distance (mm, positive = positive normal direction)
        operation: FeatureOperations (NewBodyFeatureOperation or NewComponentFeatureOperation)
    
    Returns:
        adsk.fusion.OffsetFeature: The created offset feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create ObjectCollection from faces
    faces_coll = adsk.core.ObjectCollection.create()
    for face in faces:
        faces_coll.add(face)
    
    # Create offset feature
    offsetFeats = rootComp.features.offsetFeatures
    offsetInput = offsetFeats.createInput(faces_coll, 
                                         adsk.core.ValueInput.createByReal(distance),
                                         operation)
    offset = offsetFeats.add(offsetInput)
    
    print(f"Offset feature created: {offset.name}")
    return offset

# Example usage (commented out - requires pre-existing face):
# face = rootComp.bRepBodies.item(0).faces.item(0)
# offset_surface([face], 5)
