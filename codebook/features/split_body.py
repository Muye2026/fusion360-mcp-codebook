# === Function: split_body ===
# Description: Split a body with a splitting tool (plane/face/body)
# Parameters: body (BRepBody), splitting_tool (entity), is_tool_extended (bool)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/SplitBodyFeatures_createInput.htm

import adsk.core, adsk.fusion

def split_body(body, splitting_tool, is_tool_extended=False):
    """
    Split a body using a splitting tool.
    
    Args:
        body: BRepBody to split
        splitting_tool: Splitting tool (BRepBody, construction plane, profile, or face)
        is_tool_extended: Extend tool to fully intersect body (default False)
    
    Returns:
        adsk.fusion.SplitBodyFeature: The created split feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create split feature
    splitFeats = rootComp.features.splitBodyFeatures
    splitInput = splitFeats.createInput(body, splitting_tool, is_tool_extended)
    split = splitFeats.add(splitInput)
    
    print(f"Split feature created: {split.name}")
    print(f"Number of split bodies: {split.bodies.count}")
    return split

# Example usage (commented out - requires pre-existing body and splitting tool):
# body = rootComp.bRepBodies.item(0)
# splitting_plane = rootComp.constructionPlanes.item(0)
# split_body(body, splitting_plane)
