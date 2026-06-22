---
name: project-conventions
description: >
  Defines project structure, naming conventions, and way of working for all
  projects. Referenced by other skills to ensure consistent directory
  structures, file names, and documentation standards. Use this skill when
  the user mentions "project setup", "project structure", "conventions",
  "init", "initialize project", "directory structure", or similar. Also
  automatically relevant when starting a new project.
disable-model-invocation: false
---

# Project Structure & Conventions

This skill defines the binding standards for directory structures, file
names, and ways of working. All other skills (BA, RE, Architecture, Coding,
Testing, Security Audit) follow these conventions.

## Codebase-Awareness -- Core Principle

All skills operate in the context of the existing codebase, never in a
vacuum. Read `references/codebase-awareness.md` for the complete rules.

Summary: Before any work, read existing code, recognize patterns, understand
dependencies, check reference implementations. The project's `CLAUDE.md`
takes PRECEDENCE over generic skill instructions.

## Canonical Specs (single home; other skills link here)

These specs are the canonical source for every V-Model skill (BA, RE,
Architecture, Coding, Testing, Security-Audit, Consistency-Check,
Reverse-Engineering). Phase skills do not restate them; they link
back to this section. Templates do not pre-render them; they leave
placeholders that the producing skill fills based on the rules here.

### 1. Reader budget (the under-2-minute rule)

Every produced artifact must be scannable by a human reader in under
two minutes. The number that operationalizes this is a per-artifact
hard line cap. Skills measure with `wc -l` against the cap before
handoff.

**Exceeding the cap.** A cap may be exceeded only with a one-line
justification at the top of the file:

```markdown
## Reasoned exception

Cap raised from <N> to <M> lines: <one-sentence reason>.
```

Without that block, `/consistency-check` flags the artifact as
over-cap. The exception block is read during review; agents do not
add it routinely.

**Hard caps (binding).**

| Artifact | Cap | Notes |
|---|---|---|
| Project-BA | 200 lines | Initial discovery only |
| EPIC-BA | 120 lines | Item-BA at epic scope |
| FEAT-BA | 60 lines | Item-BA at feature scope |
| BA-MINI (IMP/FIX) | 40 lines | |
| EXPLORATION-BOARD | 70 lines | Scratchpad |
| EPIC | 40 lines | |
| FEATURE | 65 lines | |
| BACKLOG | 80 lines + rows | Header+vocab leg+pointers cap; rows uncapped |
| ARCHITECT-HANDOFF | 60 lines | Dialog grows in-place |
| ADR | 60 lines | Excluding optional Implementation Notes; includes 7-line German-variant translation note |
| arc42 | 65 lines (PoC) / 100 (MVP) | |
| plan-context | 55 lines | |
| PLAN | 50 lines | Plus uncapped Change Log tail |
| FIX | 32 lines | |
| IMP | 30 lines | |
| AUDIT | 65 lines | Plus uncapped finding tables |
| METRICS | 50 lines | |
| ARCHITECTURE-MAP, MODULE-README, JSDOC-HEADER, RULES-* | per-template caps in template comments | |

### 2. Frontmatter spec

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

**Forbidden keys.** `status`, `phase`, `last_updated`, `last-updated`,
`lastUpdated`, `author`, `owner`, `claim`. State lives in the BACKLOG
row. Frontmatter status is stripped by
`tools/migration/strip_frontmatter_status.py` and flagged as N-15
by `/consistency-check`.

**Empty refs are omitted, never stubbed as `[]`.** If a feature has no
ADRs, omit `adr-refs`; do not write `adr-refs: []`. Stub keys add
noise and trigger false-positive graph edges.

### 3. Backlog vocabulary

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
artifact graph derive from this column;
`/consistency-check` uses it for orphan and cycle detection.

### 4. Writing style (canonical home)

The writing style applies to every artifact produced by every
V-Model skill (BA, EXPLORE, EPIC, FEATURE, ADR, arc42,
plan-context, architect-handoff, backlog rows, FIX, IMP,
audit reports, release notes, CHANGELOG, METRICS). It applies to
prose written at runtime, not only to templates.

