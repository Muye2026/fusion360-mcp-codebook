"""Features tools — direct Fusion API calls."""

import adsk.core
import adsk.fusion

MM_TO_CM = 0.1


def _get_root():
    app = adsk.core.Application.get()
    return app.activeProduct.rootComponent


def _find_body(body_name):
    """Find a body by name in root component."""
    rootComp = _get_root()
    for i in range(rootComp.bRepBodies.count):
        body = rootComp.bRepBodies.item(i)
        if body.name == body_name:
            return body
    raise ValueError(f'Body "{body_name}" not found')


def fillet_edge(args):
    body_name = args["body_name"]
    radius = args.get("radius", 1) * MM_TO_CM
    edge_index = args.get("edge_index", -1)

    body = _find_body(body_name)
    rootComp = _get_root()
    edgesCol = adsk.core.ObjectCollection.create()

    if edge_index >= 0:
        edgesCol.add(body.edges.item(edge_index))
    else:
        for i in range(body.edges.count):
            edgesCol.add(body.edges.item(i))

    filletFeats = rootComp.features.filletFeatures
    filletInput = filletFeats.createInput()
    filletInput.addConstantRadiusEdgeSet(edgesCol, adsk.core.ValueInput.createByReal(radius), False)
    filletFeats.add(filletInput)
    return f"Fillet applied: r={args.get('radius', 1)}mm on {body_name}"


def chamfer_edge(args):
    body_name = args["body_name"]
    distance = args.get("distance", 1) * MM_TO_CM
    edge_index = args.get("edge_index", -1)

    body = _find_body(body_name)
    rootComp = _get_root()
    edgesCol = adsk.core.ObjectCollection.create()

    if edge_index >= 0:
        edgesCol.add(body.edges.item(edge_index))
    else:
        for i in range(body.edges.count):
            edgesCol.add(body.edges.item(i))

    chamferFeats = rootComp.features.chamferFeatures
    chamferInput = chamferFeats.createInput2(edgesCol)
    chamferInput.setToEqualDistance(adsk.core.ValueInput.createByReal(distance))
    chamferFeats.add(chamferInput)
    return f"Chamfer applied: d={args.get('distance', 1)}mm on {body_name}"


def create_hole(args):
    body_name = args["body_name"]
    radius = args.get("radius", 1) * MM_TO_CM
    depth = args.get("depth", 5) * MM_TO_CM
    x = args.get("x", 0) * MM_TO_CM
    y = args.get("y", 0) * MM_TO_CM

    body = _find_body(body_name)
    rootComp = _get_root()

    # Find top face
    top_face = None
    for i in range(body.faces.count):
        face = body.faces.item(i)
        if hasattr(face.geometry, 'normal') and face.geometry.normal.z > 0.9:
            top_face = face
            break
    if not top_face:
        raise ValueError("No top face found")

    holeFeats = rootComp.features.holeFeatures
    holeInput = holeFeats.createSimpleInput(adsk.core.ValueInput.createByReal(radius))
    holeInput.setPositionByPoint(top_face, adsk.core.Point3D.create(x, y, top_face.pointOnFace.z))
    holeInput.setDistanceExtent(adsk.core.ValueInput.createByReal(depth))
    holeFeats.add(holeInput)
    return f"Hole created: r={args.get('radius', 1)}mm, d={args.get('depth', 5)}mm on {body_name}"


def create_shell(args):
    body_name = args["body_name"]
    thickness = args.get("thickness", 1) * MM_TO_CM
    face_index = args.get("face_index", 0)

    body = _find_body(body_name)
    rootComp = _get_root()

    face = body.faces.item(face_index)
    facesCol = adsk.core.ObjectCollection.create()
    facesCol.add(face)

    shellFeats = rootComp.features.shellFeatures
    shellInput = shellFeats.createInput(facesCol, True)
    shellInput.insideThickness = adsk.core.ValueInput.createByReal(thickness)
    shellFeats.add(shellInput)
    return f"Shell created: t={args.get('thickness', 1)}mm on {body_name}"


def create_thread(args):
    body_name = args["body_name"]
    is_modelled = args.get("is_modelled", True)

    body = _find_body(body_name)
    rootComp = _get_root()

    # Find cylindrical face
    cyl_face = None
    for i in range(body.faces.count):
        face = body.faces.item(i)
        if hasattr(face.geometry, 'radius'):
            cyl_face = face
            break
    if not cyl_face:
        raise ValueError("No cylindrical face found")

    threadFeats = rootComp.features.threadFeatures
    threadInfo = threadFeats.threadData.item(0)  # Default thread
    threadInput = threadFeats.createInput(cyl_face, threadInfo, is_modelled)
    threadFeats.add(threadInput)
    return f"Thread created on {body_name}"


