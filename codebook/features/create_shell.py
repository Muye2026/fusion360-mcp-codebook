# === Function: create_shell ===
# Description: Create a shell feature by removing a face and hollowing a body
# Parameters: thickness (cm), body (BRepBody), face_to_remove (BRepFace)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# API Reference: shellFeatures.createInput(facesToRemove, isTangentChain), insideThickness
# Key insight: createInput takes ObjectCollection of faces to remove, NOT the body

import adsk.core, adsk.fusion

def create_shell(thickness, face_to_remove, is_tangent_chain=True, name="Shell"):
    """
    Create a shell feature by removing a face and hollowing a body.
    
    Args:
        thickness: Wall thickness (cm)
        face_to_remove: BRepFace to remove (open the shell)
        is_tangent_chain: Include tangentially connected faces (default True)
        name: Name for the feature
    
    Returns:
        The created ShellFeature object
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    # Create ObjectCollection with face(s) to remove
    facesToRemove = adsk.core.ObjectCollection.create()
    facesToRemove.add(face_to_remove)

    shellFeats = rootComp.features.shellFeatures
    shellInput = shellFeats.createInput(facesToRemove, is_tangent_chain)
    shellInput.insideThickness = adsk.core.ValueInput.createByReal(thickness)
    shell = shellFeats.add(shellInput)
    return shell

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
#     create_shell(0.2, topFace)
