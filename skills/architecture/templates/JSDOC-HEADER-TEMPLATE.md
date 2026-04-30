<!--
Instructions for the agent: every entry-point file in `src/` carries a
short JSDoc header describing the concept it owns, the related files
it interacts with, and the ADR (or ADRs) that justify its design. The
header lives at the very top of the file, above any imports.

The header has at most 5 content lines plus the `/**` and `*/` markers.
If the explanation needs more, write a module README instead and link
it from the header.

The header is in English. The artifact prose elsewhere in the file
(comments, error messages) follows the user's working language.
-->

```ts
/**
 * @module {concept-name-from-architecture-map}
 *
 * Related files:
 *   - {relative/path/to/related-file.ts}: {one-line role}
 *   - {relative/path/to/another-file.ts}: {one-line role}
 *
 * ADR: ADR-{nn} ({short title})
 * Map row: src/ARCHITECTURE.map -> "{concept-name}"
 */
```

Notes for the writer:

- One line per related file. Drop the section if there are no related
  files (rare for entry-points).
- ADR link uses the canonical ID from `src/ARCHITECTURE.map`. If
  multiple ADRs apply, list them comma-separated.
- Map row line is a pointer back to the central wayfinder, so a reader
  can run `grep "{concept-name}" src/ARCHITECTURE.map` and see the
  extension pattern in one call.
- Do NOT list internal implementation details, line numbers, or
  algorithmic notes here. Those go into method-level JSDoc or the
  module README, not the header.
