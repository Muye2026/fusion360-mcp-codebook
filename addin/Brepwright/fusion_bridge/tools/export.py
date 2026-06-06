"""Export tools + Passthrough tools — direct Fusion API calls."""

import adsk.core
import adsk.fusion
import base64
import json
import math
import os

MM_TO_CM = 0.1


def _get_app():
    return adsk.core.Application.get()


def _get_design():
    return _get_app().activeProduct


def _get_root():
    return _get_design().rootComponent


def _find_body(body_name):
    rootComp = _get_root()
    for i in range(rootComp.bRepBodies.count):
        body = rootComp.bRepBodies.item(i)
        if body.name == body_name:
            return body
    raise ValueError(f'Body "{body_name}" not found')


# ─── Export tools ──────────────────────────────────────────────────────

def export_step(args):
    """Export a component to STEP format."""
    filepath = args["filepath"]
    component_name = args.get("component_name", "")

    rootComp = _get_root()
    comp = rootComp
    if component_name:
        for i in range(rootComp.occurrences.count):
            occ = rootComp.occurrences.item(i)
            if occ.component.name == component_name:
                comp = occ.component
                break

    design = _get_design()
    export_mgr = design.exportManager
    step_options = export_mgr.createSTEPExportOptions(filepath, comp)
    export_mgr.execute(step_options)
    return f"Exported STEP: {filepath}"


def export_stl(args):
    """Export a body to STL format."""
    filepath = args["filepath"]
    body_name = args.get("body_name", "")

    rootComp = _get_root()
    body = None
    if body_name:
        body = _find_body(body_name)
    elif rootComp.bRepBodies.count > 0:
        body = rootComp.bRepBodies.item(0)
    else:
        raise ValueError("No bodies found")

    design = _get_design()
    export_mgr = design.exportManager
    stl_options = export_mgr.createSTLExportOptions(body, filepath)
    export_mgr.execute(stl_options)
    return f"Exported STL: {filepath}"


def export_iges(args):
    """Export a component to IGES format."""
    filepath = args["filepath"]
    component_name = args.get("component_name", "")

    rootComp = _get_root()
    comp = rootComp
    if component_name:
        for i in range(rootComp.occurrences.count):
            occ = rootComp.occurrences.item(i)
            if occ.component.name == component_name:
                comp = occ.component
                break

    design = _get_design()
    export_mgr = design.exportManager
    iges_options = export_mgr.createIGESExportOptions(filepath, comp)
    export_mgr.execute(iges_options)
    return f"Exported IGES: {filepath}"


def mass_properties(args):
    """Get physical properties of a body."""
    body_name = args.get("body_name", "")

    rootComp = _get_root()
    body = None
    if body_name:
        body = _find_body(body_name)
    elif rootComp.bRepBodies.count > 0:
        body = rootComp.bRepBodies.item(0)
    else:
        raise ValueError("No bodies found")

    props = body.physicalProperties
    if not props:
        raise ValueError("Failed to get physical properties")

    center = props.centerOfMass
    return (
        f"Body: {body.name}\n"
        f"Mass: {props.mass:.4f} kg\n"
        f"Volume: {props.volume:.4f} cm3\n"
        f"Area: {props.area:.4f} cm2\n"
        f"Density: {props.density:.6f} kg/cm3\n"
        f"Center of Mass: ({center.x:.4f}, {center.y:.4f}, {center.z:.4f})"
    )


def capture_viewport(args):
    """Capture the current Fusion 360 viewport as a PNG image."""
    width = args.get("width", 800)
    height = args.get("height", 600)

    app = _get_app()
    viewport = app.activeViewport

    # Save screenshot to temp file
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        temp_path = f.name

    viewport.saveAsImageFile(temp_path, width, height)

    # Read and encode as base64
    with open(temp_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")

    os.unlink(temp_path)
    return f"Viewport captured ({width}x{height})\ndata:image/png;base64,{img_data}"


# ─── Passthrough tools ─────────────────────────────────────────────────

# Persistent Python sessions for execute_python
_python_sessions = {}


def execute_python(args):
    """Execute arbitrary Python code in the Fusion 360 session."""
    code = args["code"]
    session_id = args.get("session_id", "default")

    # Get or create session namespace
    if session_id not in _python_sessions:
        _python_sessions[session_id] = {}

    session_ns = _python_sessions[session_id]

    # Execute in a namespace with Fusion modules available
    import io
    import contextlib

    stdout_capture = io.StringIO()
    try:
        exec_globals = {
            "adsk": adsk,
            "app": _get_app(),
            "ui": _get_app().userInterface,
            "design": _get_design(),
            "root": _get_root(),
            "json": json,
            "math": math,
            **session_ns,
        }
        with contextlib.redirect_stdout(stdout_capture):
            exec(code, exec_globals)

        # Persist session variables
        builtins = {"adsk", "app", "ui", "design", "root", "json", "math"}
        for k, v in exec_globals.items():
            if not k.startswith("_") and k not in builtins:
                session_ns[k] = v

        output = stdout_capture.getvalue()
        return output if output else "Code executed successfully"
    except Exception as exc:
        import traceback
        return f"Error: {type(exc).__name__}: {exc}\n{traceback.format_exc()}"


def fetch_api_documentation(args):
    """Search live Fusion API metadata through runtime introspection."""
    search_term = args["search_term"].lower()
    category = args.get("category", "all")
    max_results = args.get("max_results", 3)

    results = []

    # Search in adsk.core and adsk.fusion
    for module_name, module in [("adsk.core", adsk.core), ("adsk.fusion", adsk.fusion)]:
        for attr_name in dir(module):
            if search_term in attr_name.lower():
                attr = getattr(module, attr_name, None)
                if attr is not None:
                    doc = getattr(attr, "__doc__", "") or ""
                    results.append({
                        "module": module_name,
                        "name": attr_name,
                        "type": type(attr).__name__,
                        "doc": doc[:200] if doc else "No documentation",
                    })
                    if len(results) >= max_results:
                        break
        if len(results) >= max_results:
            break

    if not results:
        return f"No results found for: {search_term}"

    text = f"API Documentation Search: '{args['search_term']}'\n\n"
    for i, r in enumerate(results, 1):
        text += f"{i}. {r['module']}.{r['name']} ({r['type']})\n"
        text += f"   {r['doc']}\n\n"
    return text


def fetch_design_guide(args):
    """Return Brepwright's compact Fusion design guide."""
    return """# Brepwright Fusion Design Guide

## Key API Patterns
- User-facing inputs are in millimeters; Fusion API distances are centimeters.
- Use `createInput()` plus setters plus `add()` for feature creation.
- Name bodies immediately after creation. Later tools resolve by name first.
- Use `ObjectCollection` for multi-entity operations.
- All direct `adsk.core` and `adsk.fusion` calls must run on Fusion's main thread.

## Common Pitfalls
- `addNewComponent(None)` fails. Use `Matrix3D.create()`.
- `JointGeometry.create()` does not exist. Use the supported `createByPoint()` pattern.
- `contactSets` is on `design`, not `rootComp`.
- Torus creation is sweep-based, not revolve-based.
- STL export expects a `BRepBody`, not a `Component`.

See `codebook/LIBRARY.md` and Autodesk Fusion API documentation for the full reference:
https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-0E0E4C30-5E95-4F66-9D6D-07E70F4B6F79
"""
