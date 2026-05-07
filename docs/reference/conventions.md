---
title: Conventions
description: Naming rules, language conventions, the three-layer documentation model, commit style, and git workflow.
---

# Conventions

## Three-layer documentation model

Every project organises its V-Model documentation in three layers.
Each layer has a different update cadence, a different owner, and a
different audience. Mixing layers is the dominant source of doc-vs-
code drift, so the boundaries are binding.

| Layer | Purpose | Lives in | Owner |
|---|---|---|---|
| Wayfinder | Concept-to-file lookup, navigational, grep-friendly | `src/ARCHITECTURE.map`, JSDoc headers in entry-point files, module READMEs in `src/{module}/README.md` | `/coding` (every code edit that creates or renames an entry-point updates this layer) |
| Rule sets | Stable truths: stack, conventions, design rules, domain glossary. Hard cap 500 lines total. | `_devprocess/rules/technical.md`, `_devprocess/rules/design.md` (only if UI), `_devprocess/rules/domain.md` | `/architecture`, `/coding` |
| Backlog | Single source of truth for implementation status of every artifact, plus the relation graph (Epic -> Feature -> Plan -> Fix). | `_devprocess/context/BACKLOG.md` | Every status-changing skill writes the backlog row BEFORE touching the artifact body |
| Detail artifacts | Audit trail of the engineering process: BA, Epics, Features, Plans, Fixes, Improvements, ADR detail. | `_devprocess/analysis/`, `_devprocess/requirements/{epics,features,fixes,improvements,handoff}/`, `_devprocess/architecture/`, `_devprocess/implementation/plans/` | `/business-analysis`, `/requirements-engineering`, `/architecture`, `/coding` |

**Status, phase, last-change, and claim of every artifact live in the
backlog row, not in the artifact frontmatter.** Artifact frontmatter
carries identity (`id`, `title`, `created`) and relations (`epic`,
`adr-refs`, `feature-refs`) only.

**ADR abstraction rule.** ADR core sections (Context, Decision Drivers,
Considered Options, Decision, Consequences) contain no code paths,
file names, line numbers, or method signatures. Code-level hints
belong in the optional `## Implementation Notes` appendix at the
bottom, which is allowed to go stale. The wayfinder is the canonical
source for current paths.

See the [Three-layer documentation model](../concepts/three-layer-documentation)
concept page for the full rationale.

## File naming

