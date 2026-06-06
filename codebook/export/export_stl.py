"""
Test 7.3: Export STL
Export a body to an STL file.
"""

import adsk.core, adsk.fusion

app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

# Step1: Create a simple cube
sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
sketch.sketchCurves.sketchLines.addTwoPointRectangle(
    adsk.core.Point3D.create(0, 0, 0),
    adsk.core.Point3D.create(5, 5, 0)
)
profile = sketch.profiles.item(0)
extInput = rootComp.features.extrudeFeatures.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(5))
extrude = rootComp.features.extrudeFeatures.add(extInput)
body = extrude.bodies.item(0)
body.name = "CubeForSTL"

# Step2: Export to STL file
exportMgr = design.exportManager
stlOptions = exportMgr.createSTLExportOptions(body, '/tmp/test_export.stl')
result = exportMgr.execute(stlOptions)

if result:
    print(f"STL export succeeded for body: {body.name}")
else:
    print("ERROR: STL export failed")
