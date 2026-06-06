# === Function: create_component ===
# Description: Create a new component in an assembly document
# Parameters: name (string) - name for the new component
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# Best practice: addNewComponent(transform) requires Matrix3D, not None

import adsk.core, adsk.fusion

def create_component(name="NewComponent"):
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    # Add new component to root assembly
    # addNewComponent(transform) - requires Matrix3D, not None
    transform = adsk.core.Matrix3D.create()
    occ = rootComp.occurrences.addNewComponent(transform)
    newComp = occ.component
    newComp.name = name

    return occ

create_component("TestComponent")