| Artifact | Pattern | Example |
|---|---|---|
| Project-BA (singleton) | `BA-{PROJECT}.md` | `BA-myapp.md` (in `analysis/`) |
| Item-BA Epic | `BA-EPIC-{nn}-{slug}.md` | `BA-EPIC-04-onboarding.md` (in `analysis/`) |
| Item-BA Feature | `BA-FEAT-{ee}-{ff}-{slug}.md` | `BA-FEAT-04-02-magic-link.md` (in `analysis/`) |
| Item-BA Improvement | `BA-IMP-{ee}-{ff}-{nn}-{slug}.md` | `BA-IMP-04-02-01-skip-step.md` (in `analysis/`, optional) |
| Item-BA Fix | `BA-FIX-{ee}-{ff}-{nn}-{slug}.md` | `BA-FIX-04-02-03-link-expiry.md` (in `analysis/`, optional) |
| Exploration Board | `EXPLORE-{PROJECT}.md` | `EXPLORE-myapp.md` (in `analysis/`) |
| Research note | `RESEARCH-{TOPIC}.md` | `RESEARCH-pricing.md` (in `analysis/`) |
| User source | `SOURCE-{name}.{ext}` | `SOURCE-Anforderungen.json` (in `analysis/sources/`) |
| Epic | `EPIC-{nn}-{slug}.md` | `EPIC-01-ai-agent-core.md` |
| Feature | `FEAT-{ee}-{ff}-{slug}.md` | `FEAT-01-01-semantic-search.md`, `FEAT-13-02-reindex-job.md` |
| ADR | `ADR-{nn}-{slug}.md` | `ADR-03-embedding-provider.md` |
| Plan | `PLAN-{nn}-{slug}.md` | `PLAN-04-semantic-search-mvp.md` (in `implementation/plans/`) |
| Fix detail | `FIX-{ee}-{ff}-{nn}-{slug}.md` | `FIX-01-02-03-null-pointer.md` (in `requirements/fixes/`) |
| Improvement detail | `IMP-{ee}-{ff}-{nn}-{slug}.md` | `IMP-01-02-01-cache-warmup.md` (in `requirements/improvements/`) |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` | `AUDIT-myapp-2026-03-22.md` (in `analysis/`, flat) |
| Handoff (RE -> Arch) | `architect-handoff.md` | Fixed name |
| Handoff (Arch -> Code) | `plan-context.md` | Fixed name |
| Backlog | `BACKLOG.md` | Fixed name |
| Handoffs log | `HANDOFFS.md` | Fixed name (append-only) |
| Signal layer | `METRICS.md` | Fixed name (per METRICS-TEMPLATE.md) |
| Wayfinder root | `src/ARCHITECTURE.map` | Fixed name |
| Module wayfinder | `src/{module}/README.md` | One per substantive module |
| Rules (technical) | `_devprocess/rules/technical.md` | Fixed name, hard cap part of 500 lines total |
| Rules (design) | `_devprocess/rules/design.md` | Only if UI surface |
| Rules (domain) | `_devprocess/rules/domain.md` | Fixed name |

**Rules:**

- **2-digit counters** with leading zeros (`01`, `42`, not `1`, `42`,
  not `001`, `042`). Applies to Epic, ADR, Feature epic-prefix and
  feature-counter, Fix counter, Improvement counter, Plan counter.
- **Epic-scoped feature numbering.** Features are numbered within
  their epic, not globally. The format is `FEAT-{ee}-{ff}-{slug}.md`
  where `{ee}` is the 2-digit parent epic number (identical to the
  epic's filename number) and `{ff}` is the 2-digit feature counter
  local to that epic. Example: `EPIC-01` -> `FEAT-01-01`,
  `FEAT-01-02`, ...; `EPIC-13` -> `FEAT-13-01`, `FEAT-13-02`, ...
- **Fix and Improvement scope to a feature.** `FIX-{ee}-{ff}-{nn}` and
  `IMP-{ee}-{ff}-{nn}` reference the parent feature. The `{nn}`
  counter is local to that feature.
- **Plans scope to a feature.** `PLAN-{nn}-{slug}.md` files live in
  `_devprocess/implementation/plans/`. The plan references its
  feature via the `feature` frontmatter field. The plan id is added
  to the feature's `Refs` column in the backlog.
- **kebab-case slugs** (`ai-agent-core`, not `aiAgentCore`)
- **No spaces, no umlauts** in filenames
- **Dates as `YYYY-MM-DD`**
- **Backlog** follows the binding template at
  `skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md` and
  is the single source of truth for project state.

## Required frontmatter

Every detail artifact carries identity and relation fields in
frontmatter. State is read from the backlog row, never from the
frontmatter.

```yaml
---
id: FEAT-01-02
title: Semantic search across vault notes
created: 2026-04-30
epic: EPIC-01
subtype: user-facing  # user-facing | library, default user-facing
adr-refs: [ADR-03, ADR-07]
feature-refs: []
depends-on: [FEAT-01-01]
---
```

Fields:

- `id` (required): the artifact id, matches the filename prefix
- `title` (required): one-line summary
- `created` (required): ISO date
- `epic` (features, fixes, improvements, plans): parent epic id
- `subtype` (features, since v3.2.0): `user-facing` (default, anything
  with a user trigger) or `library` (public API, no end-user trigger).
  Drives the `## Activation Path` requirement and the `/coding`
  Phase 4a steps 6 and 7. FEATUREs without `subtype:` stay valid for
  backwards compatibility; new FEATUREs MUST set it.
- `adr-refs` (features, plans): list of ADRs that apply
- `feature-refs` (plans, fixes, improvements): list of features that
  the artifact relates to
- `depends-on`: graph edges to other artifacts that must be done first

Frontmatter does **not** carry status, phase, last-change, or claim.
Those live in the backlog row.

