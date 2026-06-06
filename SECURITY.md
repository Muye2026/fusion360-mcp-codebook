# Security Policy

Brepwright is a local Autodesk Fusion add-in that exposes an MCP endpoint.

## Local Execution Risk

The MCP endpoint can execute Fusion Python code through tools such as `execute_python`. Treat any connected MCP client as code execution inside your Fusion session.

Default safety expectations:

- Bind only to `127.0.0.1`.
- Do not expose the MCP endpoint to the public internet.
- Do not connect untrusted MCP clients.
- Review generated Python before using `execute_python` for destructive design changes.
- Keep exported design packs out of sensitive folders unless you intend to share them.

## Supported Versions

Security fixes target the current main branch until versioned releases are published.

## Reporting

Open a GitHub issue with a minimal reproduction. Do not include private model files, tokens, local absolute paths, or proprietary CAD data in public reports.
