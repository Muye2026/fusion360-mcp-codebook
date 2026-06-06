# === Function: create_cylinder ===
# Description: Create a parametric cylinder at origin
# Parameters: radius (mm), height (mm), name (str)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# Best practice: Name body immediately after creation

import adsk.core, adsk.fusion

def create_cylinder(radius=5, height=20, name="Cylinder"):
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), radius
    )

    profile = sketch.profiles.item(0)
    extrudeFeats = rootComp.features.extrudeFeatures
    extrudeInput = extrudeFeats.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(height)
    extrudeInput.setDistanceExtent(False, distance)
    extrude = extrudeFeats.add(extrudeInput)
    
    # Best practice: name body immediately
    body = extrude.bodies.item(0)
    body.name = name
    return extrude

create_cylinder(5, 20, "Cylinder")
