"""Central definitions for all MCP tools — 34 domain tools + 4 passthrough tools."""

# ─── Tool name constants ──────────────────────────────────────────────

# Basic Shapes (6)
CREATE_CUBE = "create_cube"
CREATE_CYLINDER = "create_cylinder"
CREATE_SPHERE = "create_sphere"
CREATE_CONE = "create_cone"
CREATE_TORUS = "create_torus"
CREATE_LOFT = "create_loft"

# Features (10)
FILLET_EDGE = "fillet_edge"
CHAMFER_EDGE = "chamfer_edge"
CREATE_HOLE = "create_hole"
CREATE_SHELL = "create_shell"
CREATE_THREAD = "create_thread"
DRAFT_FACES = "draft_faces"
COMBINE_BODIES = "combine_bodies"
SPLIT_BODY = "split_body"
MOVE_BODY = "move_body"
DELETE_FACE = "delete_face"

# Transforms (4)
CIRCULAR_PATTERN = "circular_pattern"
RECTANGULAR_PATTERN = "rectangular_pattern"
MIRROR_BODIES = "mirror_bodies"
ROTATE_BODY = "rotate_body"

# Surfaces (6)
CREATE_SWEEP = "create_sweep"
PATCH_SURFACE = "patch_surface"
OFFSET_SURFACE = "offset_surface"
THICKEN_SURFACE = "thicken_surface"
STITCH_SURFACE = "stitch_surface"
TRIM_SURFACE = "trim_surface"

# Assembly (3)
CREATE_COMPONENT = "create_component"
JOINT_REVOLVE = "joint_revolve"
CREATE_CONTACT_SET = "create_contact_set"

# Export (5)
EXPORT_STEP = "export_step"
EXPORT_STL = "export_stl"
EXPORT_IGES = "export_iges"
MASS_PROPERTIES = "mass_properties"
CAPTURE_VIEWPORT = "capture_viewport"

# Passthrough (3)
EXECUTE_PYTHON = "execute_python"
FETCH_API_DOCUMENTATION = "fetch_api_documentation"
FETCH_DESIGN_GUIDE = "fetch_design_guide"


# ─── Tool definitions (JSON Schema) ────────────────────────────────────