**Zero em dashes, zero en dashes.** No U+2014, no U+2013, no
double-hyphen substitute written as two ASCII hyphens to fake an em
dash. Use a period, a comma, parentheses, or a plain `and` / `but`.

**Pre-save scan (binding).** Before writing or editing an artifact,
the producing skill mentally greps the output for:

- U+2014 (em dash), U+2013 (en dash): zero hits required.
- AI vocabulary: `landscape`, `nuanced`, `delve`, `leverage`,
  `utilize`, `intricate`, `crucial`, `pivotal`, `robust`,
  `seamless`, `game-changing`, `revolutionary`, `unlock`,
  `empower`, `comprehensive`, `holistic`, `foster`, `ensuring`,
  `highlighting`, `underscoring`, `emphasizing`, `reflecting`,
  `symbolizing`.
- Negative parallelisms: `not X but Y`, `it is not about A, it is
  about B`, `more than just X`. Rewrite to the positive form.
- Filler phrases: `in order to`, `it is important to note`,
  `needless to say`, `due to the fact that`.
- Inflated symbolism: `at its core`, `fundamentally`, `the real
  question is`, `this matters because`.
- Copula avoidance: `X serves as Y`, `X stands as Y`. Write `X is Y`.
- Superficial -ing tails: `highlighting the importance of X`,
  `reflecting the commitment to Y`.
- Rule-of-three padding: if a default list has exactly three parallel
  items, drop to two, add a fourth, or rewrite.
- Vague attributions: `it is often said`, `many believe`, `experts
  argue` (unless a source is named).
- Meta-signposting: `let me break this down`, `here is what you need
  to know`. Write the content instead.

**Active voice by default. Sentence case in headings.** No title case.

Any hit is rewritten before the artifact is saved. This applies
equally to brand-new artifacts, edits, and promotions from draft to
validated.

### 5. Activation Path format (canonical)

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

### 6. Priority / Effort legend

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

### 7. Three-layer model boundaries

| Layer            | Purpose                                                                                                          | Lives in                                                                                                          | Owner                                                              |
|------------------|------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| Wayfinder        | Concept-to-file lookup, navigational, grep-friendly                                                              | `src/ARCHITECTURE.map`, JSDoc headers in entry-point files, module READMEs                                        | `/coding` on every entry-point change                              |
| Rule sets        | Stable truths: stack, conventions, design rules, domain glossary. Hard cap 500 lines total.                      | `_devprocess/rules/technical.md`, `_devprocess/rules/design.md` (if UI), `_devprocess/rules/domain.md`            | `/architecture`, `/coding`                                         |
| Backlog          | Single source of truth for state and the artifact relation graph                                                 | `_devprocess/context/BACKLOG.md`                                                                                  | Every status-changing skill writes the row BEFORE the artifact     |
| Detail artifacts | Audit trail of the engineering process: BA, Epics, Features, Plans, Fixes, ADR detail                            | `_devprocess/analysis/`, `_devprocess/requirements/`, `_devprocess/architecture/`, `_devprocess/implementation/`  | `/business-analysis`, `/requirements-engineering`, `/architecture`, `/coding` |

**ADR abstraction rule.** ADR core sections (`## Kontext` / `## Context`,
`## Decision Drivers` / `## Begründung`, `## Considered Options`,
`## Entscheidung` / `## Decision`, `## Konsequenzen` /
`## Consequences`) contain NO code paths, file names, line numbers,
or method signatures. Code-level hints belong in the optional
`## Implementation Notes` appendix at the bottom of the ADR, which
is allowed to go stale. The wayfinder (`src/ARCHITECTURE.map` plus
the JSDoc header of the entry-point) is the canonical source for
current paths. `/consistency-check` rule A-1 enforces this against
the German and English heading variants.

**ADR / FEATURE / PLAN separation.**

- **ADR** answers "what is the architectural decision and why?". No
  tasks, no code paths in core sections.
- **FEATURE** answers "what should the user be able to do?". No
  tasks, no implementation details.
- **PLAN** answers "how is it concretely implemented?". Tasks with
  file paths and verify commands live HERE and only here.

### 8. Section policy

