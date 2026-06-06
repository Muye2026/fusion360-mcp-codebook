# === Function: create_sweep ===
# Description: Create a sweep feature by sweeping a profile along a path
# Parameters: profile_radius (cm), path_length (cm), path_offset_y (cm)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# API Reference: Path.create(curve, ChainedCurveOptions), sweepFeatures.createInput(profile, path, operation)
# Key insights:
#   - Path is created using Path.create(curve, chainedCurveOption), NOT a constructor
#   - Profile must be on a plane PERPENDICULAR to the path direction
#   - Path line must be at the same height as the profile center
#   - Error "ASM_PATH_TANGENT" means path is tangent to profile (wrong plane/position)

import adsk.core, adsk.fusion

def create_sweep_tube(profile_radius=0.5, path_length=10, name="SweepTube"):
    """
    Create a sweep tube by sweeping a circular profile along a straight path.
    
    Args:
        profile_radius: Radius of the circular cross-section (cm)
        path_length: Length of the sweep path along X axis (cm)
        name: Name for the resulting body
    
    Returns:
        The created SweepFeature object
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    # Step 1: Profile sketch on YZ plane (perpendicular to X-axis path)
    profileSketch = rootComp.sketches.add(rootComp.yZConstructionPlane)
    profileSketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), profile_radius
    )
    profileObj = profileSketch.profiles.item(0)

    # Step 2: Path sketch on XY plane (line along X axis at y=profile_radius)
    pathSketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    pathLine = pathSketch.sketchCurves.sketchLines.addByTwoPoints(
        adsk.core.Point3D.create(0, profile_radius, 0),
        adsk.core.Point3D.create(path_length, profile_radius, 0)
    )

    # Step 3: Create Path object
    path = adsk.fusion.Path.create(pathLine, adsk.fusion.ChainedCurveOptions.tangentChainedCurves)

    # Step 4: Create Sweep feature
    sweepFeats = rootComp.features.sweepFeatures
    sweepInput = sweepFeats.createInput(profileObj, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    sweepInput.orientation = adsk.fusion.SweepOrientationTypes.PerpendicularOrientationType
    sweep = sweepFeats.add(sweepInput)

    # Best practice: name body immediately
    body = sweep.bodies.item(0)
    body.name = name
    return sweep

create_sweep_tube(0.5, 10, "SweepTube")
