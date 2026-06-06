# === Function: create_sphere ===
# Description: Create a sphere by revolving a semi-circle 360 degrees
# Parameters: radius (cm), name (str)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# API Reference: revolveFeatures.createInput(), revolveFeatures.add()
# Note: SphereFeatures has no add() method. Sphere is created via RevolveFeature.
# Best practice: Name body immediately after creation

import adsk.core, adsk.fusion

def create_sphere(radius=5, name="Sphere"):
    """
    Create a sphere by revolving a semi-circle 360 degrees.
    
    Args:
        radius: Radius of the sphere (cm)
        name: Name for the resulting body
    
    Returns:
        The created RevolveFeature object
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    # Create sketch on XZ plane
    sketch = rootComp.sketches.add(rootComp.xZConstructionPlane)

    # Draw axis line (vertical, from bottom to top)
    axisLine = sketch.sketchCurves.sketchLines.addByTwoPoints(
        adsk.core.Point3D.create(0, -radius, 0),
        adsk.core.Point3D.create(0, radius, 0)
    )

    # Draw semi-circle arc
    arc = sketch.sketchCurves.sketchArcs.addByThreePoints(
        adsk.core.Point3D.create(-radius, 0, 0),
        adsk.core.Point3D.create(0, radius, 0),
        adsk.core.Point3D.create(radius, 0, 0)
    )

    # Close the bottom with a horizontal line (ensures clean profile)
    sketch.sketchCurves.sketchLines.addByTwoPoints(
        adsk.core.Point3D.create(-radius, 0, 0),
        adsk.core.Point3D.create(radius, 0, 0)
    )

    # Get profile (the semicircle area)
    profile = sketch.profiles.item(0)

    # Revolve 360 degrees around axis
    revFeats = rootComp.features.revolveFeatures
    revInput = revFeats.createInput(
        profile,
        axisLine,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    revInput.setAngleExtent(False, adsk.core.ValueInput.createByString('360 deg'))
    revolve = revFeats.add(revInput)

    # Best practice: name body immediately
    body = revolve.bodies.item(0)
    body.name = name
    return revolve

create_sphere(5, "Sphere")
