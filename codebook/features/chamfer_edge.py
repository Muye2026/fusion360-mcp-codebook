# === Function: chamfer_edge ===
# Description: Add a chamfer to a selected edge
# Parameters: edge (Edge object), distance (mm)
# Tested: 2026-06-05 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED

import adsk.core, adsk.fusion

def chamfer_edge(edge, distance=1.0):
    """
    Add a chamfer to an edge.
    Args:
        edge: An Edge object (from body.faces.item(i).edges.item(j))
        distance: Chamfer distance in mm
    Returns:
        The created ChamferFeature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    # Create ObjectCollection with the edge
    edgesCol = adsk.core.ObjectCollection.create()
    edgesCol.add(edge)

    # Create chamfer input (use createInput2 for edge chamfer)
    chamferFeats = rootComp.features.chamferFeatures
    chamferInput = chamferFeats.createInput2()
    
    # Add equal distance chamfer edge set
    offset = adsk.core.ValueInput.createByReal(distance)
    chamferInput.chamferEdgeSets.addEqualDistanceChamferEdgeSet(
        edgesCol,
        offset,
        True  # isTangentChain
    )

    return chamferFeats.add(chamferInput)

# Example usage (after creating a cube):
# app = adsk.core.Application.get()
# design = app.activeProduct
# rootComp = design.rootComponent
# body = rootComp.bRepBodies.item(0)
# edge = body.edges.item(0)
# chamfer_edge(edge, 1.0)
