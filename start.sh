#!/bin/bash
# Start the Fusion 360 MCP Codebook Server
# This server connects to FusionMCP (port 7432) and exposes MCP protocol (port 8000)

cd "$(dirname "$0")"
exec server/.venv/bin/python3 -m server.main
