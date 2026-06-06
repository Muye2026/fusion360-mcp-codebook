# Brepwright

Validated AI CAD workflows for Autodesk Fusion via MCP.

Brepwright is a local Autodesk Fusion add-in that exposes a small, tested MCP tool surface for AI agents. It focuses on reliable part creation, inspection, screenshots, exports, and repeatable design-pack delivery rather than competing to expose every Fusion command.

## Positioning

Brepwright is:

- Codebook-backed: core tool patterns are grounded in scripts that were validated against Fusion.
- Workflow-first: high-level tools create practical parts such as mounting plates, enclosure shells, and brackets.
- Verification-first: inspection, screenshots, mass properties, and export checks are part of the normal loop.
- Small by design: the public surface favors reliable operations over a long list of thin API wrappers.

Brepwright is not:

- An Autodesk official project.
- A replacement for Autodesk's built-in local Fusion MCP endpoint.
- A generic "maximum number of tools" Fusion MCP server.
- A wrapper around `fozzfut/FusionMCP` or the archived Gateway experiment.

## Why This Exists

AI agents can already connect to Fusion through several MCP servers. The harder problem is making agents produce stable mechanical geometry without guessing Fusion API signatures or skipping verification. Brepwright treats the tested Codebook as the source of truth and wraps it in a product-oriented execution layer.

Related projects worth knowing:

- [Autodesk Fusion MCP docs](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_FusionDesktopMcp_connecting_to_the_fusion_mcp_server_html)
- [frankhommers/autodesk-fusion-mcp](https://github.com/frankhommers/autodesk-fusion-mcp)
- [faust-machines/fusion360-mcp-server](https://github.com/faust-machines/fusion360-mcp-server)
- [JustusBraitinger/FusionMCP](https://github.com/JustusBraitinger/FusionMCP)
- [ArchimedesCrypto/fusion360-mcp-server](https://github.com/ArchimedesCrypto/fusion360-mcp-server)
- [ndoo/fusion360-mcp-bridge](https://github.com/ndoo/fusion360-mcp-bridge)

## Architecture

```text
AI Client
  -> Brepwright local MCP endpoint
  -> Fusion Add-in runtime
  -> Fusion CustomEvent main-thread dispatcher
  -> direct adsk.core / adsk.fusion API calls
  -> model + screenshot + export pack + verification result
```

The default endpoint is:

```text
http://127.0.0.1:8766/mcp
```

Port `8766` avoids common conflicts with Autodesk's `27182` endpoint and other community add-ins that use `8765`.

## Repository Layout

```text
addin/Brepwright/              Fusion add-in and MCP runtime
codebook/                      validated Fusion API scripts and reference index
docs/                          architecture, installation, and verification docs
scripts/install_addin.py       install helper with dry-run mode
tests/                         CI-safe tests that do not require Fusion
```

## Tool Surface

Baseline tools include primitives, features, transforms, surfaces, assembly, export, inspection, and `execute_python`.

Workflow tools:

- `create_mounting_plate`
- `create_enclosure_shell`
- `create_bracket`
- `inspect_design`
- `export_design_pack`
- `validate_part_for_printing`

System tools:

- `ping`
- `get_runtime_status`
- `get_active_design_info`

All user-facing dimensions are in millimeters. Fusion API calls are converted to centimeters internally.

## Quickstart

1. Install Autodesk Fusion.
2. Install the add-in:

```bash
python3 scripts/install_addin.py --dry-run
python3 scripts/install_addin.py
```

3. In Fusion, open `Utilities -> Add-Ins -> Scripts and Add-Ins`, select `Brepwright`, and run it.
4. Configure your MCP client:

```json
{
  "mcpServers": {
    "brepwright": {
      "type": "http",
      "url": "http://127.0.0.1:8766/mcp"
    }
  }
}
```

5. Call `ping`, then `get_active_design_info`.

## Verification

CI runs only tests that do not require Fusion:

```bash
python3 -m unittest discover -s tests -v
```

Live Fusion verification is manual and should cover:

- `ping`
- `create_cube`
- `fillet_edge`
- `create_hole`
- `inspect_design`
- `capture_viewport`
- `export_design_pack`

See [docs/verification-report.zh.md](docs/verification-report.zh.md) for the original Chinese verification notes.

## Security

Brepwright runs locally and can execute Fusion Python through MCP. Keep it bound to `127.0.0.1` and do not expose the endpoint to a network you do not trust. See [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).

This project includes an adapted standard-library Streamable HTTP MCP runtime inspired by `frankhommers/autodesk-fusion-mcp`; attribution is retained in [NOTICE](NOTICE).
