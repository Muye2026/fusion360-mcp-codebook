# === Function: mirror_bodies ===
# Description: Mirror bodies/features across a plane
# Parameters: input_entities (list), mirror_plane_entity
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/MirrorFeatures_createInput.htm

import adsk.core, adsk.fusion

def mirror_bodies(input_entities, mirror_plane_entity):
    """
    Mirror bodies or features across a plane.
    
    Args:
        input_entities: List of bodies/features/faces to mirror
        mirror_plane_entity: Planar face or construction plane to mirror across
    
    Returns:
        adsk.fusion.MirrorFeature: The created mirror feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create ObjectCollection from input entities
    entities_coll = adsk.core.ObjectCollection.create()
    for entity in input_entities:
        entities_coll.add(entity)
    
    # Create mirror feature
    mirrorFeats = rootComp.features.mirrorFeatures
    mirrorInput = mirrorFeats.createInput(entities_coll, mirror_plane_entity)
    mirror = mirrorFeats.add(mirrorInput)
    
    print(f"Mirror feature created: {mirror.name}")
    return mirror

# Example usage (commented out - requires pre-existing body):
# body = rootComp.bRepBodies.item(0)
# mirror_bodies([body], rootComp.yZConstructionPlane)
