"""Assembly tools — direct Fusion API calls."""

import adsk.core
import adsk.fusion


def _get_design():
    app = adsk.core.Application.get()
    return app.activeProduct


def _get_root():
    return _get_design().rootComponent


def _find_occurrence(name):
    """Find an occurrence by name."""
    rootComp = _get_root()
    for i in range(rootComp.occurrences.count):
        occ = rootComp.occurrences.item(i)
        if occ.component.name == name or occ.name == name:
            return occ
    raise ValueError(f'Occurrence "{name}" not found')


def _find_body(body_name):
    rootComp = _get_root()
    for i in range(rootComp.bRepBodies.count):
        body = rootComp.bRepBodies.item(i)
        if body.name == body_name:
            return body
    raise ValueError(f'Body "{body_name}" not found')


def create_component(args):
    """Create a new component in the assembly."""
    name = args.get("name", "Component")

    rootComp = _get_root()
    occ = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = name
    return f"Created component: {name}"


def joint_revolve(args):
    """Create a revolute joint between two components."""
    comp1_name = args["component1_name"]
    comp2_name = args["component2_name"]
    joint_axis = args.get("joint_axis", "Z")

    rootComp = _get_root()
    occ1 = _find_occurrence(comp1_name)
    occ2 = _find_occurrence(comp2_name)

    # Find a vertex on each component for joint geometry
    vertex1 = occ1.component.bRepBodies.item(0).vertices.item(0)
    vertex2 = occ2.component.bRepBodies.item(0).vertices.item(0)

    geo = adsk.fusion.JointGeometry.createByPoint(vertex1)

    axis_map = {
        "X": adsk.fusion.JointDirections.XAxisJointDirection,
        "Y": adsk.fusion.JointDirections.YAxisJointDirection,
        "Z": adsk.fusion.JointDirections.ZAxisJointDirection,
    }
    joint_dir = axis_map.get(joint_axis, adsk.fusion.JointDirections.ZAxisJointDirection)

    joints = rootComp.joints
    jointInput = joints.createInput(occ2, geo)
    jointInput.setAsRevoluteJointMotion(joint_dir)
    joints.add(jointInput)
    return f"Created revolute joint: {comp1_name} <-> {comp2_name} ({joint_axis} axis)"


def create_contact_set(args):
    """Create a contact set between two occurrences."""
    occ1_name = args["occurrence1_name"]
    occ2_name = args["occurrence2_name"]

    design = _get_design()
    occ1 = _find_occurrence(occ1_name)
    occ2 = _find_occurrence(occ2_name)

    design.contactSets.add([occ1, occ2])
    return f"Created contact set: {occ1_name} <-> {occ2_name}"