Sections are emitted only when they carry decision content. Optional
sections live in this convention (or in the relevant template
comment), not as pre-rendered `TBD` placeholders in the saved
artifact. A FEATURE without ADRs omits the ADR section entirely; it
does not write `## ADRs\n\nTBD`.

This applies to every template under `skills/*/templates/`. Templates
list optional sections in HTML comments at the top so the producing
skill knows what is available; the skill writes a section only when
it has substance.

---

## Three-layer documentation model

Every project organizes its V-Model documentation in three layers. Each
layer has a different update cadence, a different owner, and a
different audience. Mixing layers is the dominant source of doc-vs-
code drift, so the boundaries are binding.

| Layer            | Purpose                                                                                                                      | Lives in                                                                                                                                                  | Owner                                                                                          |
|------------------|------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| Wayfinder        | Concept-to-file lookup, navigational, grep-friendly                                                                          | `src/ARCHITECTURE.map`, JSDoc headers in entry-point files, module READMEs in `src/{module}/README.md`                                                      | Agent in `/coding` (every code edit that creates or renames an entry-point updates this layer) |
| Rule sets        | Stable truths: stack, conventions, design rules, domain glossary. Hard cap 500 lines total.                                  | `_devprocess/rules/technical.md`, `_devprocess/rules/design.md` (only if UI), `_devprocess/rules/domain.md`                                                  | `/architecture`, `/coding`                                                                     |
| Backlog          | Single source of truth for implementation status of every artifact, plus the relation graph (Epic -> Feature -> Plan -> Fix) | `_devprocess/context/BACKLOG.md`                                                                                                                        | Every status-changing skill writes the backlog row BEFORE touching the artifact body            |
| Detail artifacts | Audit trail of the engineering process: BA, Epics, Features, Plans, Fixes, Improvements, ADR detail                          | `_devprocess/analysis/`, `_devprocess/requirements/{epics,features,fixes,improvements,handoff}/`, `_devprocess/architecture/`, `_devprocess/implementation/plans/` | `/business-analysis`, `/requirements-engineering`, `/architecture`, `/coding`                   |

**Status, phase, last-change, and claim of every artifact live in the
backlog row, not in the artifact frontmatter.** Artifact frontmatter
carries identity (`id`, `title`, `created`) and relations (`epic`,
`adr-refs`, `feature-refs`, etc.) only. The backlog is authoritative
for state. This is the structural fix for the most common drift
class (status fields stuck at "Planned" while the code shipped).

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

## Directory Structure

Every project has this base structure. Not all directories are created
upfront, they emerge during the V-Model workflow.

Read `references/directory-structure.md` for the full reference.

### Short overview

```
{project}/
  _devprocess/                    -- Internal knowledge archive (not public)
    analysis/                     -- Flache Ablage: BA-, EXPLORE-, AUDIT-, RESEARCH- (sources/ ist Ausnahme fuer User-Quellen)
    requirements/                 -- Epics, Features, handoff documents
    architecture/                 -- ADRs, arc42
    rules/                        -- Stable rule sets (technical/design/domain), max 500 lines total
    implementation/plans/         -- PLAN-{nn} files
    context/                      -- Backlog, handoffs, metrics
  src/                            -- Source code
    ARCHITECTURE.map              -- Wayfinder: concept | entry-point | adr | how-to-extend
    {module}/README.md            -- Module wayfinder (one per module that owns substance)
  docs/                           -- Public documentation (English)
  scripts/                        -- Build/Deploy/Utility scripts
  memory/                         -- MEMORY.md + reference files
  .claude/                        -- Claude Code configuration
    skills/                       -- Project-specific skills (optional)
  CLAUDE.md                       -- Project-specific context
```

## File Name Conventions

Read `references/naming-conventions.md` for the full reference.

### Short overview

