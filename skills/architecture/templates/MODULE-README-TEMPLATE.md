<!--
Instructions for the agent: produce this file as `README.md` inside a
module directory under `src/` (e.g. `src/main/mcp/README.md`). Write
the prose in the user's working language; keep section names in
English so they grep consistently across modules.

The file is short (< 30 lines). It is a wayfinder, not a description
of code. The code is the source of truth. The README points the agent
at entry-points, patterns, and ADRs.
-->

# {Module name}

{One sentence: what this module owns, in user-outcome terms. No file
paths, no class names, no implementation details.}

## Structure

| Path or file | Purpose                            |
|--------------|------------------------------------|
| {file-1.ts}  | {one-sentence role}                |
| {dir-1/}     | {one-sentence role}                |
| {file-2.ts}  | {one-sentence role}                |

## Patterns

- {short pattern, e.g. "Every server registers itself in McpManager."}
- {short pattern, e.g. "New tools live next to their server, not in /tools/."}

## Related ADRs

- ADR-{nn}: {title} - {one sentence on how this ADR applies here}
- ADR-{nn}: {title} - {one sentence on how this ADR applies here}

## Wayfinder

This module is listed in `src/ARCHITECTURE.map` under the concept
`{concept-name}`. Run `grep "{concept-name}" src/ARCHITECTURE.map`
for the canonical entry-point and the extension pattern.
