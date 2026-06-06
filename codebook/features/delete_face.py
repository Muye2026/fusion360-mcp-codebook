# === Function: delete_face ===
# Description: Delete faces from a body (turns solid to surface)
# Parameters: faces (list or single face)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/SurfaceDeleteFaceFeatures_add.htm

import adsk.core, adsk.fusion

def delete_face(faces):
    """
    Delete faces from a body (turns solid to surface if first face deleted).
    
    Args:
        faces: Single BRepFace or list of BRepFace objects to delete
    
    Returns:
        adsk.fusion.SurfaceDeleteFaceFeature: The created delete face feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Handle single face or list
    if not isinstance(faces, list):
        faces = [faces]
    
    faces_coll = adsk.core.ObjectCollection.create()
    for face in faces:
        faces_coll.add(face)
    
    # Create delete face feature
    deleteFeats = rootComp.features.surfaceDeleteFaceFeatures
    delete = deleteFeats.add(faces_coll)
    
    print(f"SurfaceDeleteFace feature created: {delete.name}")
    return delete

# Example usage (commented out - requires pre-existing face):
# face = rootComp.bRepBodies.item(0).faces.item(0)
# delete_face(face)
