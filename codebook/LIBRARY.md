# Fusion 360 MCP Codebook — Library Index

Quick reference for all tested Fusion 360 API code snippets.
Each entry links to the source file and shows test status.

## Status Legend
- ✓ PASSED — tested and working
- ✗ FAILED — tested, needs debugging
- ? UNTESTED — not yet tested

---

## Basic Shapes (basic_shapes/)

| Function | File | Status | Notes |
|----------|------|--------|-------|
| create_cube | [create_cube.py](basic_shapes/create_cube.py) | ✓ PASSED | Parametric cube at origin |
| create_cylinder | [create_cylinder.py](basic_shapes/create_cylinder.py) | ✓ PASSED | radius=5, height=20 |
| create_sphere | [create_sphere.py](basic_shapes/create_sphere.py) | ✓ PASSED | Via RevolveFeature (SphereFeatures has no add) |
| create_loft | [create_loft.py](basic_shapes/create_loft.py) | ✓ PASSED | Two circular profiles with offset plane |
| create_cone | [create_cone.py](basic_shapes/create_cone.py) | ✓ PASSED | Revolve triangle profile 360° around Y axis |
| create_torus | [create_torus.py](basic_shapes/create_torus.py) | ✓ PASSED | Sweep circular profile along circular path (NOT revolve — ASM_PATH_TANGENT) |

---

## Features (features/)

| Function | File | Status | Notes |
|----------|------|--------|-------|
| fillet_edge | [fillet_edge.py](features/fillet_edge.py) | ✓ PASSED | Constant radius fillet, uses ObjectCollection |
| chamfer_edge | [chamfer_edge.py](features/chamfer_edge.py) | ✓ PASSED | Equal distance chamfer, uses createInput2() |
| create_hole | [create_hole.py](features/create_hole.py) | ✓ PASSED | Simple hole, setPositionByPoint(face, point) |
| create_shell | [create_shell.py](features/create_shell.py) | ✓ PASSED | Shell with face removal, createInput(facesToRemove, isTangentChain) |
| draft_face | [draft_faces.py](features/draft_faces.py) | ✓ PASSED | Draft angle on side faces, pull plane + single angle |
| thread_feature | [create_thread.py](features/create_thread.py) | ✓ PASSED | M20x2.5 external thread, isModeled=True |
| combine_bodies | [combine_bodies.py](features/combine_bodies.py) | ✓ PASSED | Join/cut/intersect bodies, createInput(targetBody, toolBodies) |
| split_body | [split_body.py](features/split_body.py) | ✓ PASSED | Split body with plane, createInput(body, splittingTool, isExtended) |
| move_body | [move_body.py](features/move_body.py) | ✓ PASSED | Move body by translation, createInput(bodies, matrix) |
| delete_face | [delete_face.py](features/delete_face.py) | ✓ PASSED | Delete face (solid→surface), SurfaceDeleteFaceFeatures.add(face) |

---

## Surfaces (surfaces/)

| Function | File | Status | Notes |
|----------|------|--------|-------|
| create_sweep | [create_sweep.py](surfaces/create_sweep.py) | ✓ PASSED | Path.create(curve, chainedCurves), profile ⊥ path |
| patch_surface | [patch_surface.py](surfaces/patch_surface.py) | ✓ PASSED | Patch from profile, createInput(profile, NewBodyFeatureOperation) |
| offset_surface | [offset_surface.py](surfaces/offset_surface.py) | ✓ PASSED | Offset face by distance, createInput(faces, distance, operation) |
| thicken_surface | [thicken_surface.py](surfaces/thicken_surface.py) | ✓ PASSED | Thicken patch body, createInput(bodies, thickness, isSymmetric, operation) |
| stitch_surface | [stitch_surface.py](surfaces/stitch_surface.py) | ✓ PASSED | Stitch surfaces, createInput(bodies, tolerance, operation) |
| trim_surface | [trim_surface.py](surfaces/trim_surface.py) | ✓ PASSED | Trim surface, createInput(trimTool), select cells on trimInput |

---

## Transforms (transforms/)

