"""Fusion bridge server assembly and startup/shutdown wiring."""

import traceback

import adsk.core

from .. import settings
from ..lib import mcp_server as mcp_server_module
from . import tool_surface, operations
from .dispatch import (
    dispatch_to_main_thread,
    drain_logs,
    get_shutdown_flag,
    init_main_thread_dispatch,
    log,
    set_tool_handler,
    stop_main_thread_dispatch,
)


_server = None


def create_server():
    """Create and configure the MCP server with all tools."""

    def handle_any_tool(call_data):
        """Route to the correct handler based on tool name in call_data."""
        tool_name = call_data.get("params", {}).get("name", "")
        handler = operations.TOOL_HANDLERS.get(tool_name)
        if handler is None:
            return {
                "content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}],
                "isError": True,
            }
        return handler(call_data)

    set_tool_handler(handle_any_tool)

    server = mcp_server_module.MCPServer(
        port=settings.MCP_SERVER_PORT,
        tools=tool_surface.TOOL_DEFINITIONS,
        tool_handlers={
            name: dispatch_to_main_thread for name in operations.TOOL_HANDLERS
        },
        log_callback=log,
    )

    # Update server info
    from ..lib.mcp_server import SERVER_INFO
    SERVER_INFO["name"] = "brepwright"
    SERVER_INFO["version"] = "0.1.0"

    return server


def _start_server():
    global _server

    if _server and _server.is_running:
        log("MCP server already running")
        return True

    log(f"Starting MCP server on port {settings.MCP_SERVER_PORT}...")
    attempt = 0
    shutdown_flag = get_shutdown_flag()
    while not shutdown_flag.is_set():
        try:
            _server = create_server()
            _server.start()
            break
        except OSError as exc:
            if "Address already use" not in str(exc) and "Address already in use" not in str(exc):
                raise
            attempt += 1
            delay = 2 if attempt <= 60 else min(2 ** (attempt - 60), 60)
            log(f"Port {settings.MCP_SERVER_PORT} busy, retrying in {delay}s (attempt {attempt})...")
            shutdown_flag.wait(delay)
    else:
        log("MCP server start aborted (add-in stopping)")
        return False

    log(f"[OK] Brepwright server running at http://127.0.0.1:{settings.MCP_SERVER_PORT}/mcp")
    log(f"  Tools: {len(tool_surface.TOOL_DEFINITIONS)}")
    return True


def start():
    """Initialize dispatch system and start MCP server."""
    log("Brepwright starting...")

    try:
        init_main_thread_dispatch()
    except Exception as exc:
        log(f"ERROR: Failed to initialize main-thread dispatch: {exc}", adsk.core.LogLevels.ErrorLogLevel)
        log(traceback.format_exc(), adsk.core.LogLevels.ErrorLogLevel)
        return False

    if settings.MCP_AUTO_CONNECT:
        try:
            if not _start_server():
                stop_main_thread_dispatch()
                return False
            log("Brepwright started successfully")
        except Exception as exc:
            log(f"ERROR: Failed to start MCP server: {exc}", adsk.core.LogLevels.ErrorLogLevel)
            log(traceback.format_exc(), adsk.core.LogLevels.ErrorLogLevel)
            stop_main_thread_dispatch()
            return False
    else:
        log("MCP_AUTO_CONNECT is False - MCP server disabled")

    drain_logs()
    return True


def stop():
    """Stop MCP server and clean up dispatch system."""
    global _server

    log("Brepwright stopping...")
    stop_main_thread_dispatch()

    if _server:
        _server.stop()
        _server = None

    log("Brepwright stopped")
    drain_logs()
