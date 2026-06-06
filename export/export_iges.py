# === Function: export_iges ===
# Description: Export the current design to an IGES file
# Parameters: filepath (str), component (Component)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# Best practice: Same pattern as STEP/STL export — createIGESExportOptions(filepath, component)

import adsk.core, adsk.fusion

def export_iges(filepath='/tmp/export.iges', component=None):
    """
    Export the current design (or specified component) to an IGES file.
    
    Args:
        filepath (str): Output file path (default '/tmp/export.iges')
        component (Component): Component to export (default rootComponent)
    
    Returns:
        bool: True if export succeeded, False otherwise
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    
    if component is None:
        component = design.rootComponent
    
    exportMgr = design.exportManager
    igesOptions = exportMgr.createIGESExportOptions(filepath, component)
    result = exportMgr.execute(igesOptions)
    
    return result

if export_iges('/tmp/test_export.iges'):
    print("IGES export succeeded")
else:
    print("ERROR: IGES export failed")
