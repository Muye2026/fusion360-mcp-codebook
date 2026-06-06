# -*- coding: utf-8 -*-
"""
Brepwright - Add-in entry point.

Starts a standalone MCP server inside Autodesk Fusion 360 that exposes
validated CAD tools and workflow helpers for AI-driven product modeling.
"""


def run(context):
    """Entry point - Fusion calls this when the add-in starts."""
    try:
        from . import addon_runtime
        addon_runtime.run(context)
    except Exception as e:
        print(f"[Brepwright] Failed to start: {e}")
        import traceback
        traceback.print_exc()


def stop(context):
    """Shutdown - Fusion calls this when the add-in stops."""
    try:
        from . import addon_runtime
        addon_runtime.stop(context)
    except Exception as e:
        print(f"[Brepwright] Error during shutdown: {e}")
