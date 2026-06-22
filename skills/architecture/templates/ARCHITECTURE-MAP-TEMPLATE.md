<!-- See skills/architecture/SKILL.md for how to fill -->
# Architecture Map
# Format: `concept | entry-point | adr | how-to-extend` (separator ` | `, `#` = comment).
# Usage: `grep "<keyword>" src/ARCHITECTURE.map`, then open the entry-point JSDoc.

# {SECTION-1: e.g. MAIN PROCESS (src/main/)}
{concept-1}        | {entry-point/path/to/file.ts}             | ADR-{nn} | {how to extend: one short sentence}
{concept-2}        | {entry-point/path/to/file.ts}             | ADR-{nn} | {how to extend}
{concept-3}        | {entry-point/path/to/file.ts}             | -        | {how to extend, or - if trivial}

# {SECTION-2: e.g. RENDERER (src/renderer/)}
{concept-4}        | {path/to/file.tsx}                        | ADR-{nn} | {how to extend}
