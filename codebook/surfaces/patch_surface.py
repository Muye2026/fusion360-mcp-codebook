# === Function: patch_surface ===
# Description: Create a patch surface from a sketch profile or edges
# Parameters: boundary_curve (profile/curve/edges), operation (NewBody/NewComponent)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/PatchFeatures_createInput.htm

import adsk.core, adsk.fusion

def patch_surface(boundary_curve, operation=adsk.fusion.FeatureOperations.NewBodyFeatureOperation):
    """
    Create a patch surface from boundary curves.
    
    Args:
        boundary_curve: Sketch profile, single curve, B-Rep edge, ObjectCollection, or Path
        operation: FeatureOperations (NewBodyFeatureOperation or NewComponentFeatureOperation)
    
    Returns:
        adsk.fusion.PatchFeature: The created patch feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create patch feature
    patchFeats = rootComp.features.patchFeatures
    patchInput = patchFeats.createInput(boundary_curve, operation)
    patch = patchFeats.add(patchInput)
    
    print(f"Patch feature created: {patch.name}")
    return patch

# Example usage (commented out - requires pre-existing profile):
# sketch = rootComp.sketches.item(0)
# profile = sketch.profiles.item(0)
# patch_surface(profile)