## Deferred-stub marker (since v3.2.0)

Stubs (no-op handlers, hard-coded placeholders, intentional empty
returns waiting on later wiring or external availability) MUST carry
a `FIXME(stub):` marker AND a paired FIX-row in the backlog.
Bidirectional binding; `/consistency-check` Mode A enforces it via
invariant E-14.

```
// FIXME(stub): <one-line reason> -- see FIX-{ee}-{ff}-{nn}
# FIXME(stub): <one-line reason> -- see FIX-{ee}-{ff}-{nn}
```

- `//` for the C-family (TypeScript, JavaScript, Java, Go, Rust, C#,
  Swift, Kotlin, React TSX/JSX).
- `#` for Python, Ruby, R, shell scripts.

The paired FIX-row in `BACKLOG.md` and its detail file at
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` carry
the context: why the stub is there, what unblocks it, what to do when
it is unblocked. Notes contain `Wiring offen`, `stub`, or
`deferred-stub` so Mode A recognises the stub character. When the
stub is replaced by real implementation, marker AND FIX-row are
cleaned up in the same commit.

## Bug IDs

- `FIX-{ee}-{ff}-{nn}` with priority `P0` (immediate), `P1` (short-term),
  or `P2` (medium-term)
- Example: `FIX-01-02-03 (P1)`: empty array causes null pointer in
  feature parser

Every bug found during `/coding` lands in `_devprocess/context/BACKLOG.md`
as a `FIX-{ee}-{ff}-{nn}` row plus a detail file at
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`. The
detail file contains the causal chain (Problem, Root Cause, Chain of
steps leading to the error, Regression test). Status, commit SHA, and
phase live in the backlog row.

## Pair IDs (concurrent agent coordination)

When multiple human-agent pairs work the same backlog, each pair
identifies itself with a pair-id in the `Claim` column of
`BACKLOG.md`:

- Format: `{human-handle}-{model}`
- Examples: `seb-opus-4-7`, `marie-sonnet-4-6`, `tom-codex`
- Claim cell value: `{pair-id} @ {YYYY-MM-DD}`, for example
  `seb-opus-4-7 @ 2026-04-19`
- Phase skills claim a row at start, release on phase end or `Status: Done`

The backlog itself is the lock. There is no central lock service.

## Security finding IDs

- `H-N` / `M-N` / `L-N`: High / Medium / Low severity
- Example: `H-3`: XSS vulnerability in user-controlled HTML rendering

Audit reports live flat under `_devprocess/analysis/` as
`AUDIT-{PROJECT}-{YYYY-MM-DD}.md`. There is no `analysis/security/`
subfolder anymore.

## Language

| Context | Language |
|---|---|
| Conversation with user | User's language (agent adapts automatically) |
| Commit messages | English, conventional prefixes |
| Private documentation (`_devprocess/`) | Matches user's language |
| Public documentation (`docs/`, README) | English |
| Code, identifiers, variables | English |
| Skill files (`SKILL.md`) | English |

The skill files are written in English so they are portable across
language contexts. The agent automatically switches to the user's
language in dialog.

## Writing style

- No em dashes (U+2014), no en dashes (U+2013). Use periods, commas,
  parentheses, "and", or "but" instead.
- No AI vocabulary: avoid `landscape`, `nuanced`, `delve`, `leverage`,
  `crucial`, `robust`, `seamless`, `holistic`, `foster`, `ensuring`,
  `highlighting`, `underscoring`.
- No negative parallelisms ("not X but Y").
- Active voice, sentence case in headings.
- Correct German umlauts when writing in German: ae, oe, ue, ss only
  if the existing project file is ASCII-only; otherwise proper
  Unicode. Consistent per file.

These rules apply to every artifact, every commit message, every
skill output. The `/humanizer` skill enforces them.

## Commit style

Conventional commits with `Co-Authored-By Claude`:

```
feat: add X
fix: resolve Y
chore: prepare Z
docs: update readme
refactor: restructure W
test: cover scenario V
```

Phase-end commits follow the canonical pattern:

