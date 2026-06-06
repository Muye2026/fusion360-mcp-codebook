"""Workflow-first CAD tools that differentiate Brepwright from generic MCP servers."""

import json
import os

import adsk.core
import adsk.fusion

from . import basic_shapes, features, export

MM_TO_CM = 0.1


def _app():
    return adsk.core.Application.get()


def _design():
    design = adsk.fusion.Design.cast(_app().activeProduct)
    if not design:
        raise ValueError("No active Fusion design. Create or open a design first.")
    return design


def _root():
    return _design().rootComponent


def _find_body(body_name):
    root = _root()
    for i in range(root.bRepBodies.count):
        body = root.bRepBodies.item(i)
        if body.name == body_name:
            return body
    raise ValueError(f'Body "{body_name}" not found')


def _body_summary(body):
    bbox = body.boundingBox
    props = body.physicalProperties
    return {
        "name": body.name,
        "is_solid": body.isSolid,
        "faces": body.faces.count,
        "edges": body.edges.count,
        "bounding_box_cm": {
            "min": [bbox.minPoint.x, bbox.minPoint.y, bbox.minPoint.z],
            "max": [bbox.maxPoint.x, bbox.maxPoint.y, bbox.maxPoint.z],
        },
        "mass_kg": props.mass if props else None,
        "volume_cm3": props.volume if props else None,
        "area_cm2": props.area if props else None,
    }


def _create_cylinder_at(name, radius_mm, height_mm, x_mm, y_mm):
    root = _root()
    radius = radius_mm * MM_TO_CM
    height = height_mm * MM_TO_CM
    x = x_mm * MM_TO_CM
    y = y_mm * MM_TO_CM

    sketch = root.sketches.add(root.xYConstructionPlane)
    sketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(x, y, 0), radius
    )
    profile = sketch.profiles.item(0)
    ext_input = root.features.extrudeFeatures.createInput(
        profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(height))
    extrude = root.features.extrudeFeatures.add(ext_input)
    body = extrude.bodies.item(0)
    body.name = name
    return body


def create_mounting_plate(args):
    """Create a practical mounting plate with rounded edges and four holes."""
    width = args.get("width", 80)
    depth = args.get("depth", 50)
    thickness = args.get("thickness", 4)
    corner_radius = args.get("corner_radius", 2)
    hole_diameter = args.get("hole_diameter", 4)
    hole_offset_x = args.get("hole_offset_x", 10)
    hole_offset_y = args.get("hole_offset_y", 10)
    name = args.get("name", "MountingPlate")

    basic_shapes.create_cube(
        {"width": width, "height": depth, "depth": thickness, "name": name}
    )
    if corner_radius > 0:
        features.fillet_edge({"body_name": name, "radius": corner_radius, "edge_index": -1})

    holes = [
        (hole_offset_x, hole_offset_y),
        (width - hole_offset_x, hole_offset_y),
        (hole_offset_x, depth - hole_offset_y),
        (width - hole_offset_x, depth - hole_offset_y),
    ]
    for x, y in holes:
        features.create_hole(
            {
                "body_name": name,
                "radius": hole_diameter / 2,
                "depth": thickness + 1,
                "x": x,
                "y": y,
            }
        )

    return json.dumps(
        {
            "created": "mounting_plate",
            "body": name,
            "dimensions_mm": [width, depth, thickness],
            "hole_count": len(holes),
            "hole_diameter_mm": hole_diameter,
        },
        ensure_ascii=False,
    )


def create_enclosure_shell(args):
    """Create a box-like enclosure shell with optional screw posts."""
    width = args.get("width", 80)
    depth = args.get("depth", 50)
    height = args.get("height", 25)
    wall_thickness = args.get("wall_thickness", 2)
    corner_radius = args.get("corner_radius", 1.5)
    post_diameter = args.get("post_diameter", 6)
    post_hole_diameter = args.get("post_hole_diameter", 2.5)
    add_posts = args.get("add_posts", True)
    name = args.get("name", "EnclosureShell")

    basic_shapes.create_cube(
        {"width": width, "height": depth, "depth": height, "name": name}
    )
    if corner_radius > 0:
        features.fillet_edge({"body_name": name, "radius": corner_radius, "edge_index": -1})
    features.create_shell(
        {"body_name": name, "thickness": wall_thickness, "face_index": 0}
    )

    posts = []
    if add_posts:
        offset = max(post_diameter, wall_thickness * 3)
        positions = [
            (offset, offset),
            (width - offset, offset),
            (offset, depth - offset),
            (width - offset, depth - offset),
        ]
        for idx, (x, y) in enumerate(positions, 1):
            post_name = f"{name}_Post{idx}"
            _create_cylinder_at(post_name, post_diameter / 2, height - wall_thickness, x, y)
            posts.append(post_name)
            if post_hole_diameter > 0:
                features.create_hole(
                    {
                        "body_name": post_name,
                        "radius": post_hole_diameter / 2,
                        "depth": height,
                        "x": x,
                        "y": y,
                    }
                )

    return json.dumps(
        {
            "created": "enclosure_shell",
            "body": name,
            "dimensions_mm": [width, depth, height],
            "wall_thickness_mm": wall_thickness,
            "posts": posts,
        },
        ensure_ascii=False,
    )


