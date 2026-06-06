"""Tool routing — maps tool names to handler functions."""

import traceback

from . import tool_surface
from .tools import (
    assembly,
    basic_shapes,
    export,
    features,
    surfaces,
    system,
    transforms,
    workflow,
)
from .dispatch import log


def _wrap(func):
    """Wrap a tool function to match the call_data format expected by the router."""
    def handler(call_data):
        params = call_data.get("params", {})
        tool_name = params.get("name", getattr(func, "__name__", "unknown_tool"))
        arguments = params.get("arguments", {})
        try:
            result = func(arguments)
            if isinstance(result, dict) and "content" in result:
                return result
            return {"content": [{"type": "text", "text": str(result)}], "isError": False}
        except Exception as exc:
            tb = traceback.format_exc()
            log(f"Tool error in {tool_name}: {exc}\n{tb}")
            return {
                "content": [{
                    "type": "text",
                    "text": (
                        f"Tool: {tool_name}\n"
                        f"Error: {type(exc).__name__}: {exc}\n"
                        "Suggested next action: verify required parameters, confirm an active Fusion design is open, "
                        "then retry with a smaller operation."
                    ),
                }],
                "isError": True,
            }
    return handler


# ─── Tool handler registry ─────────────────────────────────────────────

TOOL_HANDLERS = {
    # System
    tool_surface.PING: _wrap(system.ping),
    tool_surface.GET_RUNTIME_STATUS: _wrap(system.get_runtime_status),
    tool_surface.GET_ACTIVE_DESIGN_INFO: _wrap(system.get_active_design_info),

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

    # Workflow
    tool_surface.CREATE_MOUNTING_PLATE: _wrap(workflow.create_mounting_plate),
    tool_surface.CREATE_ENCLOSURE_SHELL: _wrap(workflow.create_enclosure_shell),
    tool_surface.CREATE_BRACKET: _wrap(workflow.create_bracket),
    tool_surface.INSPECT_DESIGN: _wrap(workflow.inspect_design),
    tool_surface.EXPORT_DESIGN_PACK: _wrap(workflow.export_design_pack),
    tool_surface.VALIDATE_PART_FOR_PRINTING: _wrap(workflow.validate_part_for_printing),
}

# Validate all tools have handlers
if set(TOOL_HANDLERS) != tool_surface._TOOL_NAMES:
    missing = tool_surface._TOOL_NAMES - set(TOOL_HANDLERS)
    extra = set(TOOL_HANDLERS) - tool_surface._TOOL_NAMES
    raise RuntimeError(f"Handler registry mismatch. Missing: {missing}, Extra: {extra}")
