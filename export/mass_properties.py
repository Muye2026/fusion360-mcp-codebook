"""
Test 7.4: Mass Properties
Get physical properties (mass, volume, area, density) of a body.
"""

import adsk.core, adsk.fusion

app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

# Get the first body from root component
if rootComp.bRepBodies.count > 0:
    body = rootComp.bRepBodies.item(0)
    print(f"Body: {body.name}")
    
    # Get physical properties
    props = body.physicalProperties
    if props:
        print(f"Mass: {props.mass} kg")
        print(f"Volume: {props.volume} cm3")
        print(f"Area: {props.area} cm2")
        print(f"Density: {props.density} kg/cm3")
        center = props.centerOfMass
        print(f"Center of Mass: ({center.x}, {center.y}, {center.z})")
    else:
        print("ERROR: Failed to get physical properties")
else:
    print("ERROR: No bodies found in root component")
