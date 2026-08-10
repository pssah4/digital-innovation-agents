# Canonical specs (full detail)

Canonical source for every V-Model skill. The SKILL.md body carries the
index; this file carries the full rules. Phase skills and templates
never restate these specs; they link to `project-conventions`.

## 2. Frontmatter spec

Artifact frontmatter carries identity and relations only. No state.

**Allowed keys.**

- Identity: `id`, `title`, `date` (creation date)
- Relations (only present when populated):
  - `epic`: parent epic id (string), used by FEAT/IMP/FIX/PLAN
  - `feature`: parent feature id (string), used by IMP/FIX/PLAN
  - `ba-ref`: relative path to the Item-BA (string), used by EPIC/FEAT/IMP/FIX
  - `project-ba-ref`: relative path to `BA-{PROJECT}.md` (string), MANDATORY on every Item-BA
  - `hmw-ref`: link to the HMW question this artifact answers (string, optional)
  - `adr-refs`: list of ADR ids (used by FEAT/PLAN)
  - `feature-refs`: list of FEAT ids (used by ADR)
  - `supersedes`, `superseded-by`: ADR linkage (strings)
  - `subtype`: `user-facing` or `library` (FEATURE only)
  - `depends-on`: list of artifact ids (cross-cutting dependency)
  - `kind`: ADR only, `constraint` | `choice` | `post-hoc` (default `choice`)
  - `reversal-cost`: ADR only, `low` | `medium` | `high`
  - `applies-to`: ADR only, list of kebab-case domain tags
  - `read-when`: ADR only, one-line trigger phrase ("changing X")

**Forbidden keys.** `status`, `phase`, `last_updated`, `last-updated`,
`lastUpdated`, `author`, `owner`, `claim`. State lives in the BACKLOG
row. Frontmatter status is stripped by
`tools/migration/strip_frontmatter_status.py` and flagged as N-15
by `/consistency-check`.

**Empty refs are omitted, never stubbed as `[]`.** If a feature has no
ADRs, omit `adr-refs`; do not write `adr-refs: []`.

## 3. Backlog vocabulary

The BACKLOG.md table column order is binding (parsed by index in
four tools): `| ID | Type | Title | Status | Phase | Prio | Refs | Source | Commit | Claim | Last change | Notes |`.

**Status (artifact lifecycle).** Aligned 1:1 with GitHub Projects so
`flow.py sync-status` stays consistent.

- `Backlog`: captured, not yet prioritized. Also the resting place for
  blocked or deferred items.
- `Ready`: prioritized, scheduled, free to be claimed.
- `In Progress`: someone is actively working on it.
- `In Review`: PR open, awaiting review or quality gates.
- `Done`: merged. Row stays under its Epic for traceability.

Legacy status values (migrated by
`tools/migration/migrate_status_vocabulary.py`): `Planned -> Ready`,
`Active -> In Progress`, `Review -> In Review`, `Waiting -> Backlog`,
`Deferred -> Backlog`. `Done` stays `Done`.

**Phase tags (git annotated tags, format `<id>/<phase>-done`).** Set
via `python3 tools/github-integration/flow.py tag-phase
--item <ID> --phase <phase>`.

- `ba-done`, `re-done`, `arch-done`, `plan-done`, `code-done`,
  `test-done`, `sec-done`

Legacy `audit-done` is still accepted as an alias for `sec-done`.

**Phase-end commit trailers (binding since v4).** Every phase-end
commit carries machine-readable trailers instead of a HANDOFFS.md
entry:

```
Refs: FEAT-01-03, ADR-04
DIA-Phase: arch-done
DIA-Handoff: FEAT-01-03 -> coding
DIA-Triage: FEAT-01-03 feature
```

`DIA-Phase` uses the phase-tag vocabulary above. `DIA-Handoff` names
the item and the next skill. `DIA-Triage` replaces the old
`triage:`/`triage_kind:` handoff fields; a skill that finds a
`DIA-Triage` trailer for its item skips its Phase-0 triage question.
Read with `git log --format='%(trailers:key=DIA-Handoff,valueonly)'`.
Legacy `HANDOFFS.md` files stay untouched and are skipped by tooling.

**Type union.** `BA`, `EPIC`, `FEAT`, `ADR`, `PLAN`, `IMP`, `FIX`.
Backlog rows additionally use `Security`, `Bug-Followup`, `BL-Item`
for items that do not bind to a detail-file type.

