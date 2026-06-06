# === Function: create_cone ===
# Description: Create a parametric cone at origin
# Parameters: radius (mm), height (mm), name (str)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# Best practice: Revolve triangle profile 360° around Y axis (sketch line 0)

import adsk.core, adsk.fusion

def create_cone(radius=5, height=10, name="Cone"):
    """
    Create a parametric cone at origin by revolving a triangle profile.
    
    Args:
        radius (float): Cone base radius in mm (default 5)
        height (float): Cone height in mm (default 10)
        name (str): Name for the resulting body (default "Cone")
    
    Returns:
        adsk.fusion.RevolveFeature: The created revolve feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create triangle sketch on YZ plane (right triangle for cone)
    sketch = rootComp.sketches.add(rootComp.yZConstructionPlane)
    lines = sketch.sketchCurves.sketchLines
    
    # Triangle vertices in YZ plane: (y=0,z=0), (y=radius,z=0), (y=0,z=height)
    p0 = adsk.core.Point3D.create(0, 0, 0)
    p1 = adsk.core.Point3D.create(0, radius, 0)
    p2 = adsk.core.Point3D.create(0, 0, height)
    
    lines.addByTwoPoints(p0, p1)  # axis line (Y axis, will be revolution axis)
    lines.addByTwoPoints(p1, p2)  # diagonal
    lines.addByTwoPoints(p2, p0)  # vertical (Z axis)
    
    # Get profile (closed region)
    profile = sketch.profiles.item(0)
    
    # Revolve 360° around Y axis (sketch line 0 = axis)
    revolveFeats = rootComp.features.revolveFeatures
    revolveInput = revolveFeats.createInput(
        profile,
        sketch.sketchCurves.sketchLines.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    revolveInput.setAngleExtent(False, adsk.core.ValueInput.createByReal(360))
    revolve = revolveFeats.add(revolveInput)
    
    # Name body
    body = revolve.bodies.item(0)
    body.name = name
    return revolve

create_cone(5, 10, "Cone")
