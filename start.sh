#!/usr/bin/env bash
# Start the Fusion 360 MCP Codebook Server
# Prerequisites: Python 3.10+, mcp[cli] and pydantic installed
#
# Usage:
#   ./start.sh                # Start on default port 8000
#   FUSION_SERVER_PORT=9000 ./start.sh  # Custom port

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Check for virtual environment
if [ -d ".venv" ]; then
    PYTHON=".venv/bin/python"
elif [ -d "server/.venv" ]; then
    PYTHON="server/.venv/bin/python"
else
    PYTHON="python3"
fi

echo "Starting Fusion 360 MCP Codebook Server..."
echo "  Python: $PYTHON"
echo "  Upstream: ${FUSION_UPSTREAM_URL:-http://127.0.0.1:8765/mcp}"
echo "  Port: ${FUSION_SERVER_PORT:-8000}"
echo ""

exec $PYTHON -m server.main
