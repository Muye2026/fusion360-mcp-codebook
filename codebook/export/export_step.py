"""
Test 7.2: Export STEP
Export the current design to a STEP file.
"""

import adsk.core, adsk.fusion

app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

# Export to STEP file
exportMgr = design.exportManager
stepOptions = exportMgr.createSTEPExportOptions('/tmp/test_export.step', rootComp)
result = exportMgr.execute(stepOptions)

if result:
    print("STEP export succeeded")
else:
    print("ERROR: STEP export failed")
