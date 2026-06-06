# === Function: trim_surface ===
# Description: Trim surfaces with a trim tool (plane/curve/face/body)
# Parameters: trim_tool (entity), cells_to_keep (list of indices or 'all')
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/TrimFeatures_createInput.htm

import adsk.core, adsk.fusion

def trim_surface(trim_tool, cells_to_keep='all'):
    """
    Trim surfaces using a trim tool.
    
    Args:
        trim_tool: Trim tool entity (patch body, B-Rep face, construction plane, or sketch curve)
        cells_to_keep: 'all' to keep all cells, or list of cell indices to keep
    
    Returns:
        adsk.fusion.TrimFeature: The created trim feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create TrimFeatureInput
    trimFeats = rootComp.features.trimFeatures
    trimInput = trimFeats.createInput(trim_tool)
    
    # Select cells to keep
    cells = trimInput.bRepCells
    if cells_to_keep == 'all':
        for i in range(cells.count):
            cells.item(i).isSelected = True
    else:
        for idx in cells_to_keep:
            cells.item(idx).isSelected = True
    
    # Create trim feature
    trim = trimFeats.add(trimInput)
    
    print(f"Trim feature created: {trim.name}")
    return trim

# Example usage (commented out - requires pre-existing surface and trim tool):
# surface_body = rootComp.bRepBodies.item(0)
# trim_tool = rootComp.yZConstructionPlane
# trim_surface(trim_tool, 'all')
