"""Assembly MCP Tools — 3 domain-specific tools for assembly operations.

Each tool generates Python code based on tested codebook patterns,
and executes via FusionBridge.
"""

from pydantic import Field

from server.app import mcp
from server.bridge import bridge
from server import config


# ─── create_component ──────────────────────────────────────────────────

@mcp.tool()
async def create_component(
    name: str = Field(default="NewComponent", description="Name for the new component"),
) -> str:
    """Create a new component in the root assembly in Fusion 360.

    Uses addNewComponent(Matrix3D.create()) — requires Matrix3D, not None.
    """
    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

transform = adsk.core.Matrix3D.create()
occ = rootComp.occurrences.addNewComponent(transform)
newComp = occ.component
newComp.name = "{name}"
print(f"Created component: {name}")
'''
    return await bridge.execute_python(code)


# ─── joint_revolve ─────────────────────────────────────────────────────

@mcp.tool()
async def joint_revolve(
    occ1_index: int = Field(default=0, description="Index of first occurrence (0-based)"),
    occ2_index: int = Field(default=1, description="Index of second occurrence (0-based)"),
    axis_direction: str = Field(default="Z", description="Joint axis: 'X', 'Y', or 'Z'"),
) -> str:
    """Create a revolute (hinge) joint between two occurrences in Fusion 360.

    Uses JointGeometry.createByPoint(vertex) and setAsRevoluteJointMotion(JointDirections enum).
    Finds vertices near the origin in each body for the joint connection.
    """
    axis_map = {"X": "XAxisJointDirection", "Y": "YAxisJointDirection", "Z": "ZAxisJointDirection"}
    axis_enum = axis_map.get(axis_direction, "ZAxisJointDirection")

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

occ1 = rootComp.occurrences.item({occ1_index})
occ2 = rootComp.occurrences.item({occ2_index})
if not occ1 or not occ2:
    print("ERROR: Occurrence not found at specified indices")
else:
    comp1 = occ1.component
    comp2 = occ2.component
    body1 = comp1.bRepBodies.item(0)
    body2 = comp2.bRepBodies.item(0)

    v1 = None
    v2 = None
    for v in body1.vertices:
        p = v.geometry
        if abs(p.x) < 0.1 and abs(p.y) < 0.1 and abs(p.z) < 0.1:
            v1 = v
            break
    for v in body2.vertices:
        p = v.geometry
        if abs(p.x) < 0.1 and abs(p.y) < 0.1 and abs(p.z) < 0.1:
            v2 = v
            break

    if not v1 or not v2:
        print("ERROR: No vertices near origin found in bodies")
    else:
        jointGeom1 = adsk.fusion.JointGeometry.createByPoint(v1)
        jointGeom2 = adsk.fusion.JointGeometry.createByPoint(v2)
        joints = rootComp.joints
        jointInput = joints.createInput(jointGeom1, jointGeom2)
        jointInput.setAsRevoluteJointMotion(adsk.fusion.JointDirections.{axis_enum})
        joint = joints.add(jointInput)
        print(f"Revolute joint created: occ {occ1_index} + occ {occ2_index} around {axis_direction} axis")
'''
    return await bridge.execute_python(code)


# ─── create_contact_set ────────────────────────────────────────────────

@mcp.tool()
async def create_contact_set(
    entity_indices: list = Field(description="List of occurrence indices to include in contact set (0-based)"),
) -> str:
    """Create a contact set between occurrences in Fusion 360.

    Uses design.contactSets.add([occ1, occ2]) — on design, not rootComp; takes Python list, not ObjectCollection.
    """
    indices_str = str(entity_indices)

    code = f'''import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent

entities = []
for idx in {indices_str}:
    occ = rootComp.occurrences.item(idx)
    if occ:
        entities.append(occ)

if len(entities) < 2:
    print("ERROR: Need at least 2 occurrences for a contact set")
else:
    # ContactSets is on design, not rootComp; add() takes Python list
    contactSet = design.contactSets.add(entities)
    print(f"Contact set created with {len(entities)} occurrences")
'''
    return await bridge.execute_python(code)
