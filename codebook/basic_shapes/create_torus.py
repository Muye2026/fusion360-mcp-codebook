# === Function: create_torus ===
# Description: Create a parametric torus at origin
# Parameters: major_radius (mm), minor_radius (mm), name (str)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# Best practice: Use SweepFeatures (not RevolveFeatures — revolve fails with ASM_PATH_TANGENT)

import adsk.core, adsk.fusion

def create_torus(major_radius=10, minor_radius=3, name="Torus"):
    """
    Create a parametric torus at origin by sweeping a circle along a circular path.
    
    Args:
        major_radius (float): Distance from center to tube center in mm (default 10)
        minor_radius (float): Tube radius in mm (default 3)
        name (str): Name for the resulting body (default "Torus")
    
    Returns:
        adsk.fusion.SweepFeature: The created sweep feature
    
    API Pitfall:
        RevolveFeatures CANNOT create a torus — fails with ASM_PATH_TANGENT error.
        Must use SweepFeatures with a circular path and circular profile instead.
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    R = major_radius
    r = minor_radius
    
    # Step 1: Create circular path on XY plane (major circle)
    pathSketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    pathCircle = pathSketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), R
    )
    path = adsk.fusion.Path.create(pathCircle, adsk.fusion.ChainedCurveOptions.noChainedCurves)
    
    # Step 2: Create circular profile on XZ plane (minor circle at path start)
    profileSketch = rootComp.sketches.add(rootComp.xZConstructionPlane)
    profileCircle = profileSketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(R, 0, 0), r
    )
    profile = profileSketch.profiles.item(0)
    
    # Step 3: Sweep profile along path
    sweepFeats = rootComp.features.sweepFeatures
    sweepInput = sweepFeats.createInput(profile, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    sweep = sweepFeats.add(sweepInput)
    
    # Name body
    body = sweep.bodies.item(0)
    body.name = name
    return sweep

create_torus(10, 3, "Torus")
