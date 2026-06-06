"""Tool routing — maps tool names to handler functions."""

import traceback

from . import tool_surface
from .tools import basic_shapes, features, transforms, surfaces, assembly, export
from .dispatch import log


def _wrap(func):
    """Wrap a tool function to match the call_data format expected by the router."""
    def handler(call_data):
        arguments = call_data.get("params", {}).get("arguments", {})
        try:
            result = func(arguments)
            if isinstance(result, dict) and "content" in result:
                return result
            return {"content": [{"type": "text", "text": str(result)}], "isError": False}
        except Exception as exc:
            tb = traceback.format_exc()
            log(f"Tool error: {exc}\n{tb}")
            return {
                "content": [{"type": "text", "text": f"Error: {type(exc).__name__}: {exc}"}],
                "isError": True,
            }
    return handler


# ─── Tool handler registry ─────────────────────────────────────────────

TOOL_HANDLERS = {
    # Basic Shapes
    tool_surface.CREATE_CUBE: _wrap(basic_shapes.create_cube),
    tool_surface.CREATE_CYLINDER: _wrap(basic_shapes.create_cylinder),
    tool_surface.CREATE_SPHERE: _wrap(basic_shapes.create_sphere),
    tool_surface.CREATE_CONE: _wrap(basic_shapes.create_cone),
    tool_surface.CREATE_TORUS: _wrap(basic_shapes.create_torus),
    tool_surface.CREATE_LOFT: _wrap(basic_shapes.create_loft),

    # Features
    tool_surface.FILLET_EDGE: _wrap(features.fillet_edge),
    tool_surface.CHAMFER_EDGE: _wrap(features.chamfer_edge),
    tool_surface.CREATE_HOLE: _wrap(features.create_hole),
    tool_surface.CREATE_SHELL: _wrap(features.create_shell),
    tool_surface.CREATE_THREAD: _wrap(features.create_thread),
    tool_surface.DRAFT_FACES: _wrap(features.draft_faces),
    tool_surface.COMBINE_BODIES: _wrap(features.combine_bodies),
    tool_surface.SPLIT_BODY: _wrap(features.split_body),
    tool_surface.MOVE_BODY: _wrap(features.move_body),
    tool_surface.DELETE_FACE: _wrap(features.delete_face),

    # Transforms
    tool_surface.CIRCULAR_PATTERN: _wrap(transforms.circular_pattern),
    tool_surface.RECTANGULAR_PATTERN: _wrap(transforms.rectangular_pattern),
    tool_surface.MIRROR_BODIES: _wrap(transforms.mirror_bodies),
    tool_surface.ROTATE_BODY: _wrap(transforms.rotate_body),

    # Surfaces
    tool_surface.CREATE_SWEEP: _wrap(surfaces.create_sweep),
    tool_surface.PATCH_SURFACE: _wrap(surfaces.patch_surface),
    tool_surface.OFFSET_SURFACE: _wrap(surfaces.offset_surface),
    tool_surface.THICKEN_SURFACE: _wrap(surfaces.thicken_surface),
    tool_surface.STITCH_SURFACE: _wrap(surfaces.stitch_surface),
    tool_surface.TRIM_SURFACE: _wrap(surfaces.trim_surface),

    # Assembly
    tool_surface.CREATE_COMPONENT: _wrap(assembly.create_component),
    tool_surface.JOINT_REVOLVE: _wrap(assembly.joint_revolve),
    tool_surface.CREATE_CONTACT_SET: _wrap(assembly.create_contact_set),

    # Export
    tool_surface.EXPORT_STEP: _wrap(export.export_step),
    tool_surface.EXPORT_STL: _wrap(export.export_stl),
    tool_surface.EXPORT_IGES: _wrap(export.export_iges),
    tool_surface.MASS_PROPERTIES: _wrap(export.mass_properties),
    tool_surface.CAPTURE_VIEWPORT: _wrap(export.capture_viewport),

    # Passthrough
    tool_surface.EXECUTE_PYTHON: _wrap(export.execute_python),
    tool_surface.FETCH_API_DOCUMENTATION: _wrap(export.fetch_api_documentation),
    tool_surface.FETCH_DESIGN_GUIDE: _wrap(export.fetch_design_guide),
}

# Validate all tools have handlers
if set(TOOL_HANDLERS) != tool_surface._TOOL_NAMES:
    missing = tool_surface._TOOL_NAMES - set(TOOL_HANDLERS)
    extra = set(TOOL_HANDLERS) - tool_surface._TOOL_NAMES
    raise RuntimeError(f"Handler registry mismatch. Missing: {missing}, Extra: {extra}")
