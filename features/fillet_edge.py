# === Function: fillet_edge ===
# Description: Add a constant radius fillet to a selected edge
# Parameters: edge (Edge object), radius (mm)
# Tested: 2026-06-05 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED

import adsk.core, adsk.fusion

def fillet_edge(edge, radius=2.0):
    """
    Add a constant radius fillet to an edge.
    Args:
        edge: An Edge object (from body.faces.item(i).edges.item(j))
        radius: Fillet radius in mm
    Returns:
        The created FilletFeature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    # Create ObjectCollection with the edge
    edgesCol = adsk.core.ObjectCollection.create()
    edgesCol.add(edge)

    # Create fillet input
    filletFeats = rootComp.features.filletFeatures
    filletInput = filletFeats.createInput()
    filletInput.addConstantRadiusEdgeSet(
        edgesCol,
        adsk.core.ValueInput.createByReal(radius),
        False  # isTangentChain (False = only selected edge)
    )

    return filletFeats.add(filletInput)

# Example usage (after creating a cube):
# app = adsk.core.Application.get()
# design = app.activeProduct
# rootComp = design.rootComponent
# body = rootComp.bRepBodies.item(0)
# edge = body.edges.item(0)  # Get first edge
# fillet_edge(edge, 2.0)
