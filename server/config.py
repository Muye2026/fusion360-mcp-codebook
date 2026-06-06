"""Configuration for Fusion 360 MCP Codebook Server."""

import os

# Upstream frankhommers MCP Server (runs inside Fusion 360 as Add-in)
UPSTREAM_URL = os.getenv("FUSION_UPSTREAM_URL", "http://127.0.0.1:8765/mcp")

# This server's configuration
HOST = os.getenv("FUSION_SERVER_HOST", "0.0.0.0")
PORT = int(os.getenv("FUSION_SERVER_PORT", "8000"))

# Path to the codebook root (parent of server/)
CODEBOOK_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Unit convention: MCP tools accept mm, Fusion API uses cm internally
# Conversion: divide by 10.0
MM_TO_CM = 0.1
