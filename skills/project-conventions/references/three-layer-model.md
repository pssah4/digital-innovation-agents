# Three-layer documentation model

Every project organizes its V-Model documentation in three layers.
Each layer has a different update cadence, a different owner, and a
different audience. Mixing layers is the dominant source of
doc-vs-code drift, so the boundaries are binding.

| Layer            | Purpose                                                                                                          | Lives in                                                                                                          | Owner                                                              |
|------------------|------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| Wayfinder        | Concept-to-file lookup, navigational, grep-friendly                                                              | `src/ARCHITECTURE.map`, JSDoc headers in entry-point files, module READMEs                                        | `/coding` on every entry-point change                              |
| Rule sets        | Stable truths: stack, conventions, design rules, domain glossary. Hard cap 500 lines total.                      | `_devprocess/rules/technical.md`, `design.md` (if UI), `domain.md`. Lean profile: consolidated into AGENTS.md.    | `/architecture`, `/coding`                                         |
| Backlog          | Single source of truth for state and the artifact relation graph                                                 | `_devprocess/context/BACKLOG.md`                                                                                  | Every status-changing skill writes the row BEFORE the artifact     |
| Detail artifacts | Audit trail of the engineering process: BA, Epics, Features, Plans, Fixes, ADR detail                            | `_devprocess/analysis/`, `_devprocess/requirements/`, `_devprocess/architecture/`, `_devprocess/implementation/`  | `/business-analysis`, `/requirements-engineering`, `/architecture`, `/coding` |

**Status, phase, last-change, and claim of every artifact live in the
backlog row, not in the artifact frontmatter.** Artifact frontmatter
carries identity (`id`, `title`, `date`) and relations only. The
backlog is authoritative for state. This is the structural fix for the
most common drift class (status fields stuck at "Planned" while the
code shipped).

**Wayfinder layer rationale.** A model querying "where does X live?"
gets a single grep-friendly answer from `src/ARCHITECTURE.map` plus
the JSDoc header of the entry-point. Concrete code paths that age
fast (file names, line numbers, method signatures) live in the code
or next to it, never in detail artifacts.

**Detail artifact discipline.** Detail artifacts hold the substance
that does not age fast (problem, decision, rejected alternatives,
success criteria, reasoning). They do NOT list current code paths in
core sections. ADRs are allowed an optional `## Implementation Notes`
appendix that may go stale. FEATUREs are allowed an optional
`## Code Pointer` appendix that references an ARCHITECTURE.map
concept name, not a file path.

**ADR abstraction rule.** ADR core sections (`## Kontext` /
`## Context`, `## Decision Drivers` / `## Begründung`,
`## Considered Options`, `## Entscheidung` / `## Decision`,
`## Konsequenzen` / `## Consequences`) contain NO code paths, file
names, line numbers, or method signatures. Code-level hints belong in
the optional `## Implementation Notes` appendix (allowed to go stale)
or in `## Sources` (post-hoc ADRs). `/consistency-check` rule A-1
enforces this against the German and English heading variants.

**ADR / FEATURE / PLAN separation.**

- **ADR** answers "what is the architectural decision and why?". No
  tasks, no code paths in core sections.
- **FEATURE** answers "what should the user be able to do?". No
  tasks, no implementation details.
- **PLAN** answers "how is it concretely implemented?". Tasks with
  file paths and verify commands live HERE and only here.
