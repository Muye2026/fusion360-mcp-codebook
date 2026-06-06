# -*- coding: utf-8 -*-
"""Brepwright settings."""

import os

# Default 8766 avoids known conflicts with Autodesk official MCP (27182)
# and frankhommers/autodesk-fusion-mcp (8765).
MCP_SERVER_PORT = 8766

# Auto-connect on add-in start
MCP_AUTO_CONNECT = True

# Runtime log is outside the repository so public checkouts stay clean.
LOG_FILE = os.path.expanduser("~/brepwright.log")

# Debug mode
DEBUG = False
