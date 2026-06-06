"""System and inspection tools for Brepwright."""

import json
import time

import adsk.core
import adsk.fusion


_START_TIME = time.time()


def _app():
    return adsk.core.Application.get()


def _design():
    return adsk.fusion.Design.cast(_app().activeProduct)


def _root():
    design = _design()
    if not design:
        raise ValueError("No active Fusion design. Create or open a design first.")
    return design.rootComponent


def ping(args):
    """Return a lightweight health response."""
    del args
    return json.dumps(
        {
            "pong": True,
            "server": "Brepwright",
            "uptime_seconds": round(time.time() - _START_TIME, 3),
        },
        ensure_ascii=False,
    )


def get_runtime_status(args):
    """Return runtime and active-document status."""
    del args
    app = _app()
    design = _design()
    status = {
        "server": "Brepwright",
        "fusion_version": getattr(app, "version", "unknown"),
        "has_active_design": bool(design),
        "uptime_seconds": round(time.time() - _START_TIME, 3),
    }
    if design:
        root = design.rootComponent
        status.update(
            {
                "root_component": root.name,
                "body_count": root.bRepBodies.count,
                "occurrence_count": root.occurrences.count,
                "sketch_count": root.sketches.count,
            }
        )
    return json.dumps(status, ensure_ascii=False, indent=2)


def get_active_design_info(args):
    """Return a concise summary of the active design."""
    del args
    root = _root()
    bodies = []
    for i in range(root.bRepBodies.count):
        body = root.bRepBodies.item(i)
        bbox = body.boundingBox
        bodies.append(
            {
                "index": i,
                "name": body.name,
                "is_solid": body.isSolid,
                "faces": body.faces.count,
                "edges": body.edges.count,
                "min_cm": [bbox.minPoint.x, bbox.minPoint.y, bbox.minPoint.z],
                "max_cm": [bbox.maxPoint.x, bbox.maxPoint.y, bbox.maxPoint.z],
            }
        )

    components = []
    design = _design()
    for i in range(design.allComponents.count):
        comp = design.allComponents.item(i)
        components.append(
            {
                "index": i,
                "name": comp.name,
                "bodies": comp.bRepBodies.count,
                "occurrences": comp.occurrences.count,
            }
        )

    return json.dumps(
        {
            "root_component": root.name,
            "body_count": root.bRepBodies.count,
            "component_count": design.allComponents.count,
            "bodies": bodies,
            "components": components,
        },
        ensure_ascii=False,
        indent=2,
    )
