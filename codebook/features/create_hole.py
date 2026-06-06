# === Function: create_hole ===
# Description: Create a simple hole on a face of an existing body
# Parameters: diameter (cm), depth (cm), face (BRepFace), point (Point3D)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# API Reference: holeFeatures.createSimpleInput(), setPositionByPoint(face, point), setDistanceExtent()
# Key insight: setPositionByPoint requires BOTH planarEntity (BRepFace) AND point (Point3D)

import adsk.core, adsk.fusion

def create_hole(diameter, depth, face, point, name="Hole"):
    """
    Create a simple hole on a face of an existing body.
    
    Args:
        diameter: Hole diameter (cm)
        depth: Hole depth (cm)
        face: BRepFace to place the hole on (defines orientation)
        point: Point3D defining the hole center position
        name: Name for the feature
    
    Returns:
        The created HoleFeature object
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    holeFeats = rootComp.features.holeFeatures
    holeInput = holeFeats.createSimpleInput(adsk.core.ValueInput.createByReal(diameter))
    holeInput.setPositionByPoint(face, point)
    holeInput.setDistanceExtent(adsk.core.ValueInput.createByReal(depth))
    hole = holeFeats.add(holeInput)
    return hole

# Helper: Find top face of a body (face with normal pointing up in Z)
def find_top_face(body):
    """Find the face of a body whose normal points in +Z direction."""
    for i in range(body.faces.count):
        face = body.faces.item(i)
        normal = face.geometry.normal if hasattr(face.geometry, 'normal') else None
        if normal and normal.z > 0.9:
            return face
    return None

# Example usage (requires an existing body):
# body = rootComp.bRepBodies.itemByName("MyBody")
# topFace = find_top_face(body)
# if topFace:
#     create_hole(1.0, 5.0, topFace, adsk.core.Point3D.create(5, 5, 10))