**Source union.** `manual`, `derived`, `reverse-engineered`. Backlog
rows additionally carry the producing skill: `BA`, `RE`, `REV`,
`SEC`, `USER`, `BUG`, `CONSISTENCY-CHECK`.

**Priority.** `P0` (blocker, immediate), `P1` (short-term), `P2`
(mid-term). `P3` exists in GitHub labels for idea-stage items but
does not enter the implementation queue.

**ID schema.**

| Type | Pattern | Example |
|------|---------|---------|
| Project-BA | `BA-{PROJECT}` | `BA-myapp` |
| Epic | `EPIC-{ee}` | `EPIC-04` |
| Feature | `FEAT-{ee}-{ff}` | `FEAT-04-02` |
| ADR | `ADR-{ee}-{nn}` | `ADR-04-03` |
| Improvement | `IMP-{ee}-{ff}-{nn}` | `IMP-04-02-01` |
| Fix | `FIX-{ee}-{ff}-{nn}` | `FIX-04-02-03` |
| Plan | `PLAN-{ee}-{ff}-{nn}` | `PLAN-04-02-01` |

IDs are monotonic and never reused. `{ee}` is the parent epic
counter, `{ff}` the feature counter local to that epic, `{nn}` the
artifact counter local to that feature (or epic for ADR).

**Claim column.** Format `{pair-id} @ {YYYY-MM-DD}`. Empty cell means
free. Example: `sebastian-opus-4.7 @ 2026-04-19`. The Claim
protocol is documented in `skills/dia-guide/SKILL.md`.

**Refs column.** Comma-separated artifact ids forming the relation
graph. Examples: `EPIC-04, ADR-04-03, PLAN-04-02-01`. Edges in the
artifact graph derive from this column; `/consistency-check` uses it
for orphan and cycle detection.

## 5. Activation Path format

Every FEATURE spec carries an `## Activation Path` section.
`/consistency-check` rule N-18 parses it via the anchored regex
`^## Activation Path\s*$`; the heading text is fixed and untranslated.

**Format (user-facing subtype, default):**

```markdown
## Activation Path

- Type: command | route | UI-element | endpoint | scheduled-job | tool | hotkey | public-API
- Identifier: <command name | route path | URL | symbol name>
- Where it lives: <file or section pointer>
- How a user (or caller) reaches it: <one sentence>
```

**Format (library subtype):**

```markdown
## Activation Path

- Type: public-API
- Identifier: `<exported function or class name>`
- Where it lives: <module path or package export>
- How a caller reaches it: imported and called as documented in <doc reference>
```

The `Type:` and `Identifier:` sub-bullets are parsed by
`/consistency-check`; renaming or translating either breaks N-18.

## 6. Priority / Effort legend

**Priority.**

- `P0`: blocker. Drop other work. Ship today or tomorrow.
- `P1`: short-term. Next iteration.
- `P2`: mid-term. Backlog with intent. Revisit at next planning.
- `P3` (labels only): idea stage. Not committed.

**Effort scale.** Coarse, relative, set at FEAT or PLAN scope.

| Scale | Rough size | Typical artifact |
|-------|------------|------------------|
| XS | under 1 hour | FIX, doc tweak |
| S  | half a day  | IMP, small FEAT |
| M  | one to two days | typical FEAT |
| L  | one week | multi-FEAT change, ADR with prototype |
| XL | over one week | epic-scope; split into FEATs first |

XL is a smell at FEAT scope. If a FEAT scopes XL, split it before
implementation starts.

## 8. Section policy

Sections are emitted only when they carry decision content. Optional
sections live in this convention (or in the relevant template
comment), not as pre-rendered `TBD` placeholders in the saved
artifact. A FEATURE without ADRs omits the ADR section entirely; it
does not write `## ADRs\n\nTBD`.

This applies to every template under `skills/*/templates/`. Templates
list optional sections in HTML comments at the top so the producing
skill knows what is available; the skill writes a section only when
it has substance.

## The `_devprocess/context/` files

Living documents under `_devprocess/context/`:

- **`BACKLOG.md`** -- the project backlog and **single source of
  truth for project state and the artifact relation graph**. Follows
  the binding template at
  `skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`.
  One row per artifact (Feature, ADR, Plan, Fix, Improvement, Epic,
  BL-Item) with status, phase, claim, refs, and commit SHA. Bug
  entries live as FIX-{ee}-{ff}-{nn} rows directly in this file; the
  detail file at `_devprocess/requirements/fixes/FIX-*.md` carries
  the substance. There is NO separate bug-log aggregation file.
  Status-changing actions update the backlog row BEFORE the artifact
  body.
