# === Function: create_loft ===
# Description: Create a loft feature between two circular profiles
# Parameters: radius1 (cm), radius2 (cm), height (cm), name (str)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# API Reference: loftFeatures.createInput(), loftSections.add(), constructionPlanes.createInput().setByOffset()
# Best practice: Name body immediately after creation

import adsk.core, adsk.fusion

def create_loft(radius1=3, radius2=1.5, height=5, name="Loft"):
    """
    Create a loft between two circular profiles on offset planes.
    
    Args:
        radius1: Radius of the bottom circle (cm)
        radius2: Radius of the top circle (cm)
        height: Distance between the two profiles (cm)
        name: Name for the resulting body
    
    Returns:
        The created LoftFeature object
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    # Step 1: Create offset plane at Z=height
    planes = rootComp.constructionPlanes
    planeInput = planes.createInput()
    planeInput.setByOffset(rootComp.xYConstructionPlane, adsk.core.ValueInput.createByReal(height))
    offsetPlane = planes.add(planeInput)

    # Step 2: Sketch 1 - circle on XY plane
    sketch1 = rootComp.sketches.add(rootComp.xYConstructionPlane)
    sketch1.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), radius1
    )
    profile1 = sketch1.profiles.item(0)

    # Step 3: Sketch 2 - circle on offset plane
    sketch2 = rootComp.sketches.add(offsetPlane)
    sketch2.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), radius2
    )
    profile2 = sketch2.profiles.item(0)

    # Step 4: Create loft feature
    loftFeats = rootComp.features.loftFeatures
    loftInput = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    loftInput.loftSections.add(profile1)
    loftInput.loftSections.add(profile2)
    loftInput.isSolid = True
    loft = loftFeats.add(loftInput)

    # Best practice: name body immediately
    body = loft.bodies.item(0)
    body.name = name
    return loft

create_loft(3, 1.5, 5, "Loft")
