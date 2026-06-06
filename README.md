# Muye Fusion Gateway

> A lightweight MCP Gateway that bridges AI clients to **Fusion 360** via [FusionMCP](https://github.com/fozzfut/FusionMCP).
>
> **35 hand-crafted domain tools + `execute_python` universal passthrough.**
> Quality over quantity — every tool is tested and reliable.

## Why this exists

FusionMCP (fozzfut) runs inside Fusion 360 as an Add-in and exposes 170+ commands via a custom HTTP JSON protocol (port 7432). However, it does **not** speak the standard MCP protocol that AI clients (WorkBuddy, Claude Desktop, Cursor) expect.

**Muye Fusion Gateway translates between the two protocols:**

```
AI Client (WorkBuddy / Claude / Cursor)
    │
    │  Standard MCP Protocol (Streamable HTTP)
    ▼
┌──────────────────────────────┐
│   Muye Fusion Gateway (:8000)│  ← This project
│                              │
│  ┌─ 35 domain tools ────────┤│  Hand-crafted, tested
│  │ create_cube, extrude, ... │
│  │ fillet, hole, export ...  │
│  ├─ execute_python ─────────┤│  Universal fallback
│  │ (any adsk API code)      │
│  └──────────────────────────┘│
│         │                    │
│     bridge.py               ││  Protocol translator
│         │                    │
└─────────┼────────────────────┘
          │  Custom HTTP JSON (:7432)
          ▼
   FusionMCP Add-in (inside Fusion 360)
          │
          ▼
     Fusion 360 API (adsk.core / adsk.fusion)
```

## Architecture

| Layer | Technology | Port | Protocol |
|-------|-----------|------|----------|
| AI Client | WorkBuddy, Claude Desktop, etc | — | MCP Streamable HTTP |
| **Gateway** | Python / FastMCP | **8000** | MCP → HTTP JSON translator |
| Backend | fozzfut/FusionMCP Add-in | **7432** | Custom HTTP POST JSON |
| Engine | Autodesk Fusion 360 | — | adsk.core / adsk.fusion |

## Tools (35 total)

### Basic Shapes (6)
| Tool | Description |
|------|-------------|
| `create_cube` | Parametric cube at origin |
| `create_cylinder` | Cylinder at origin |
| `create_sphere` | Sphere at origin |
| `create_cone` | Cone at origin |
| `create_torus` | Torus at origin |
| `create_loft` | Loft between two profiles |

### Features (10)
| Tool | Description |
|------|-------------|
| `fillet_edge` | Constant radius fillet |
| `chamfer_edge` | Equal distance chamfer |
| `create_hole` | Simple through-hole |
| `create_shell` | Shell with face removal |
| `create_thread` | Thread feature on cylinder |
| `draft_faces` | Draft angle on side faces |
| `combine_bodies` | Join/cut/intersect bodies |
| `split_body` | Split body with plane |
| `move_body` | Move body by translation |
| `delete_face` | Delete face (solid→surface) |

### Transforms (4)
| Tool | Description |
|------|-------------|
| `rotate_body` | Rotate body around axis |
| `mirror_bodies` | Mirror across construction plane |
| `circular_pattern` | Circular pattern around Z axis |
| `rectangular_pattern` | Rectangular pattern grid |

### Surfaces (6)
| Tool | Description |
|------|-------------|
| `create_sweep` | Sweep tube along path |
| `patch_surface` | Patch from profile boundary |
| `offset_surface` | Offset face by distance |
| `thicken_surface` | Thicken surface→solid |
| `stitch_surface` | Stitch surfaces together |
| `trim_surface` | Trim surface with plane |

### Assembly (3)
| Tool | Description |
|------|-------------|
| `create_component` | New component in assembly |
| `joint_revolve` | Revolute (hinge) joint |
| `create_contact_set` | Contact set between occurrences |

### Export (4)
| Tool | Description |
|------|-------------|
| `export_step` | Export to STEP file |
| `export_stl` | Export to STL file |
| `export_iges` | Export to IGES file |
| `mass_properties` | Get mass/volume/area/density |

### Passthrough (2)
| Tool | Description |
|------|-------------|
| `execute_python` | **Run any Fusion 360 Python code** (universal tool) |
| `capture_viewport` | Screenshot of current viewport |

## Quick Start

### Prerequisites

1. **Fusion 360** installed and running
2. **[FusionMCP](https://github.com/fozzfut/FusionMCP)** Add-in installed in Fusion 360
3. **Python 3.13+** (Homebrew recommended, not managed/workbuddy Python)

### Install & Run

```bash
# Clone and setup
cd fusion360-mcp-codebook
python3 -m venv server/.venv
source server/.venv/bin/activate
pip install mcp fastmcp pydantic

# Start the Gateway
./start.sh
# Server runs on http://127.0.0.1:8000/mcp
```

### Configure MCP Client

```json
{
  "mcpServers": {
    "fusion": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

## Key Design Decisions

### Why 35 tools, not 170+?

We started by auto-generating MCP wrappers for all 170 FusionMCP commands. This gave us impressive numbers but poor quality:

- **Variable name mismatches**: Auto-generated tools had bugs like undefined variables (`combine_bodies`)
- **Poor descriptions**: Generic "Execute FusionMCP command: X" doesn't help AI choose the right tool
- **Maintenance burden**: 170 tools × potential bugs = hard to keep reliable

**Our hybrid approach**: 35 carefully crafted tools for common operations + `execute_python` as a universal fallback. For anything not covered by a dedicated tool, the AI can write arbitrary Fusion 360 Python API code and run it via `execute_python`.

This gives us:
- ✅ **High-quality dedicated tools** for common operations (AI picks right every time)
- ✅ **Full API access** via `execute_python` (no functionality lost)
- ✅ **Easy maintenance** (35 tools vs 170)
- ✅ **Better AI experience** (smaller tool set = less confusion)

## Project Structure

```
fusion360-mcp-codebook/
├── start.sh                  # Launch script
├── README.md                 # This file
├── server/
│   ├── main.py               # Entry point
│   ├── app.py                # FastMCP singleton
│   ├── bridge.py             # FusionMCP HTTP client
│   ├── config.py             # Configuration
│   └── tools/
│       ├── basic_shapes.py   # create_cube, create_cylinder, ...
│       ├── features.py       # fillet_edge, chamfer_edge, hole, ...
│       ├── transforms.py     # move, rotate, mirror, pattern
│       ├── surfaces.py       # sweep, loft, offset, thicken, ...
│       ├── assembly.py       # component, joint, contact_set
│       ├── export.py         # STEP, STL, IGES export
│       └── passthrough.py    # execute_python, capture_viewport
└── docs/
    └── handoff-*.md          # Session handoff documents
```

## License

MIT License — free to use, modify, and distribute.
