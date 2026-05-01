<!--
Instructions for the agent: produce this file at the project's source root
(typically `src/ARCHITECTURE.map`). Write the file content in the user's
working language conventions for prose, but keep the keywords (concept,
entry-point, adr, how-to-extend) in English. The file is grep-friendly
and lives next to the code, so the agent updates it whenever an
entry-point file is created, renamed, or deleted.
-->

# Architecture Map
#
# Flat lookup: concept -> entry-point file -> ADR -> how-to-extend pattern.
# Usage: `grep "<keyword>" src/ARCHITECTURE.map`, then read the entry
# file's JSDoc header for details.
#
# Format: `concept | entry-point | adr | how-to-extend`
# Columns are separated by ` | `. Lines starting with `#` are comments.
# Blank lines split sections. Keep one row per concept.
# Keep the file under ~80 lines. If it grows beyond that, split modules
# into module-level READMEs and link them here.

# {SECTION-1: e.g. MAIN PROCESS (src/main/)}
{concept-1}        | {entry-point/path/to/file.ts}             | ADR-{nn} | {how to extend: one short sentence}
{concept-2}        | {entry-point/path/to/file.ts}             | ADR-{nn} | {how to extend}
{concept-3}        | {entry-point/path/to/file.ts}             | -         | {how to extend, or - if trivial}

# {SECTION-2: e.g. RENDERER (src/renderer/)}
{concept-4}        | {path/to/file.tsx}                        | ADR-{nn} | {how to extend}

# {SECTION-3: e.g. SHARED (src/shared/)}
{concept-5}        | {path/to/dir/}                            | -         | {how to extend, or - if trivial}
