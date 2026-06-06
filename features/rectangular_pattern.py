# === Function: rectangular_pattern ===
# Description: Create rectangular pattern of features/bodies
# Parameters: input_entities (list), direction1_entity, direction2_entity, qty1, qty2, dist1, dist2
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/RectangularPatternFeatures_createInput.htm

import adsk.core, adsk.fusion

def rectangular_pattern(input_entities, direction1_entity, direction2_entity,
                      qty1=2, qty2=2, dist1=20, dist2=20):
    """
    Create rectangular pattern of features or bodies.
    
    Args:
        input_entities: List of features/bodies/occurrences to pattern
        direction1_entity: Entity defining first direction (edge/axis/line)
        direction2_entity: Entity defining second direction
        qty1: Number of instances in direction 1 (default 2)
        qty2: Number of instances in direction 2 (default 2)
        dist1: Distance between instances in direction 1 (mm, default 20)
        dist2: Distance between instances in direction 2 (mm, default 20)
    
    Returns:
        adsk.fusion.RectangularPatternFeature: The created pattern feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create ObjectCollection from input entities
    entities_coll = adsk.core.ObjectCollection.create()
    for entity in input_entities:
        entities_coll.add(entity)
    
    # Create rectangular pattern
    rectPatterns = rootComp.features.rectangularPatternFeatures
    
    rectInput = rectPatterns.createInput(
        entities_coll,
        direction1_entity,
        adsk.core.ValueInput.createByReal(qty1),
        adsk.core.ValueInput.createByReal(dist1 / 10.0),  # Convert mm to cm
        adsk.fusion.PatternDistanceType.SpacingPatternDistanceType
    )
    
    # Set direction 2
    rectInput.setDirectionTwo(
        direction2_entity,
        adsk.core.ValueInput.createByReal(qty2),
        adsk.core.ValueInput.createByReal(dist2 / 10.0)  # Convert mm to cm
    )
    
    rectPattern = rectPatterns.add(rectInput)
    
    print(f"Rectangular pattern created: {rectPattern.name}")
    return rectPattern

# Example usage (commented out - requires pre-existing hole feature and direction lines):
# hole_feat = rootComp.features.itemByName("Hole1")
# x_line = rootComp.sketches.item(0).sketchCurves.sketchLines.item(0)
# y_line = rootComp.sketches.item(0).sketchCurves.sketchLines.item(1)
# rectangular_pattern([hole_feat], x_line, y_line, 2, 2, 20, 20)
