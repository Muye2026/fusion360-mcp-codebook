"""FusionBridge — communicates with FusionMCP (fozzfut) via HTTP POST."""

import json
import logging
import urllib.request
import urllib.error

from . import config

logger = logging.getLogger(__name__)


class FusionBridge:
    """Encapsulates communication with the upstream FusionMCP HTTP bridge.

    FusionMCP exposes a plain HTTP POST API (not MCP protocol) on localhost:7432.
    Each call sends a JSON POST request and returns the result.

    FusionMCP response format:
        {"success": true, "output": "result string"}   — success with output
        {"success": true, "output": null}              — success, no output
        {"success": false, "error": "error message"}   — execution error
        {"error": "connection error message"}          — network error
    """

    def __init__(self, upstream_url: str | None = None):
        self.upstream_url = upstream_url or config.UPSTREAM_URL

    def _post(self, command: str, params: dict | None = None) -> dict:
        """Send a command to FusionMCP via HTTP POST.

        Args:
            command: The FusionMCP command name (e.g., 'execute_script', 'fusion_status').
            params: Optional parameters dict.

        Returns:
            The parsed JSON response dict.
        """
        payload = {"command": command}
        if params:
            payload["params"] = params

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.upstream_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = resp.read().decode("utf-8")
                logger.debug("_post raw response: %s", raw[:500])

                # Parse JSON response
                try:
                    result = json.loads(raw)
                except json.JSONDecodeError:
                    # If raw is not valid JSON, wrap it
                    logger.warning("_post received non-JSON: %s", raw[:200])
                    return {"success": True, "output": raw}

                # Ensure we always return a dict
                if not isinstance(result, dict):
                    logger.warning("_post returned non-dict type: %s", type(result))
                    return {"success": True, "output": str(result)}
                return result
        except urllib.error.URLError as e:
            return {"error": f"Failed to reach FusionMCP at {self.upstream_url}: {e}"}
        except json.JSONDecodeError as e:
            return {"error": f"FusionMCP returned invalid JSON: {e}\nRaw: {raw[:500]}"}
        except Exception as e:
            return {"error": f"FusionMCP request failed: {e}"}

    async def execute_python(self, code: str) -> str:
        """Execute Python code in the live Fusion 360 session via FusionMCP.

        Args:
            code: Python code string to execute. Has access to adsk.core and adsk.fusion.

        Returns:
            The output text from FusionMCP, or an error message.
            Always returns a plain string suitable for MCP TextContent.
        """
        logger.info("execute_python called, code length=%d", len(code))

        result = self._post("execute_script", {"code": code})
        logger.error("DEBUG: _post returned type=%s, val=%s", type(result), str(result)[:300])

        # Sanity: _post must return a dict
        if not isinstance(result, dict):
            err = str(result)
            logger.error("execute_python: _post returned non-dict type=%s, val=%s", type(result), err[:200])
            return f"[FusionBridge Error] _post returned non-dict: {err[:200]}"

        # Case1: Network/JSON error from _post itself
        if "error" in result and "success" not in result:
            err_msg = result.get("error", str(result))
            logger.error("execute_python network error: %s", err_msg[:200])
            return f"[FusionBridge Error] {err_msg}"

        # Case2: FusionMCP reports execution failure
        success = result.get("success", False)
        if not success:
            err_detail = result.get("error") or result.get("output") or str(result)
            logger.warning("execute_python fusion error: %s", str(err_detail)[:200])
            return f"[Fusion Error] {err_detail}"

        # Case3: Success with output text
        output = result.get("output")
        if output is not None and isinstance(output, str) and output.strip():
            logger.info("execute_python OK, output length=%d", len(output))
            return output

        # Case4: Success but no output (output is null or empty)
        logger.info("execute_python OK, no output")
        return "[OK] Code executed successfully (no output)"

    async def call_tool(self, tool_name: str, arguments: dict | None = None) -> str:
        """Call an arbitrary command on FusionMCP.

        Args:
            tool_name: The FusionMCP command name.
            arguments: Parameters to pass.

        Returns:
            The result text, or an error message.
        """
        result = self._post(tool_name, arguments)
        if not isinstance(result, dict):
            return f"[FusionBridge Error] _post returned non-dict: {result}"
        if "error" in result and "success" not in result:
            return f"[FusionBridge Error] {result['error']}"
        return json.dumps(result, ensure_ascii=False, indent=2)

    def call(self, command: str, params: dict | None = None) -> dict:
        """Call a FusionMCP command and return the raw dict result.

        Args:
            command: The FusionMCP command name.
            params: Optional parameters dict.

        Returns:
            The parsed JSON response dict.
        """
        return self._post(command, params)

    async def health_check(self) -> bool:
        """Check if FusionMCP is reachable.

        Returns:
            True if reachable, False otherwise.
        """
        try:
            result = self._post("fusion_status")
            if not isinstance(result, dict):
                return False
            return "error" not in result or result.get("success", False)
        except Exception:
            return False


# Global singleton instance
bridge = FusionBridge()
