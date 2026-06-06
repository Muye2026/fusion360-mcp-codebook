# Autodesk MCP Strategy

Autodesk provides a local Fusion MCP endpoint documented here:

https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_FusionDesktopMcp_connecting_to_the_fusion_mcp_server_html

Brepwright does not try to replace that endpoint. The project focuses on a narrower layer:

- tested part-building workflows;
- Codebook-backed API patterns;
- inspection, screenshot, and export verification;
- repeatable design-pack outputs for AI agents.

Future compatibility work can add an optional backend abstraction that delegates low-level operations to Autodesk's official endpoint when that is the better integration path. The public mainline should still preserve Brepwright's workflow-first surface.
