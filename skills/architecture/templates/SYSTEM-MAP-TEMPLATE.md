<!-- Navigation map for agents (lean profile core artifact, useful in
     full profile too). Names stable boundaries and first code entry
     points. It is NOT a full module inventory and is read on demand,
     never auto-loaded. Cap: 120 lines. Project file:
     _devprocess/SYSTEM-MAP.md. -->

# System map: {project}

## System shape

{Three to four sentences: processes, boundaries, what talks to what.}

Core boundaries:

- {boundary}: `{src/entry-point}`
- {boundary}: `{src/entry-point}`

## Data ownership

- {store (DB, config, state)}: owned by `{module}`; nobody else writes

## Security invariants

- {invariant, e.g. "renderer never gets raw credentials"}
- {invariant; changing one of these requires a decision record BEFORE
  implementation}

## Fast paths

When changing {topic}: start in `{file1}`, `{file2}`, `{file3}`.

When changing {topic}: start in `{file1}`, `{file2}`.

## Decision hooks

Before changing a listed area, check `decisions/README.md` (or the
`applies-to`/`read-when` frontmatter of the ADRs) for a binding
decision. If a change would violate one, stop and ask.