- **`BACKLOG-HISTORY.md`** -- append-only session history, one line
  per entry (`## {YYYY-MM-DD} {skill}: {one line}`). Git log is the
  authoritative history; this file is a convenience index. Never
  accumulate `[Previous]` blocks inside BACKLOG.md itself.
- **`METRICS.md`** -- signal layer (cycle time, drift count, hypothesis
  validation, phase transitions, mid-course trigger counts). Populated
  by `/coding`, `/business-analysis`, `/dia-guide`. See
  `skills/dia-guide/templates/METRICS-TEMPLATE.md`.

Phase handoffs live in phase-end commit trailers (see Backlog
vocabulary above), not in a handoffs file. A legacy `HANDOFFS.md` in
an existing project stays where it is; `/dia-realign` offers a
deprecation header and an archive move.

FIX and IMP detail files live under
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` and
`_devprocess/requirements/improvements/IMP-{ee}-{ff}-{nn}-{slug}.md`
(parallel to `epics/` and `features/`).

## `_devprocess/analysis/` layout rule

Flat layout. Every artefact carries a type prefix in its filename and
sits at the analysis/ root. No subfolders per artefact type.

- `BA-{PROJECT}.md`                       -- Project-BA, singleton, product-layer
- `BA-EPIC-{nn}-{slug}.md`                -- Item-BA for a new epic (mandatory before EPIC)
- `BA-FEAT-{ee}-{ff}-{slug}.md`           -- Item-BA for a new feature (mandatory before FEAT)
- `BA-IMP-{ee}-{ff}-{nn}-{slug}.md`       -- Item-BA for an improvement (optional)
- `BA-FIX-{ee}-{ff}-{nn}-{slug}.md`       -- Item-BA for a fix (optional)
- `EXPLORE-{PROJECT}.md`                  -- Exploration Board (optional, one per project)
- `AUDIT-{PROJECT}-{DATE}.md`             -- Security Audit Report (n per project)
- `RESEARCH-{TOPIC}.md`                   -- Research note (n per project, optional)
- `ADR-{nn}-review.md`                    -- Root-cause review for an ADR amendment

The single exception is `analysis/sources/`, a subfolder for user-
provided source documents. Files in `sources/` use a
`SOURCE-{name}.{ext}` prefix and are read-only from the skill's
perspective; only the user copies files there.

## Artifact language (binding)

Every skill produces the documents under `_devprocess/` in the
language the user uses in chat. A language switch by the user pulls
subsequent artifacts; existing artifacts are not auto-translated. On
ambiguity (mixed DE/EN, very short first turn), the skill asks one
short question before the first artifact:

> "Which language should the artifacts use, German or English?"

Excluded: code, identifiers, commit messages, `docs/`, `README`,
skill files, and English keyword fields (frontmatter keys, template
placeholders, technical terms such as `status`, `phase`, `Epic`,
`Feature`, `ADR`, `Refs`).

## Debugging conventions

Bugs as causal chains:

```
Problem: [observable behavior]
Root Cause: [why it happens]
Chain: step 1 -> step 2 -> ... -> error
```

Bug IDs: `FIX-{ee}-{ff}-{nn}` (P0 = immediate, P1 = short-term, P2 =
medium-term). Security findings: `H-N` / `M-N` / `L-N`. All bugs land
as a FIX row in `_devprocess/context/BACKLOG.md` plus a detail file
under `_devprocess/requirements/fixes/` carrying symptom, root cause
(causal chain), fix, and regression test.

## Initializing a project

```bash
mkdir -p _devprocess/{analysis/sources,requirements/{epics,features,fixes,improvements,handoff},architecture,rules,implementation/plans,context}
mkdir -p src docs scripts memory
```

Initial files:

- `_devprocess/context/BACKLOG.md` -- seeded from
  `skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`
- `_devprocess/rules/technical.md` (and `design.md` if UI,
  `domain.md`) -- seeded from `skills/architecture/templates/RULES-*`
  (full profile; the lean profile consolidates rules into AGENTS.md
  instead, see `skills/dia-setup/SKILL.md`)
- `src/ARCHITECTURE.map` -- seeded from
  `skills/architecture/templates/ARCHITECTURE-MAP-TEMPLATE.md`
- `CLAUDE.md` (project context), `memory/MEMORY.md`