| Function | File | Status | Notes |
|----------|------|--------|-------|
| mirror_body | [mirror_bodies.py](features/mirror_bodies.py) | ✓ PASSED | Mirror body across YZ plane, createInput(entities, plane) |
| rotate_body | [rotate_body.py](features/rotate_body.py) | ✓ PASSED | MoveFeatures with Matrix3D.setToRotation(angleRad, axis, origin) |
| circular_pattern | [circular_pattern.py](features/circular_pattern.py) | ✓ PASSED | 4 instances, 360° around Z axis, pattern body not feature |
| rectangular_pattern | [rectangular_pattern.py](features/rectangular_pattern.py) | ✓ PASSED | 2x2 pattern, 20mm spacing, createInput needs PatternDistanceType |

---

## Assembly (assembly/)

| Function | File | Status | Notes |
|----------|------|--------|-------|
| create_component | [create_component.py](assembly/create_component.py) | ✓ PASSED | `addNewComponent(transform)` — requires Matrix3D, not None |
| joint_revolve | [joint_revolve.py](assembly/joint_revolve.py) | ✓ PASSED | `JointGeometry.createByPoint(vertex)`, `setAsRevoluteJointMotion(JointDirections)` |
| contact_set | [contact_set.py](assembly/contact_set.py) | ✓ PASSED | `design.contactSets.add([occ1, occ2])` — on design, not rootComp; takes list, not ObjectCollection |

---

## Export (export/)

| Function | File | Status | Notes |
|----------|------|--------|-------|
| capture_viewport | MCP tool | ✓ PASSED | MCP tool: capture_viewport (width, height) |
| export_step | [export_step.py](export/export_step.py) | ✓ PASSED | Export component to STEP, createSTEPExportOptions(filename, component) |
| export_stl | [export_stl.py](export/export_stl.py) | ✓ PASSED | Export body to STL, createSTLExportOptions(**body**, filename) — pass BRepBody not Component |
| mass_properties | [mass_properties.py](export/mass_properties.py) | ✓ PASSED | Get mass/volume/area/density, body.physicalProperties |
| export_iges | [export_iges.py](export/export_iges.py) | ✓ PASSED | createIGESExportOptions(filepath, component), same pattern as STEP |

---

## API Documentation References

| Resource | Location | Description |
|----------|------|-------------|
| Autodesk Fusion API documentation | https://help.autodesk.com/view/fusion360/ENU/ | Official API reference |
| Autodesk Fusion MCP documentation | https://help.autodesk.com/view/ADSKMCP/ENU/ | Official local MCP endpoint documentation |
| Brepwright Design Guide | MCP tool: `fetch_design_guide` | Compact project-specific API lessons |
| Runtime API Discovery | MCP tool: `fetch_api_documentation` | Introspects available `adsk.core` and `adsk.fusion` symbols |

### How to Look Up API Documentation

1. **Discover** — Use `fetch_api_documentation` to find relevant classes and methods available in the local Fusion runtime.
2. **Confirm** — Open Autodesk's official API documentation for exact signatures and behavior.
3. **Implement** — Prefer an existing Codebook script before writing a new API pattern.
4. **Verify** — Record live Fusion behavior before promoting the pattern into a Brepwright tool.

---

## Key API Lessons Learned

