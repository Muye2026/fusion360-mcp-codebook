# Fusion 360 MCP Codebook

> A curated, tested Python code library for Fusion 360 MCP operations.
> Works with any Fusion 360 MCP Server (frankhommers, AuraFriday, Autodesk official).

## Why this exists

When AI writes Fusion 360 API code, it often gets the API signatures wrong — wrong parameter types, wrong method calls, wrong object construction patterns. This library provides **tested, ready-to-use** code snippets that AI can directly execute via MCP.

## Architecture

```
AI (WorkBuddy / Cursor / Codex)
    │
    │  MCP Protocol (HTTP/SSE)
    ▼
Fusion 360 MCP Server (frankhommers / AuraFriday / official)
    │
    │  execute_python / execute_api_script
    ▼
Fusion 360 API (adsk.core / adsk.fusion)
    │
    ▼  (uses code from this library)
3D Model created ✓
```

## Directory structure

```
fusion360-mcp-codebook/
├── api_docs/          # Fusion 360 API reference & search database
├── basic_shapes/      # Primitives: cube, cylinder, sphere, torus, cone
├── features/          # Feature operations: extrude, fillet, chamfer, hole, shell, draft, thread
├── surfaces/          # Surface operations: loft, sweep, patch, offset, thicken, split
├── transforms/        # Transforms: move, rotate, mirror, pattern (circular/rectangular)
├── assembly/          # Assembly: components, joints, contacts
├── export/            # Export: STEP, STL, IGES, screenshot
├── LIBRARY.md         # Quick reference index of all functions
└── README.md          # This file
```

## Code conventions

Each code snippet follows this format:

```python
# === Function: create_cube ===
# Description: Create a parametric cube at origin
# Parameters: width (mm), height (mm), depth (mm)
# Tested: 2026-06-05 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED

import adsk.core, adsk.fusion

def create_cube(width=10, height=10, depth=10):
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(width, height, 0)
    )

    profile = sketch.profiles.item(0)
    extrudeFeats = rootComp.features.extrudeFeatures
    extInput = extrudeFeats.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(depth)
    extInput.setDistanceExtent(False, distance)
    return extrudeFeats.add(extInput)

create_cube(10, 10, 10)
```

## Test status

> Last updated: 2026-06-06 | Fusion 360 v2703.1.11 (Mac, Apple Silicon) | MCP: frankhommers v1.0.0

| Category | Total | Passed | Failed | Untested |
|----------|-------|--------|--------|----------|
| Basic shapes | 6 | 4 | 0 | 2 (cone, torus) |
| Features | 10 | 10 | 0 | 0 |
| Surfaces | 6 | 6 | 0 | 0 |
| Transforms | 4 | 3 | 0 | 1 (rotate_body) |
| Assembly | 3 | 3 | 0 | 0 |
| Export | 5 | 4 | 0 | 1 (export_iges) |
| **Total** | **34** | **30** | **0** | **4** |

> **Assembly note**: `addNewComponent` requires Matrix3D (not None), `ContactSets` is on `design` not `rootComp`, `JointGeometry` uses `createByPoint()` not `create()`.

## Usage with AI

When using this library with an AI assistant:

1. AI reads the relevant snippet from the codebook
2. AI adjusts parameters (dimensions, positions) as needed
3. AI sends the code via MCP `execute_python` tool
4. Fusion 360 executes and creates the 3D model

## License

MIT License — free to use, modify, and distribute.

## Contributing

Contributions welcome! Please ensure:
- All code is tested on a real Fusion 360 instance
- Follow the code conventions above
- Include the test status header comment
