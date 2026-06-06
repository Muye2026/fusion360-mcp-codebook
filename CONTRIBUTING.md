# Contributing

Contributions are welcome when they improve reliability, verification, or product-level CAD workflows.

## Tool Requirements

New tools must include at least one of:

- A Codebook script under `codebook/` that demonstrates the underlying Fusion API pattern.
- A live Fusion verification note with input parameters, expected result, and observed result.

Tool behavior should follow these rules:

- User-facing dimensions are millimeters.
- Convert to Fusion's centimeter-based API internally.
- Prefer body and component names over indexes.
- Keep direct `adsk.core` and `adsk.fusion` calls on Fusion's main thread.
- Return structured inspection or export results when possible.
- Do not add Gateway C or `fozzfut/FusionMCP` dependencies to the mainline.

## Testing

Run CI-safe tests before submitting changes:

```bash
python3 -m unittest discover -s tests -v
```

For live Fusion changes, document the manual verification flow in a pull request or release note.

## Documentation

Avoid copying Autodesk documentation into this repository. Link to official pages and summarize only the project-specific lessons learned from live testing.