| Artifact | Pattern | Example |
|----------|---------|---------|
| Project-BA (singleton) | `BA-{PROJECT}.md` | `BA-myapp.md` (in `analysis/`) |
| Item-BA Epic | `BA-EPIC-{nn}-{slug}.md` | `BA-EPIC-04-onboarding.md` (in `analysis/`) |
| Item-BA Feature | `BA-FEAT-{ee}-{ff}-{slug}.md` | `BA-FEAT-04-02-magic-link.md` (in `analysis/`) |
| Item-BA Improvement | `BA-IMP-{ee}-{ff}-{nn}-{slug}.md` | `BA-IMP-04-02-01-skip-step.md` (in `analysis/`, optional) |
| Item-BA Fix | `BA-FIX-{ee}-{ff}-{nn}-{slug}.md` | `BA-FIX-04-02-03-link-expiry.md` (in `analysis/`, optional) |
| Exploration Board | `EXPLORE-{PROJECT}.md` | `EXPLORE-myapp.md` (in `analysis/`) |
| Research note | `RESEARCH-{TOPIC}.md` | `RESEARCH-pricing.md` (in `analysis/`) |
| User source | `SOURCE-{name}.{ext}` | `SOURCE-Anforderungen.json` (in `analysis/sources/`) |
| Epic | `EPIC-{nn}-{slug}.md` | `EPIC-01-ai-agent-core.md` |
| Feature | `FEAT-{ee}-{ff}-{slug}.md` | `FEAT-01-01-semantic-search.md` |
| ADR | `ADR-{nn}-{slug}.md` | `ADR-03-embedding-provider.md` |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` | `AUDIT-myapp-2026-03-22.md` (in `analysis/`) |
| Handoff (RE->Arch) | `architect-handoff.md` | Fixed name |
| Handoff (Arch->Code) | `plan-context.md` | Fixed name |
| Backlog | `BACKLOG.md` | Fixed name |
| Fix detail file | `FIX-{ee}-{ff}-{nn}-{slug}.md` | Lives in `_devprocess/requirements/fixes/` |
| Improvement detail file | `IMP-{ee}-{ff}-{nn}-{slug}.md` | Lives in `_devprocess/requirements/improvements/` |
| Handoffs log | `HANDOFFS.md` | Fixed name (append-only) |

Rules: 2-digit numbers (counters), kebab-case slugs, no spaces, no umlauts in file names.

**Epic-scoped feature numbering:** Features are numbered within their
epic, not globally. The format is `FEAT-{ee}-{ff}-{slug}.md`
where `EPIC` is the 2-digit epic number (identical to the number in
the epic's filename) and `NNN` is the 2-digit feature counter local
to that epic. Examples:

- EPIC-01 -> FEAT-01-01, FEAT-01-02, FEAT-01-03, ...
- EPIC-02 -> FEAT-02-01, FEAT-02-02, ...
- EPIC-13 -> FEAT-13-01, FEAT-13-02, ...

This keeps epic and feature traceable via the filename alone, makes
parallel epic work conflict-free (two epics can each start at
FEATURE-{EPIC}-001), and keeps alphabetical sort order stable.

### The `_devprocess/context/` files

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
  body. Every skill that touches project state also touches this file.
- **`HANDOFFS.md`** -- the phase handoffs log. Append-only. Each phase
  skill writes one entry at the end of its run with: artifacts produced,
  handoff context (open questions, assumptions, risks), and next phase.
  Used by the next skill to pick up context without re-reading all artifacts.
- **`METRICS.md`** -- signal layer (cycle time, drift count, hypothesis
  validation, phase transitions, mid-course trigger counts). Populated
  by `/coding`, `/business-analysis`, `/dia-guide`. See
  `skills/dia-guide/templates/METRICS-TEMPLATE.md`.

FIX and IMP detail files live under
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` and
`_devprocess/requirements/improvements/IMP-{ee}-{ff}-{nn}-{slug}.md`
(parallel to `epics/` and `features/`). Status, phase, claim, and
commit SHA live in the backlog row, not in the file's frontmatter.

### `_devprocess/analysis/` layout rule

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
provided source documents (specifications, glossaries, RFP drafts,
PDFs the user wants to keep as project context). Files in
`sources/` use a `SOURCE-{name}.{ext}` prefix and are read-only from
the skill's perspective. Skills never write into `sources/`; only
the user copies files there.

This layout is the post-flatten target of `dia-migration` Phase 4
and supersedes the earlier `analysis/security/` subfolder.

## Writing style for every artifact

