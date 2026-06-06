# -*- coding: utf-8 -*-
"""Fusion Codebook MCP - Runtime initialization and cleanup."""

import traceback

import adsk.core

from .fusion_bridge.runtime import start as fusion_start, stop as fusion_stop


def run(context):
    """Initialize and start the MCP server."""
    del context
    try:
        print("[FusionCodebookMCP] Starting...")
        if not fusion_start():
            print("[FusionCodebookMCP] ERROR: Startup aborted")
            return
        print("[FusionCodebookMCP] Started successfully")
    except Exception:
        print(f"[FusionCodebookMCP] Failed to start:\n{traceback.format_exc()}")


def stop(context):
    """Stop the MCP server and clean up."""
    del context
    try:
        print("[FusionCodebookMCP] Stopping...")
        fusion_stop()
        print("[FusionCodebookMCP] Stopped")
    except Exception:
        print(f"[FusionCodebookMCP] Error during shutdown:\n{traceback.format_exc()}")
