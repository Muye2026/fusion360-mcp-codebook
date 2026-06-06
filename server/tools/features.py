"""Features MCP Tools — 10 domain-specific tools for feature operations.

Each tool generates Python code based on tested codebook patterns,
and executes via FusionBridge.
"""

from pydantic import Field

from server.app import mcp
from server.bridge import bridge
from server import config


# ─── fillet_edge ────────────────────────────────────────────────────────

@mcp.tool()
async def fillet_edge(
    body_index: int = Field(default=0, description="Index of the body (0-based)"),
    radius: float = Field(default=2, description="Fillet radius in mm"),
    all_edges: bool = Field(default=True, description="Fillet all edges (True) or only first edge (False)"),
) -> str:
    """Add a constant radius fillet to edges of a body in Fusion 360.

    Uses ObjectCollection for edge selection. Radius is in millimeters.
    """
    r = radius * config.MM_TO_CM

    if all_edges:
        edge_code = f'''edgesCol = adsk.core.ObjectCollection.create()
for i in range(body.edges.count):
    edgesCol.add(body.edges.item(i))'''
    else:
        edge_code = '''edgesCol = adsk.core.ObjectCollection.create()
edgesCol.add(body.edges.item(0))'''

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    {edge_code}
    filletFeats = rootComp.features.filletFeatures
    filletInput = filletFeats.createInput()
    filletInput.addConstantRadiusEdgeSet(edgesCol, adsk.core.ValueInput.createByReal({r}), False)
    fillet = filletFeats.add(filletInput)
    print(f"Fillet created: r={radius}mm on body {body.name}")
'''
    return await bridge.execute_python(code)


# ─── chamfer_edge ───────────────────────────────────────────────────────

@mcp.tool()
async def chamfer_edge(
    body_index: int = Field(default=0, description="Index of the body (0-based)"),
    distance: float = Field(default=1, description="Chamfer distance in mm"),
    all_edges: bool = Field(default=True, description="Chamfer all edges (True) or only first edge (False)"),
) -> str:
    """Add a chamfer to edges of a body in Fusion 360.

    Uses createInput2() for edge chamfer. Distance is in millimeters.
    """
    d = distance * config.MM_TO_CM

    if all_edges:
        edge_code = f'''edgesCol = adsk.core.ObjectCollection.create()
for i in range(body.edges.count):
    edgesCol.add(body.edges.item(i))'''
    else:
        edge_code = '''edgesCol = adsk.core.ObjectCollection.create()
edgesCol.add(body.edges.item(0))'''

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    {edge_code}
    chamferFeats = rootComp.features.chamferFeatures
    chamferInput = chamferFeats.createInput2()
    offset = adsk.core.ValueInput.createByReal({d})
    chamferInput.chamferEdgeSets.addEqualDistanceChamferEdgeSet(edgesCol, offset, True)
    chamfer = chamferFeats.add(chamferInput)
    print(f"Chamfer created: d={distance}mm on body {body.name}")
'''
    return await bridge.execute_python(code)


# ─── create_hole ────────────────────────────────────────────────────────

@mcp.tool()
async def create_hole(
    diameter: float = Field(default=2, description="Hole diameter in mm"),
    depth: float = Field(default=5, description="Hole depth in mm"),
    x: float = Field(default=0, description="Hole center X position in mm"),
    y: float = Field(default=0, description="Hole center Y position in mm"),
    body_index: int = Field(default=0, description="Index of the body to drill into (0-based)"),
) -> str:
    """Create a simple hole on the top face of a body in Fusion 360.

    Automatically finds the top face (normal pointing +Z) and drills a hole at the specified position.
    All dimensions are in millimeters.
    """
    d = diameter * config.MM_TO_CM
    dep = depth * config.MM_TO_CM
    px = x * config.MM_TO_CM
    py = y * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    # Find top face (normal pointing +Z)
    topFace = None
    for i in range(body.faces.count):
        face = body.faces.item(i)
        normal = face.geometry.normal if hasattr(face.geometry, 'normal') else None
        if normal and normal.z > 0.9:
            topFace = face
            break

    if topFace:
        holeFeats = rootComp.features.holeFeatures
        holeInput = holeFeats.createSimpleInput(adsk.core.ValueInput.createByReal({d}))
        holeInput.setPositionByPoint(topFace, adsk.core.Point3D.create({px}, {py}, 0))
        holeInput.setDistanceExtent(adsk.core.ValueInput.createByReal({dep}))
        hole = holeFeats.add(holeInput)
        print(f"Hole created: dia={diameter}mm, depth={depth}mm at ({x},{y})mm")
    else:
        print("ERROR: No top face found on body")