def draft_faces(args):
    body_name = args["body_name"]
    angle_deg = args.get("angle_deg", 5)
    pull_plane = args.get("pull_plane", "XY")

    body = _find_body(body_name)
    rootComp = _get_root()

    # Find side faces
    side_faces = []
    for i in range(body.faces.count):
        face = body.faces.item(i)
        normal = face.geometry.normal
        if pull_plane == "XY" and abs(normal.z) < 0.1:
            side_faces.append(face)
        elif pull_plane == "XZ" and abs(normal.y) < 0.1:
            side_faces.append(face)
        elif pull_plane == "YZ" and abs(normal.x) < 0.1:
            side_faces.append(face)

    if not side_faces:
        raise ValueError(f"No side faces found for pull plane {pull_plane}")

    pull_map = {"XY": rootComp.xYConstructionPlane, "XZ": rootComp.xZConstructionPlane, "YZ": rootComp.yZConstructionPlane}
    pull_direction = pull_map[pull_plane]

    angle = adsk.core.ValueInput.createByString(f"{angle_deg} deg")
    draftFeats = rootComp.features.draftFeatures
    draftInput = draftFeats.createInput(side_faces, pull_direction)
    draftInput.setSingleAngle(True, angle)
    draftFeats.add(draftInput)
    return f"Draft applied: {angle_deg}deg on {body_name}"


def combine_bodies(args):
    target_name = args["target_body"]
    tool_name = args["tool_body"]
    operation = args.get("operation", "join")

    target = _find_body(target_name)
    tool = _find_body(tool_name)
    rootComp = _get_root()

    op_map = {
        "join": adsk.fusion.FeatureOperations.JoinFeatureOperation,
        "cut": adsk.fusion.FeatureOperations.CutFeatureOperation,
        "intersect": adsk.fusion.FeatureOperations.IntersectFeatureOperation,
    }
    op = op_map.get(operation, adsk.fusion.FeatureOperations.JoinFeatureOperation)

    toolBodies = adsk.core.ObjectCollection.create()
    toolBodies.add(tool)

    combineFeats = rootComp.features.combineFeatures
    combineInput = combineFeats.createInput(target, toolBodies)
    combineInput.operation = op
    combineFeats.add(combineInput)
    return f"Combined {target_name} {operation} {tool_name}"


def split_body(args):
    body_name = args["body_name"]
    plane = args.get("plane", "XY")
    offset = args.get("offset", 0) * MM_TO_CM

    body = _find_body(body_name)
    rootComp = _get_root()

    plane_map = {"XY": rootComp.xYConstructionPlane, "XZ": rootComp.xZConstructionPlane, "YZ": rootComp.yZConstructionPlane}
    base_plane = plane_map[plane]

    if offset != 0:
        planes = rootComp.constructionPlanes
        planeInput = planes.createInput()
        planeInput.setByOffset(base_plane, adsk.core.ValueInput.createByReal(offset))
        split_plane = planes.add(planeInput)
    else:
        split_plane = base_plane

    splitFeats = rootComp.features.splitBodyFeatures
    splitInput = splitFeats.createInput(body, split_plane, True)
    splitFeats.add(splitInput)
    return f"Split {body_name} on {plane} plane (offset={args.get('offset', 0)}mm)"


def move_body(args):
    body_name = args["body_name"]
    dx = args.get("dx", 0) * MM_TO_CM
    dy = args.get("dy", 0) * MM_TO_CM
    dz = args.get("dz", 0) * MM_TO_CM

    body = _find_body(body_name)
    rootComp = _get_root()

    matrix = adsk.core.Matrix3D.create()
    matrix.translation = adsk.core.Vector3D.create(dx, dy, dz)

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)

    moveFeats = rootComp.features.moveFeatures
    moveInput = moveFeats.createInput(bodies, matrix)
    moveFeats.add(moveInput)
    return f"Moved {body_name} by ({args.get('dx', 0)}, {args.get('dy', 0)}, {args.get('dz', 0)})mm"


def delete_face(args):
    body_name = args["body_name"]
    face_index = args.get("face_index", 0)

    body = _find_body(body_name)
    rootComp = _get_root()

    face = body.faces.item(face_index)
    delFeats = rootComp.features.surfaceDeleteFaceFeatures
    delFeats.add(face)
    return f"Deleted face {face_index} from {body_name}"