```
{type}({phase}): {ITEM-ID} {phase} complete

Refs: FEAT-01-02, ADR-03
```

Examples:

- `chore(ba): EPIC-01 BA complete`
- `feat(re): FEAT-01-02 RE complete`
- `chore(arch): FEAT-01-02 ARCH complete`
- `feat(code): FEAT-01-02 implementation complete`
- `test: FEAT-01-02 testing complete`

After a phase-end commit, run `tools/github-integration/flow.py
tag-phase --phase {phase}` to attach the `<id>/{phase}-done` tag.

## Git workflow

- **Item branches**: `feature/<ITEM-ID>-<short-slug>`,
  `chore/<ITEM-ID>-<short-slug>`, `feature/audit-<YYYY-MM-DD>`,
  `feature/reverse-engineer-<repo-name>`. The branch is the item.
- **Main branches**: `feature/*` -> `dev` -> `main` -> `public/main`.
- **Safe-merge**: merges to `dev` via `scripts/merge-to-dev.sh` (when
  available).
- **No interactive git commands**: no `git rebase -i`, no `git add -i`.
- **Never amend published commits** without explicit user consent.
- **Two-stage stripping** for public distribution: dev tooling first,
  then internal docs.

## GitHub integration

Phase skills coordinate with GitHub through
`tools/github-integration/flow.py`. Mode-aware: GitHub-only
subcommands are no-ops outside `mode = "github-sync"`.

- `flow.py create-issue --item <ITEM-ID>`: create a tracking issue,
  optionally add to the configured GitHub Project
- `flow.py tag-phase --phase {ba|re|arch|code|test|sec}`: attach
  a `<id>/<phase>-done` tag at the phase-end commit. The release-
  readiness marker `ready-for-review` is the special case: it
  emits `<id>/ready-for-review` without the `-done` suffix
- `flow.py sync-status --item <ITEM-ID>`: mirror BACKLOG Status to
  issue and Project, mirror GitHub Assignee back into the Claim
  column
- `flow.py promote-to-epic --item EPIC-NN [--rename-branch]`:
  rewrite the parent issue, create sub-issues, write the
  Sub-Issues tasklist, optionally rename the feature branch
- `flow.py open-draft-pr --item <ITEM-ID>`: open a draft PR
  against the configured `source_branch`
- `flow.py ready-for-review --item <ITEM-ID> [--with-sec]`:
  flip the draft PR to ready, set the `<id>/ready-for-review`
  tag
- `flow.py validate-fix --item FIX-EE-FF-NN`: hotfix-scoped
  consistency check (local checks always, GitHub-issue check in
  `github-sync`)
- `flow.py apply-renumber --plan FILE`: align GitHub issue titles
  and parent-body Sub-Issues tasklists with a renumber plan;
  invoked from `scripts/merge-to-dev.sh` after the merge

The backlog row is the source of truth for Status; the GitHub
Assignee is the source of truth for Claim; `sync-status` mirrors
both sides.

## Plan structure

Every non-trivial plan follows the same structure and persists as a
`PLAN-{nn}-{slug}.md` file in `_devprocess/implementation/plans/`:

1. **Context**: diagnostic, not descriptive. Root-cause analysis.
2. **Changes**: one subsection per file, BEFORE / AFTER code blocks.
3. **File summary**: table (File | Change | Risk).
4. **Not affected**: explicit list of unchanged files (blast radius).
5. **Verification**: acceptance criteria, build always step 1.
6. **Plan Coverage Gate**: success-criteria coverage map (which SC
   each step closes), ADR alignment (which ADR each decision honours),
   codebase anchoring (each file referenced exists or is named as
   new), verify commands ready to run.

`PLAN-NN` rows in the backlog track Status (Draft / Active / Done),
last-change, and the change log. The plan id is added to the parent
feature's `Refs` column.

## See also

- [Artifacts](./artifacts): full directory tree and artifact catalog
- [Project Conventions guide](../guides/project-conventions): the
  binding skill that owns these rules
- [Commands](./commands): every slash-command and its purpose
- [Three-layer documentation model](../concepts/three-layer-documentation):
  the rationale behind the structural rules above