'''
    return await bridge.execute_python(code)


# ─── create_shell ───────────────────────────────────────────────────────

@mcp.tool()
async def create_shell(
    thickness: float = Field(default=2, description="Wall thickness in mm"),
    body_index: int = Field(default=0, description="Index of the body to shell (0-based)"),
    remove_top_face: bool = Field(default=True, description="Remove top face to open the shell"),
) -> str:
    """Create a shell feature by removing a face and hollowing a body in Fusion 360.

    Uses createInput(ObjectCollection_of_faces, isTangentChain). Thickness is in millimeters.
    """
    t = thickness * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    # Find top face to remove
    topFace = None
    for i in range(body.faces.count):
        face = body.faces.item(i)
        normal = face.geometry.normal if hasattr(face.geometry, 'normal') else None
        if normal and normal.z > 0.9:
            topFace = face
            break

    if not topFace and {remove_top_face}:
        print("ERROR: No top face found to remove")
    else:
        facesToRemove = adsk.core.ObjectCollection.create()
        if {remove_top_face} and topFace:
            facesToRemove.add(topFace)
        shellFeats = rootComp.features.shellFeatures
        shellInput = shellFeats.createInput(facesToRemove, True)
        shellInput.insideThickness = adsk.core.ValueInput.createByReal({t})
        shell = shellFeats.add(shellInput)
        print(f"Shell created: thickness={thickness}mm on body {body.name}")
'''
    return await bridge.execute_python(code)


# ─── create_thread ──────────────────────────────────────────────────────

@mcp.tool()
async def create_thread(
    body_name: str = Field(description="Name of the target body with a cylindrical face"),
    thread_designation: str = Field(default="M20x2.5", description="Thread designation (e.g., M20x2.5, M10x1.5)"),
    thread_type: str = Field(default="ISO Metric profile", description="Thread type (e.g., 'ISO Metric profile')"),
    thread_class: str = Field(default="4g6g", description="Thread class (e.g., '4g6g' for external)"),
    is_external: bool = Field(default=True, description="True for external thread, False for internal"),
) -> str:
    """Create a thread feature on a cylindrical face of a body in Fusion 360.

    Automatically finds the first cylindrical face on the named body.
    Uses ThreadFeatures.createInput() with isModeled=True for physical threads.
    """
    is_internal = "True" if not is_external else "False"

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

# Find the target body by name
body = None
for i in range(rootComp.bRepBodies.count):
    b = rootComp.bRepBodies.item(i)
    if b.name == "{body_name}":
        body = b
        break

if not body:
    print("ERROR: Body {body_name} not found")
else:
    # Find cylindrical face
    cyl_face = None
    for j in range(body.faces.count):
        face = body.faces.item(j)
        if hasattr(face.geometry, 'radius'):
            cyl_face = face
            break

    if not cyl_face:
        print("ERROR: No cylindrical face found on body {body_name}")
    else:
        threadFeatures = rootComp.features.threadFeatures
        threadInfo = threadFeatures.createThreadInfo(
            {is_internal},
            "{thread_type}",
            "{thread_designation}",
            "{thread_class}"
        )
        faces = adsk.core.ObjectCollection.create()
        faces.add(cyl_face)
        threadInput = threadFeatures.createInput(faces, threadInfo)
        threadInput.isFullLength = True
        threadInput.isModeled = True
        thread = threadFeatures.add(threadInput)
        print(f"Thread created: {thread_designation} on {body_name}")
'''
    return await bridge.execute_python(code)


# ─── draft_faces ────────────────────────────────────────────────────────

@mcp.tool()
async def draft_faces(
    body_name: str = Field(description="Name of the target body"),
    angle_deg: float = Field(default=5, description="Draft angle in degrees"),
    pull_plane: str = Field(default="XY", description="Pull direction plane: 'XY', 'XZ', or 'YZ'"),
) -> str:
    """Apply draft angle to side faces of a body in Fusion 360.

    Automatically identifies side faces based on the pull plane direction.
    Uses draftFeatures.createInput() with setSingleAngle().
    """
    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

# Find the target body
body = None
for i in range(rootComp.bRepBodies.count):
    b = rootComp.bRepBodies.item(i)
    if b.name == "{body_name}":
        body = b
        break

if not body:
    print("ERROR: Body {body_name} not found")
else:
    # Find side faces
    side_faces = []
    for i in range(body.faces.count):
        face = body.faces.item(i)
        normal = face.geometry.normal
        if "{pull_plane}" == "XY":
            if abs(normal.z) < 0.1:
                side_faces.append(face)
        elif "{pull_plane}" == "XZ":
            if abs(normal.y) < 0.1:
                side_faces.append(face)
        elif "{pull_plane}" == "YZ":
            if abs(normal.x) < 0.1:
                side_faces.append(face)

    if not side_faces:
        print("ERROR: No side faces found for pull plane {pull_plane}")
    else:
        if "{pull_plane}" == "XY":
            pull_direction = rootComp.xYConstructionPlane
        elif "{pull_plane}" == "XZ":
            pull_direction = rootComp.xZConstructionPlane
        elif "{pull_plane}" == "YZ":
            pull_direction = rootComp.yZConstructionPlane
        angle = adsk.core.ValueInput.createByString('{angle_deg} deg')
        draftFeats = rootComp.features.draftFeatures
        draftInput = draftFeats.createInput(side_faces, pull_direction)
        draftInput.setSingleAngle(True, angle)
        draft = draftFeats.add(draftInput)
        print(f"Draft created: {angle_deg} deg on {body_name}")
'''
    return await bridge.execute_python(code)


