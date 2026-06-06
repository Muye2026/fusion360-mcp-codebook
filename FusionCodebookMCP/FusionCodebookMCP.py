# -*- coding: utf-8 -*-
"""
Fusion Codebook MCP - Add-in entry point.

Starts a standalone MCP server inside Autodesk Fusion 360 that exposes
34 domain-specific tools + 4 passthrough tools for AI-driven CAD.
"""


def run(context):
    """Entry point - Fusion calls this when the add-in starts."""
    try:
        from . import addon_runtime
        addon_runtime.run(context)
    except Exception as e:
        print(f"[FusionCodebookMCP] Failed to start: {e}")
        import traceback
        traceback.print_exc()


def stop(context):
    """Shutdown - Fusion calls this when the add-in stops."""
    try:
        from . import addon_runtime
        addon_runtime.stop(context)
    except Exception as e:
        print(f"[FusionCodebookMCP] Error during shutdown: {e}")
