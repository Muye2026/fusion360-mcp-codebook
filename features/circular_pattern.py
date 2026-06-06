# === Function: circular_pattern ===
# Description: Create circular pattern of features/bodies
# Parameters: input_entities (list), axis_entity, quantity, total_angle_deg
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/circularPatternFeatures_add_Sample.htm

import adsk.core, adsk.fusion

def circular_pattern(input_entities, axis_entity, quantity=4, total_angle_deg=360):
    """
    Create circular pattern of features or bodies.
    
    Args:
        input_entities: List of features/bodies/occurrences to pattern
        axis_entity: Entity defining axis (sketch line, edge, construction axis, etc.)
        quantity: Number of instances (default 4)
        total_angle_deg: Total angle in degrees (default 360)
    
    Returns:
        adsk.fusion.CircularPatternFeature: The created pattern feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Create ObjectCollection from input entities
    entities_coll = adsk.core.ObjectCollection.create()
    for entity in input_entities:
        entities_coll.add(entity)
    
    # Create circular pattern
    circPatterns = rootComp.features.circularPatternFeatures
    
    circInput = circPatterns.createInput(
        entities_coll,
        axis_entity
    )
    
    circInput.quantity = adsk.core.ValueInput.createByReal(quantity)
    circInput.totalAngle = adsk.core.ValueInput.createByString(f'{total_angle_deg} deg')
    circInput.isSymmetric = False
    
    circPattern = circPatterns.add(circInput)
    
    print(f"Circular pattern created: {circPattern.name}")
    return circPattern

# Example usage (commented out - requires pre-existing body and axis):
# box_body = rootComp.bRepBodies.itemByName("PatternBox")
# z_axis = rootComp.zConstructionAxis
# circular_pattern([box_body], z_axis, 4, 360)