TOOL_DEFINITIONS = [
    # === Basic Shapes ===
    {
        "name": CREATE_CUBE,
        "description": "Create a parametric cube at the origin in Fusion 360. Creates an extruded rectangle on the XY plane. All dimensions in millimeters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "width": {"type": "number", "description": "Width in mm (default: 10)", "default": 10},
                "height": {"type": "number", "description": "Height in mm (default: 10)", "default": 10},
                "depth": {"type": "number", "description": "Depth in mm (default: 10)", "default": 10},
                "name": {"type": "string", "description": "Body name (default: Cube)", "default": "Cube"},
            },
        },
    },
    {
        "name": CREATE_CYLINDER,
        "description": "Create a parametric cylinder at the origin. Creates a circle on XY plane and extrudes upward. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "radius": {"type": "number", "description": "Radius in mm (default: 5)", "default": 5},
                "height": {"type": "number", "description": "Height in mm (default: 20)", "default": 20},
                "name": {"type": "string", "description": "Body name (default: Cylinder)", "default": "Cylinder"},
            },
        },
    },
    {
        "name": CREATE_SPHERE,
        "description": "Create a sphere at the origin by revolving a semi-circle 360 degrees. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "radius": {"type": "number", "description": "Radius in mm (default: 5)", "default": 5},
                "name": {"type": "string", "description": "Body name (default: Sphere)", "default": "Sphere"},
            },
        },
    },
    {
        "name": CREATE_CONE,
        "description": "Create a parametric cone at the origin by revolving a triangle 360 degrees. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "radius": {"type": "number", "description": "Base radius in mm (default: 5)", "default": 5},
                "height": {"type": "number", "description": "Height in mm (default: 10)", "default": 10},
                "name": {"type": "string", "description": "Body name (default: Cone)", "default": "Cone"},
            },
        },
    },
    {
        "name": CREATE_TORUS,
        "description": "Create a torus at the origin by sweeping a circular profile along a circular path. IMPORTANT: Uses SweepFeatures (not RevolveFeatures). All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "major_radius": {"type": "number", "description": "Distance from center to tube center in mm (default: 10)", "default": 10},
                "minor_radius": {"type": "number", "description": "Tube radius in mm (default: 3)", "default": 3},
                "name": {"type": "string", "description": "Body name (default: Torus)", "default": "Torus"},
            },
        },
    },
    {
        "name": CREATE_LOFT,
        "description": "Create a loft feature between two circular profiles on offset planes. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "radius1": {"type": "number", "description": "Bottom circle radius in mm (default: 3)", "default": 3},
                "radius2": {"type": "number", "description": "Top circle radius in mm (default: 1.5)", "default": 1.5},
                "height": {"type": "number", "description": "Distance between profiles in mm (default: 5)", "default": 5},
                "name": {"type": "string", "description": "Body name (default: Loft)", "default": "Loft"},
            },
        },
    },

    # === Features ===
    {
        "name": FILLET_EDGE,
        "description": "Apply constant radius fillet to edges of a body. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the target body"},
                "radius": {"type": "number", "description": "Fillet radius in mm (default: 1)", "default": 1},
                "edge_index": {"type": "integer", "description": "Edge index (-1 for all edges, default: -1)", "default": -1},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": CHAMFER_EDGE,
        "description": "Apply equal distance chamfer to edges of a body. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the target body"},
                "distance": {"type": "number", "description": "Chamfer distance in mm (default: 1)", "default": 1},
                "edge_index": {"type": "integer", "description": "Edge index (-1 for all edges, default: -1)", "default": -1},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": CREATE_HOLE,
        "description": "Create a simple hole on a face of a body. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the target body"},
                "radius": {"type": "number", "description": "Hole radius in mm (default: 1)", "default": 1},
                "depth": {"type": "number", "description": "Hole depth in mm (default: 5)", "default": 5},
                "x": {"type": "number", "description": "X position on face in mm (default: center)", "default": 0},
                "y": {"type": "number", "description": "Y position on face in mm (default: center)", "default": 0},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": CREATE_SHELL,
        "description": "Create a shell feature by removing a face and hollowing the body. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the target body"},
                "thickness": {"type": "number", "description": "Shell wall thickness in mm (default: 1)", "default": 1},
                "face_index": {"type": "integer", "description": "Index of face to remove (default: 0 = top face)", "default": 0},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": CREATE_THREAD,
        "description": "Create an external thread on a cylindrical face of a body.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the target body"},
                "thread_size": {"type": "string", "description": "Thread size designation (default: M20x2.5)", "default": "M20x2.5"},
                "is_modelled": {"type": "boolean", "description": "If true, model the thread geometry (default: true)", "default": True},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": DRAFT_FACES,
        "description": "Apply draft angle to side faces of a body.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the target body"},
                "angle_deg": {"type": "number", "description": "Draft angle in degrees (default: 5)", "default": 5},
                "pull_plane": {"type": "string", "description": "Pull direction plane: XY, XZ, or YZ (default: XY)", "default": "XY"},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": COMBINE_BODIES,
        "description": "Combine two bodies using join, cut, or intersect operation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target_body": {"type": "string", "description": "Name of the target body"},
                "tool_body": {"type": "string", "description": "Name of the tool body"},
                "operation": {"type": "string", "description": "Operation: join, cut, or intersect (default: join)", "default": "join"},
            },
            "required": ["target_body", "tool_body"],
        },
    },
    {
        "name": SPLIT_BODY,
        "description": "Split a body using a construction plane.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the body to split"},
                "plane": {"type": "string", "description": "Splitting plane: XY, XZ, or YZ (default: XY)", "default": "XY"},
                "offset": {"type": "number", "description": "Plane offset in mm (default: 0)", "default": 0},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": MOVE_BODY,
        "description": "Move a body by translation vector. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the body to move"},
                "dx": {"type": "number", "description": "X translation in mm (default: 0)", "default": 0},
                "dy": {"type": "number", "description": "Y translation in mm (default: 0)", "default": 0},
                "dz": {"type": "number", "description": "Z translation in mm (default: 0)", "default": 0},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": DELETE_FACE,
        "description": "Delete a face from a body (converts solid to open surface).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the target body"},
                "face_index": {"type": "integer", "description": "Index of face to delete (default: 0)", "default": 0},
            },
            "required": ["body_name"],
        },
    },

    # === Transforms ===
    {
        "name": CIRCULAR_PATTERN,
        "description": "Create a circular pattern of a body around an axis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the body to pattern"},
                "count": {"type": "integer", "description": "Number of instances (default: 4)", "default": 4},
                "angle_deg": {"type": "number", "description": "Total angle in degrees (default: 360)", "default": 360},
                "axis": {"type": "string", "description": "Rotation axis: X, Y, or Z (default: Z)", "default": "Z"},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": RECTANGULAR_PATTERN,
        "description": "Create a rectangular pattern of a body. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the body to pattern"},
                "count_x": {"type": "integer", "description": "Number of instances in X (default: 2)", "default": 2},
                "count_y": {"type": "integer", "description": "Number of instances in Y (default: 2)", "default": 2},
                "spacing_x": {"type": "number", "description": "X spacing in mm (default: 20)", "default": 20},
                "spacing_y": {"type": "number", "description": "Y spacing in mm (default: 20)", "default": 20},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": MIRROR_BODIES,
        "description": "Mirror a body across a construction plane.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the body to mirror"},
                "plane": {"type": "string", "description": "Mirror plane: XY, XZ, or YZ (default: YZ)", "default": "YZ"},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": ROTATE_BODY,
        "description": "Rotate a body around an axis by a given angle.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the body to rotate"},
                "angle_deg": {"type": "number", "description": "Rotation angle in degrees (default: 45)", "default": 45},
                "axis": {"type": "string", "description": "Rotation axis: X, Y, or Z (default: Z)", "default": "Z"},
            },
            "required": ["body_name"],
        },
    },

    # === Surfaces ===
    {
        "name": CREATE_SWEEP,
        "description": "Create a sweep feature by sweeping a circular profile along a straight path. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "profile_radius": {"type": "number", "description": "Cross-section radius in mm (default: 5)", "default": 5},
                "path_length": {"type": "number", "description": "Sweep path length in mm (default: 100)", "default": 100},
                "name": {"type": "string", "description": "Body name (default: SweepTube)", "default": "SweepTube"},
            },
        },
    },
    {
        "name": PATCH_SURFACE,
        "description": "Create a patch surface from a sketch profile.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "radius": {"type": "number", "description": "Profile radius in mm (default: 5)", "default": 5},
                "name": {"type": "string", "description": "Body name (default: Patch)", "default": "Patch"},
            },
        },
    },
    {
        "name": OFFSET_SURFACE,
        "description": "Create an offset surface from existing faces. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the source body"},
                "distance": {"type": "number", "description": "Offset distance in mm (default: 2)", "default": 2},
                "face_index": {"type": "integer", "description": "Face index to offset (default: 0)", "default": 0},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": THICKEN_SURFACE,
        "description": "Thicken a surface body to create a solid. All dimensions in mm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the surface body"},
                "thickness": {"type": "number", "description": "Thickness in mm (default: 2)", "default": 2},
                "symmetric": {"type": "boolean", "description": "Symmetric thickening (default: true)", "default": True},
            },
            "required": ["body_name"],
        },
    },
    {
        "name": STITCH_SURFACE,
        "description": "Stitch multiple surface bodies into one.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_names": {"type": "array", "items": {"type": "string"}, "description": "List of body names to stitch"},
                "tolerance": {"type": "number", "description": "Stitch tolerance in mm (default: 0.01)", "default": 0.01},
            },
            "required": ["body_names"],
        },
    },
    {
        "name": TRIM_SURFACE,
        "description": "Trim a surface body using a trimming tool (construction plane).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Name of the surface body to trim"},
                "trim_plane": {"type": "string", "description": "Trimming plane: XY, XZ, or YZ (default: XY)", "default": "XY"},
            },
            "required": ["body_name"],
        },
    },

    # === Assembly ===
    {
        "name": CREATE_COMPONENT,
        "description": "Create a new component in the assembly.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Component name (default: Component)", "default": "Component"},
            },
        },
    },
    {
        "name": JOINT_REVOLVE,
        "description": "Create a revolute joint between two components.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "component1_name": {"type": "string", "description": "Name of first component"},
                "component2_name": {"type": "string", "description": "Name of second component"},
                "joint_axis": {"type": "string", "description": "Joint axis: X, Y, or Z (default: Z)", "default": "Z"},
            },
            "required": ["component1_name", "component2_name"],
        },
    },
    {
        "name": CREATE_CONTACT_SET,
        "description": "Create a contact set between two occurrences.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "occurrence1_name": {"type": "string", "description": "Name of first occurrence"},
                "occurrence2_name": {"type": "string", "description": "Name of second occurrence"},
            },
            "required": ["occurrence1_name", "occurrence2_name"],
        },
    },

    # === Export ===
    {
        "name": EXPORT_STEP,
        "description": "Export a component to STEP format.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Output file path (.step)"},
                "component_name": {"type": "string", "description": "Component to export (default: root)", "default": ""},
            },
            "required": ["filepath"],
        },
    },
    {
        "name": EXPORT_STL,
        "description": "Export a body to STL format.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Output file path (.stl)"},
                "body_name": {"type": "string", "description": "Body to export (default: first body)", "default": ""},
            },
            "required": ["filepath"],
        },
    },
    {
        "name": EXPORT_IGES,
        "description": "Export a component to IGES format.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Output file path (.iges)"},
                "component_name": {"type": "string", "description": "Component to export (default: root)", "default": ""},
            },
            "required": ["filepath"],
        },
    },
    {
        "name": MASS_PROPERTIES,
        "description": "Get physical properties (mass, volume, area, density) of a body.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_name": {"type": "string", "description": "Body name (default: first body)", "default": ""},
            },
        },
    },
    {
        "name": CAPTURE_VIEWPORT,
        "description": "Capture the current Fusion 360 viewport as a PNG image.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "width": {"type": "integer", "description": "Image width in pixels (default: 800)", "default": 800},
                "height": {"type": "integer", "description": "Image height in pixels (default: 600)", "default": 600},
            },
        },
    },

    # === Passthrough ===
    {
        "name": EXECUTE_PYTHON,
        "description": "Execute arbitrary Python code in the live Fusion 360 session. Has full access to adsk.core and adsk.fusion. Use for operations not covered by domain-specific tools.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code to execute"},
                "session_id": {"type": "string", "description": "Session ID for persistent variables (default: 'default')", "default": "default"},
            },
            "required": ["code"],
        },
    },
    {
        "name": FETCH_API_DOCUMENTATION,
        "description": "Search live Fusion API metadata through runtime introspection. Returns class overviews, properties, and function signatures.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "search_term": {"type": "string", "description": "Search term (e.g. 'BRepBody', 'sketches')"},
                "category": {"type": "string", "description": "Search category: class_name, member_name, description, or all", "default": "all"},
                "max_results": {"type": "integer", "description": "Maximum results (default: 3)", "default": 3},
            },
            "required": ["search_term"],
        },
    },
    {
        "name": FETCH_DESIGN_GUIDE,
        "description": "Read the bundled Fusion design guide with workflow guidance, API patterns, naming rules, and modeling habits.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]

_TOOL_NAMES = {t["name"] for t in TOOL_DEFINITIONS}
