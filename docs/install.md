# Installing Brepwright

## macOS

Use the install helper:

```bash
python3 scripts/install_addin.py --dry-run
python3 scripts/install_addin.py
```

The script copies `addin/Brepwright` into Fusion's user add-ins folder.

## Fusion

1. Open Autodesk Fusion.
2. Go to `Utilities -> Add-Ins -> Scripts and Add-Ins`.
3. Select `Brepwright`.
4. Click `Run`.

The add-in starts a local MCP endpoint at:

```text
http://127.0.0.1:8766/mcp
```

## MCP Client Config

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

## Uninstall

Stop the add-in from Fusion, then remove the copied `Brepwright` folder from Fusion's add-ins directory.

## Troubleshooting

- If the client cannot connect, confirm Fusion is open and the add-in is running.
- If port `8766` is busy, edit `addin/Brepwright/settings.py`.
- Logs are written to `~/brepwright.log` by default.
- Keep the endpoint local. Do not expose it to public networks.