| Feature | Pitfall | Correct Usage |
|---------|---------|---------------|
| Extrude | `add(profile, extent, operation)` ❌ | `createInput()` + `setDistanceExtent()` + `add(input)` ✓ |
| Fillet | Pass Python list ❌ | Wrap in `ObjectCollection.create()` ✓ |
| Chamfer | `createInput(bodies)` ❌ | `createInput2()` ✓ |
| Hole | `setPositionByPoint(point)` ❌ | `setPositionByPoint(face, point)` — needs BOTH args ✓ |
| Shell | Pass body directly ❌ | `createInput(ObjectCollection_of_faces, isTangentChain)` ✓ |
| Sweep | Profile on same plane as path ❌ | Profile must be ⊥ to path direction ✓ |
| Loft | `constructPlanes` ❌ | `constructionPlanes` ✓ |
| Sphere | `SphereFeatures.add()` ❌ | Use `RevolveFeature` with semi-circle ✓ |
| Draft | Include top/bottom faces ❌ | Identify side faces via `face.geometry.normal` (z~0 for XY pull) ✓ |
| Thread | `body.sideFaces` attribute ❌ | Iterate `body.faces`, check `hasattr(face.geometry, 'radius')` for cylindrical face ✓ |
| Rectangular Pattern | Distance in mm ❌ | Convert mm→cm (÷10.0), use `PatternDistanceType.SpacingPatternDistanceType` ✓ |
| Circular Pattern | Pattern hole feature (intersects) ❌ | Pattern **body** not feature, `ObjectCollection.createWithArray([body])` ✓ |
| Mirror | Pass body list directly ❌ | Wrap body in `ObjectCollection`, pass to `mirrorFeatures.createInput(entities, plane)` ✓ |
| Trim Surface | `add(trimInput)` before selecting cells ❌ | Get cells via `trimInput.bRepCells`, set `isSelected=True`, then `add(trimInput)` ✓ |
| Split Body | Use construction plane that coincides with body face ❌ | Use offset plane that cuts through interior; set `isExtended=True` ✓ |
| Move Body | `matrix.setToTranslation(vector)` ❌ | `matrix.translation = vector` (property assignment, not method call) ✓ |
| Delete Face | `DeleteFaceFeatures.add(face)` fails if gap not fillable ❌ | Use `SurfaceDeleteFaceFeatures.add(face)` — converts solid to open surface ✓ |
| STL Export | Pass `rootComp` (Component) to `createSTLExportOptions` ❌ | Pass `BRepBody` object: `rootComp.bRepBodies.item(0)` ✓ |
| Assembly | `occurrences.addNewComponent(None)` ❌ | `addNewComponent(Matrix3D.create())` — requires Matrix3D, not None ✓ |
| Assembly | `JointGeometry.create(point, occ, keyPointType)` ❌ | `JointGeometry.createByPoint(BRepVertex)` — static method, not `create()` ✓ |
| Assembly | `setAsRevoluteJointMotion(Vector3D)` ❌ | `setAsRevoluteJointMotion(JointDirections.ZAxisJointDirection)` — takes enum, not Vector3D ✓ |
| Assembly | `rootComp.contactSets.add(ObjectCollection)` ❌ | `design.contactSets.add([occ1, occ2])` — on design not rootComp, takes Python list ✓ |
| Torus | RevolveFeatures with circular profile ❌ | Use SweepFeatures (circular profile along circular path) — revolve fails with ASM_PATH_TANGENT ✓ |

---

## How to Use

1. **Find the function** you need in this index
2. **Open the .py file** to see the working code
3. **Copy the function** into your AI prompt or MCP `execute_python` call
4. **Adjust parameters** (dimensions, positions) as needed
5. **Send to Fusion 360** via MCP

### Example: Create a filleted cube with a hole

```python
import adsk.core, adsk.fusion

app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

# Step 1: Create cube
sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
sketch.sketchCurves.sketchLines.addTwoPointRectangle(
    adsk.core.Point3D.create(0, 0, 0),
    adsk.core.Point3D.create(10, 10, 0)
)
profile = sketch.profiles.item(0)
extInput = rootComp.features.extrudeFeatures.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(10))
extrude = rootComp.features.extrudeFeatures.add(extInput)
body = extrude.bodies.item(0)
body.name = "MyCube"

# Step 2: Fillet edges
edgesCol = adsk.core.ObjectCollection.create()
for i in range(body.edges.count):
    edgesCol.add(body.edges.item(i))
filletInput = rootComp.features.filletFeatures.createInput()
filletInput.addConstantRadiusEdgeSet(edgesCol, adsk.core.ValueInput.createByReal(1.0), False)
rootComp.features.filletFeatures.add(filletInput)

# Step 3: Drill hole on top face
topFace = None
for i in range(body.faces.count):
    face = body.faces.item(i)
    if hasattr(face.geometry, 'normal') and face.geometry.normal.z > 0.9:
        topFace = face
        break
if topFace:
    holeInput = rootComp.features.holeFeatures.createSimpleInput(adsk.core.ValueInput.createByReal(1.0))
    holeInput.setPositionByPoint(topFace, adsk.core.Point3D.create(5, 5, 10))
    holeInput.setDistanceExtent(adsk.core.ValueInput.createByReal(5))
    rootComp.features.holeFeatures.add(holeInput)
```

---

## Contributing

When you fix a ✗ FAILED or test a ? UNTESTED function:
1. Write the working code in the appropriate `/<category>/<function_name>.py`
2. Update this `LIBRARY.md` with ✓ PASSED status
3. Update `README.md` test status table