def create_bracket(args):
    """Create a simple L or U bracket as named bodies with optional mounting holes."""
    bracket_type = args.get("type", "L").upper()
    width = args.get("width", 60)
    depth = args.get("depth", 40)
    height = args.get("height", 40)
    thickness = args.get("thickness", 4)
    hole_diameter = args.get("hole_diameter", 4)
    name = args.get("name", "Bracket")

    base_name = f"{name}_Base"
    wall_name = f"{name}_Wall"
    basic_shapes.create_cube(
        {"width": width, "height": depth, "depth": thickness, "name": base_name}
    )
    basic_shapes.create_cube(
        {"width": width, "height": thickness, "depth": height, "name": wall_name}
    )

    created = [base_name, wall_name]
    if bracket_type == "U":
        wall2_name = f"{name}_Wall2"
        basic_shapes.create_cube(
            {"width": width, "height": thickness, "depth": height, "name": wall2_name}
        )
        features.move_body({"body_name": wall2_name, "dx": 0, "dy": depth - thickness, "dz": 0})
        created.append(wall2_name)

    features.create_hole(
        {
            "body_name": base_name,
            "radius": hole_diameter / 2,
            "depth": thickness + 1,
            "x": width * 0.25,
            "y": depth * 0.5,
        }
    )
    features.create_hole(
        {
            "body_name": base_name,
            "radius": hole_diameter / 2,
            "depth": thickness + 1,
            "x": width * 0.75,
            "y": depth * 0.5,
        }
    )

    return json.dumps(
        {
            "created": "bracket",
            "type": bracket_type,
            "bodies": created,
            "dimensions_mm": [width, depth, height],
        },
        ensure_ascii=False,
    )


def inspect_design(args):
    """Return body, component, and warning information for the active design."""
    del args
    root = _root()
    bodies = []
    warnings = []
    for i in range(root.bRepBodies.count):
        body = root.bRepBodies.item(i)
        summary = _body_summary(body)
        bodies.append(summary)
        if not body.isSolid:
            warnings.append(f"{body.name}: not a solid body")
        if summary["volume_cm3"] is not None and summary["volume_cm3"] <= 0:
            warnings.append(f"{body.name}: non-positive volume")

    return json.dumps(
        {
            "body_count": len(bodies),
            "bodies": bodies,
            "warnings": warnings,
        },
        ensure_ascii=False,
        indent=2,
    )


def export_design_pack(args):
    """Export STEP, STL, screenshot, and JSON summary into a folder."""
    output_dir = args.get("output_dir", os.path.expanduser("~/Desktop/brepwright-export"))
    base_name = args.get("base_name", "brepwright-design")
    body_name = args.get("body_name", "")
    os.makedirs(output_dir, exist_ok=True)

    step_path = os.path.join(output_dir, f"{base_name}.step")
    stl_path = os.path.join(output_dir, f"{base_name}.stl")
    png_path = os.path.join(output_dir, f"{base_name}.png")
    json_path = os.path.join(output_dir, f"{base_name}.summary.json")

    export.export_step({"filepath": step_path, "component_name": ""})
    export.export_stl({"filepath": stl_path, "body_name": body_name})
    _app().activeViewport.saveAsImageFile(png_path, 1600, 1000)

    summary = json.loads(inspect_design({}))
    summary["exports"] = {
        "step": step_path,
        "stl": stl_path,
        "screenshot": png_path,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return json.dumps(
        {
            "exported": True,
            "output_dir": output_dir,
            "files": {
                "step": step_path,
                "stl": stl_path,
                "screenshot": png_path,
                "summary": json_path,
            },
        },
        ensure_ascii=False,
        indent=2,
    )


def validate_part_for_printing(args):
    """Run lightweight checks that are useful before 3D printing handoff."""
    min_wall_thickness = args.get("min_wall_thickness", 1.2)
    root = _root()
    warnings = []
    solid_count = 0
    for i in range(root.bRepBodies.count):
        body = root.bRepBodies.item(i)
        if body.isSolid:
            solid_count += 1
        else:
            warnings.append(f"{body.name}: body is not solid")
        bbox = body.boundingBox
        dims_cm = [
            bbox.maxPoint.x - bbox.minPoint.x,
            bbox.maxPoint.y - bbox.minPoint.y,
            bbox.maxPoint.z - bbox.minPoint.z,
        ]
        if min(dims_cm) * 10 < min_wall_thickness:
            warnings.append(
                f"{body.name}: smallest bounding dimension is below {min_wall_thickness}mm"
            )

    return json.dumps(
        {
            "printability": "review" if warnings else "pass",
            "body_count": root.bRepBodies.count,
            "solid_body_count": solid_count,
            "warnings": warnings,
        },
        ensure_ascii=False,
        indent=2,
    )
