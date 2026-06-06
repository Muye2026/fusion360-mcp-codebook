# Architecture History

Brepwright went through three architecture options before the open-source mainline was selected.

## A: Codebook

The Codebook is the verified Fusion API knowledge base. It contains scripts and notes that record working API patterns, unit conversions, and pitfalls found through live Fusion testing.

Status: retained as `codebook/`.

Role: regression reference and source material for reliable tools.

## B: Direct Fusion Add-in

The direct add-in architecture runs an MCP endpoint inside the Fusion add-in runtime. Tool calls are dispatched back to Fusion's main thread through CustomEvent and then executed with direct `adsk.core` and `adsk.fusion` API calls.

Status: selected mainline.

Reason: it keeps the runtime local, avoids an extra gateway process, makes thread ownership explicit, and lets Brepwright build high-level workflows on top of tested API patterns.

## C: Gateway Experiment

The gateway architecture routed an AI client through a local server and then into another Fusion MCP bridge.

Status: archived experiment.

Reason: it added process and dependency complexity without improving Brepwright's core value. It also made the repository look like another generic Fusion MCP server instead of a validated workflow layer.

## Final Direction

Brepwright keeps A as the golden knowledge base and B as the public runtime. C is preserved in git history for reference, but it is not part of the main branch.
