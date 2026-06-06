# -*- coding: utf-8 -*-
"""Brepwright - Runtime initialization and cleanup."""

import traceback

import adsk.core

from .fusion_bridge.runtime import start as fusion_start, stop as fusion_stop


def run(context):
    """Initialize and start the MCP server."""
    del context
    try:
        print("[Brepwright] Starting...")
        if not fusion_start():
            print("[Brepwright] ERROR: Startup aborted")
            return
        print("[Brepwright] Started successfully")
    except Exception:
        print(f"[Brepwright] Failed to start:\n{traceback.format_exc()}")


def stop(context):
    """Stop the MCP server and clean up."""
    del context
    try:
        print("[Brepwright] Stopping...")
        fusion_stop()
        print("[Brepwright] Stopped")
    except Exception:
        print(f"[Brepwright] Error during shutdown:\n{traceback.format_exc()}")