Every artifact produced by any V-Model skill (BA, EXPLORE, EPIC,
FEATURE, ADR, arc42, plan-context, architect-handoff, backlog rows,
bug-log entries, handoff-log entries, security-audit reports, release
notes, CHANGELOG) follows the same writing rules. The rules apply to
the prose the skill writes at runtime, not only to the templates.

**No em dashes, ever.** No Unicode em dash (U+2014), no en dash
(U+2013), no double-hyphen substitute written as two ASCII hyphens.
Use a period, a comma, parentheses, or a plain "and" or "but". The
user has explicitly said they hate em dashes. Every single one is a
regression.

**No AI writing tells.** These patterns leak into machine-generated
prose and have to be avoided on purpose:

- No negative parallelisms. Skip "not X but Y", "it is not about A,
  it is about B", "more than just X". State the positive form.
- No rule-of-three padding. If a default list has three parallel items,
  drop to two, add a fourth, or rewrite.
- No AI vocabulary: landscape, nuanced, delve, leverage, utilize,
  intricate, crucial, pivotal, robust, seamless, game-changing,
  revolutionary, unlock, empower, comprehensive, holistic, foster,
  ensuring, highlighting, underscoring, emphasizing, reflecting,
  symbolizing.
- No inflated symbolism ("at its core", "fundamentally", "the real
  question is", "this matters because").
- No copula avoidance. Write "X is Y", not "X serves as Y" or "X
  stands as Y".
- No promotional language. No boasting adjectives.
- No vague attributions ("it is often said", "many believe", "experts
  argue") unless a specific source is named.
- No filler phrases ("in order to", "it is important to note", "needless
  to say", "due to the fact that").
- No superficial -ing phrases ("highlighting the importance of X",
  "reflecting the commitment to Y") tacked onto sentences to fake depth.
- No title case in headings. Sentence case only.
- No meta-signposting ("let me break this down", "here is what you need
  to know"). Just write the content.
- Active voice by default.

**Grep before you save.** Before writing an artifact, the skill runs a
mental grep for U+2014, U+2013, the double-hyphen substitute, and the
forbidden vocabulary words ("crucial", "delve", "landscape", "foster",
"nuanced"). Any hit gets rewritten. This applies whether the artifact
is brand new, an edit, or a promotion from draft to validated.

**Templates follow the same rule.** Every `skills/*/templates/*.md`
file is held to the same standard. When a skill copies a template into
`_devprocess/`, it copies the clean version, and any prose it fills
into the placeholders is written in the same style.

## Language Conventions

| Context | Language |
|---------|----------|
| Conversation with user | User's language (agent adapts automatically) |
| Commit messages | English, conventional prefixes (feat/fix/chore/docs/refactor) |
| Private documentation (`_devprocess/`) | **Match the user's chat language** |
| Public documentation (`docs/`, `README`) | English |
| Code, identifiers, variables | English |
| Skill files (`SKILL.md`) | English (user language adapts in dialog) |

**Artifact language (binding):** every skill produces the documents
under `_devprocess/` (BA, EPIC, FEATURE, ADR, arc42, plan-context,
architect-handoff, backlog rows, bug-log entries, handoff-log entries,
audit reports, release notes, FIX, IMP) in the language the user
uses in chat. A language switch by the user pulls subsequent
artifacts; existing artifacts are not auto-translated. On ambiguity
(mixed DE/EN, very short first turn), the skill asks one short
question before the first artifact:

> "Which language should the artifacts use, German or English?"

Excluded from this rule: code, identifiers, commit messages, `docs/`,
`README`, skill files, and English keyword fields (frontmatter keys,
template placeholders, technical terms such as `status`, `phase`,
`Epic`, `Feature`, `ADR`, `Refs`).

**Note:** Skills are written in English so they are portable across
languages, but when a skill runs and talks to the user, the agent
switches to the user's language. See
`skills/dia-bootstrap/SKILL.md`.

## Feature Lifecycle

Every feature goes through:

```
1. BACKLOG ROW      -- Create row in _devprocess/context/BACKLOG.md
                       FIRST. Status=Ready, Phase=Building, Refs={Epic}.
2. CLAIM            -- Set Claim column to {pair-id} @ {date}
3. FEATURE-SPEC     -- Write the substance (description, SC, NFRs)
                       AFTER the row exists. No status field in
                       frontmatter.
4. PLAN             -- Persist agent's plan as PLAN-{nn}, append PLAN-{nn}
                       to the feature's Refs column in backlog
5. IMPLEMENTATION   -- Code, build, test after each step. Backlog row
                       reflects status (Active -> Review).
6. SPEC UPDATE      -- Feature spec stays the substance reference
                       (success criteria verified, NFRs honored). Code
                       paths NEVER added to the spec.
7. WAYFINDER UPDATE -- New entry-point landed: update
                       src/ARCHITECTURE.map and write the JSDoc header
8. BACKLOG UPDATE   -- Status=Done, commit SHA, claim cleared
```

See the Concurrent-agent coordination section in
`skills/dia-guide/SKILL.md` for the Claim protocol and
conflict-resolution rules when multiple pairs work in parallel.

## Plan Structure

Every non-trivial plan has:

1. **Context** -- Diagnostic, not descriptive. Root-cause analysis
2. **Changes** -- Per file one subsection, BEFORE/AFTER code blocks
3. **File summary** -- Table (File | Change | Risk)
4. **Not affected** -- Explicit list of UNCHANGED files (blast radius)
5. **Verification** -- Acceptance criteria, build always step 1

## Git Workflow

- Dual-remote: private (origin, all branches) + public (only main)
- Branch flow: `feature/*` -> `dev` -> `main` -> `public/main`
- Safe-merge: merges to dev via `scripts/merge-to-dev.sh`
- Commits: conventional prefixes, Co-Authored-By Claude
- Two-stage stripping for public (dev tooling, then internal docs)

## Debugging Conventions

Bugs as causal chains:
```
Problem: [observable behavior]
Root Cause: [why it happens]
Chain: step 1 -> step 2 -> ... -> error
```

Bug IDs: `FIX-{ee}-{ff}-{nn}` (P0 = immediate, P1 = short-term, P2 =
medium-term, where `{ee}` = parent epic, `{ff}` = parent feature,
`{nn}` = bug counter local to that feature). Security findings:
`H-N` / `M-N` / `L-N` (High/Medium/Low).

All bugs discovered during `/coding` (or surfaced by the user
mid-flow) land as a FIX-{ee}-{ff}-{nn} row in
`_devprocess/context/BACKLOG.md` with priority, plus a detail file at
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`
carrying symptom, root cause (causal chain), fix, and regression
test. There is no separate bug-log file.

## Memory Conventions

- `CLAUDE.md` (global `~/.claude/`): HOW we work (cross-project)
- `CLAUDE.md` (project-root): project-specific context
- `memory/MEMORY.md`: key facts, short references (< 200 lines)
- Detailed references: separate files, linked from MEMORY.md
- Update existing entries instead of creating new ones
- Actively delete outdated entries

## Initializing a Project

When setting up a new project, create this base structure:

```bash
mkdir -p _devprocess/{analysis/sources,requirements/{epics,features,fixes,improvements,handoff},architecture,rules,implementation/plans,context}
mkdir -p src docs scripts memory
```

And create the initial files:
- `_devprocess/context/BACKLOG.md` -- seeded from
  `skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`
  with the project name filled in and empty dashboard counts
- `_devprocess/context/HANDOFFS.md` (empty handoffs log)
- `_devprocess/rules/technical.md` -- seeded from
  `skills/architecture/templates/RULES-TECHNICAL-TEMPLATE.md`
- `_devprocess/rules/design.md` (only if the project has UI surface) --
  seeded from `skills/architecture/templates/RULES-DESIGN-TEMPLATE.md`
- `_devprocess/rules/domain.md` -- seeded from
  `skills/architecture/templates/RULES-DOMAIN-TEMPLATE.md`
- `src/ARCHITECTURE.map` -- seeded from
  `skills/architecture/templates/ARCHITECTURE-MAP-TEMPLATE.md`. Empty
  rows initially; `/coding` and `/architecture` populate it as
  entry-points appear.
- `CLAUDE.md` (project context template)
- `memory/MEMORY.md` (empty memory template)

## Keywords
Project structure, conventions, init, project setup, directory structure,
naming conventions, coding standards, way of working