# ─── combine_bodies ─────────────────────────────────────────────────────

@mcp.tool()
async def combine_bodies(
    target_body_index: int = Field(description="Index of the target body (0-based)"),
    tool_body_indices: list = Field(description="List of tool body indices (0-based)"),
    operation: str = Field(default="join", description="Operation: 'join', 'cut', or 'intersect'"),
) -> str:
    """Combine (join/cut/intersect) multiple bodies in Fusion 360.

    Uses combineFeatures.createInput(targetBody, toolBodies).
    """
    op_map = {"join": "JoinFeatureOperation", "cut": "CutFeatureOperation", "intersect": "IntersectFeatureOperation"}
    fusion_op = op_map.get(operation, "JoinFeatureOperation")
    indices_str = str(tool_body_indices)

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

target = rootComp.bRepBodies.item({target_body_index})
if not target:
    print("ERROR: Target body not found at index {target_body_index}")
else:
    tool_coll = adsk.core.ObjectCollection.create()
    for idx in {indices_str}:
        b = rootComp.bRepBodies.item(idx)
        if b:
            tool_coll.add(b)

    combineFeats = rootComp.features.combineFeatures
    combineInput = combineFeats.createInput(target, tool_coll)
    combineInput.operation = adsk.fusion.FeatureOperations.{fusion_op}
    combine = combineFeats.add(combineInput)
    print(f"Combine created: {operation} on body {target.name}")
'''
    return await bridge.execute_python(code)


# ─── split_body ─────────────────────────────────────────────────────────

@mcp.tool()
async def split_body(
    body_index: int = Field(default=0, description="Index of the body to split (0-based)"),
    offset_distance: float = Field(default=5, description="Offset distance of splitting plane from XY plane in mm"),
    is_tool_extended: bool = Field(default=True, description="Extend tool to fully intersect body"),
) -> str:
    """Split a body with an offset construction plane in Fusion 360.

    Creates an offset plane from the XY plane and uses it as the splitting tool.
    All dimensions are in millimeters.
    """
    d = offset_distance * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    # Create offset plane as splitting tool
    planes = rootComp.constructionPlanes
    planeInput = planes.createInput()
    planeInput.setByOffset(rootComp.xYConstructionPlane, adsk.core.ValueInput.createByReal({d}))
    offsetPlane = planes.add(planeInput)

    splitFeats = rootComp.features.splitBodyFeatures
    splitInput = splitFeats.createInput(body, offsetPlane, {str(is_tool_extended)})
    split = splitFeats.add(splitInput)
    print(f"Split created: body {body.name} at offset {offset_distance}mm")
'''
    return await bridge.execute_python(code)


# ─── move_body ──────────────────────────────────────────────────────────

@mcp.tool()
async def move_body(
    body_index: int = Field(default=0, description="Index of the body to move (0-based)"),
    x: float = Field(default=0, description="Translation along X axis in mm"),
    y: float = Field(default=0, description="Translation along Y axis in mm"),
    z: float = Field(default=0, description="Translation along Z axis in mm"),
) -> str:
    """Move a body by translation in Fusion 360.

    Uses MoveFeatures with matrix.translation property assignment (not setToTranslation method).
    All dimensions are in millimeters.
    """
    dx = x * config.MM_TO_CM
    dy = y * config.MM_TO_CM
    dz = z * config.MM_TO_CM

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    translation = adsk.core.Vector3D.create({dx}, {dy}, {dz})
    matrix = adsk.core.Matrix3D.create()
    matrix.translation = translation
    bodies_coll = adsk.core.ObjectCollection.create()
    bodies_coll.add(body)
    moveFeats = rootComp.features.moveFeatures
    moveInput = moveFeats.createInput(bodies_coll, matrix)
    move = moveFeats.add(moveInput)
    print(f"Moved body {body.name} by ({x},{y},{z})mm")
'''
    return await bridge.execute_python(code)


# ─── delete_face ────────────────────────────────────────────────────────

@mcp.tool()
async def delete_face(
    body_index: int = Field(default=0, description="Index of the body (0-based)"),
    face_index: int = Field(default=0, description="Index of the face to delete (0-based)"),
) -> str:
    """Delete a face from a body in Fusion 360 (converts solid to surface).

    Uses SurfaceDeleteFaceFeatures.add() (not DeleteFaceFeatures, which requires gap fillability).
    """
    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

body = rootComp.bRepBodies.item({body_index})
if not body:
    print("ERROR: Body not found at index {body_index}")
else:
    face = body.faces.item({face_index})
    if not face:
        print("ERROR: Face not found at index {face_index}")
    else:
        faces_coll = adsk.core.ObjectCollection.create()
        faces_coll.add(face)
        deleteFeats = rootComp.features.surfaceDeleteFaceFeatures
        delete = deleteFeats.add(faces_coll)
        print(f"Deleted face {face_index} from body {body.name}")
'''
    return await bridge.execute_python(code)
