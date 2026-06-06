# === Function: create_cube ===
# Description: Create a parametric cube at origin
# Parameters: width (mm), height (mm), depth (mm)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# Best practice: Name body immediately after creation

import adsk.core, adsk.fusion

def create_cube(width=10, height=10, depth=10, name="Cube"):
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(width, height, 0)
    )

    profile = sketch.profiles.item(0)
    extrudeFeats = rootComp.features.extrudeFeatures
    extInput = extrudeFeats.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(depth)
    extInput.setDistanceExtent(False, distance)
    extrude = extrudeFeats.add(extInput)
    
    # Best practice: name body immediately
    body = extrude.bodies.item(0)
    body.name = name
    return extrude

create_cube(10, 10, 10, "Cube")
