# === Function: draft_faces ===
# Description: Apply draft angle to selected faces of a body
# Parameters: body_name (str), angle_deg (float), pull_plane (str: 'XY'|'XZ'|'YZ')
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/draftFeatures_add_Sample.htm

import adsk.core, adsk.fusion

def draft_faces(body_name: str, angle_deg: float = 5.0, pull_plane: str = 'XY'):
    """
    Apply draft angle to side faces of a body.
    
    Args:
        body_name: Name of the target body (must exist in root component)
        angle_deg: Draft angle in degrees (default 5.0)
        pull_plane: Pull direction plane ('XY', 'XZ', or 'YZ')
    
    Returns:
        adsk.fusion.DraftFeature: The created draft feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Find the target body
    body = None
    for i in range(rootComp.bRepBodies.count):
        b = rootComp.bRepBodies.item(i)
        if b.name == body_name:
            body = b
            break
    
    if not body:
        raise ValueError(f'Body "{body_name}" not found')
    
    # Find side faces (not parallel to pull plane)
    faces = body.faces
    side_faces = []
    
    for i in range(faces.count):
        face = faces.item(i)
        normal = face.geometry.normal
        
        # Determine which faces are "side faces" based on pull plane
        if pull_plane == 'XY':
            # Side faces have normal.z ~ 0 (not parallel to XY)
            if abs(normal.z) < 0.1:
                side_faces.append(face)
        elif pull_plane == 'XZ':
            # Side faces have normal.y ~ 0
            if abs(normal.y) < 0.1:
                side_faces.append(face)
        elif pull_plane == 'YZ':
            # Side faces have normal.x ~ 0
            if abs(normal.x) < 0.1:
                side_faces.append(face)
    
    if not side_faces:
        raise ValueError(f'No side faces found for pull plane {pull_plane}')
    
    print(f'Found {len(side_faces)} side faces to draft')
    
    # Get pull direction plane
    if pull_plane == 'XY':
        pull_direction = rootComp.xYConstructionPlane
    elif pull_plane == 'XZ':
        pull_direction = rootComp.xZConstructionPlane
    elif pull_plane == 'YZ':
        pull_direction = rootComp.yZConstructionPlane
    else:
        raise ValueError(f'Invalid pull_plane: {pull_plane}')
    
    # Create draft feature
    angle = adsk.core.ValueInput.createByString(f'{angle_deg} deg')
    
    draftFeats = rootComp.features.draftFeatures
    draftInput = draftFeats.createInput(side_faces, pull_direction)
    draftInput.setSingleAngle(True, angle)  # isFixed=True, angle
    draft = draftFeats.add(draftInput)
    
    print(f'Draft feature created: {draft.name}')
    return draft

# Test: Apply 5° draft to "DraftTarget" body
draft_faces("DraftTarget", 5.0, "XY")
