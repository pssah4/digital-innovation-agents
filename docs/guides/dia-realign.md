---
title: DIA Realign
description: One entry point for repos that predate current DIA conventions. Detects the repo state, then runs a full reverse walk, a migration script pass, or a gap walk.
---

# DIA Realign

`/dia-realign` is the successor of the retired `/reverse-engineering`
and `/dia-migration` skills. It brings any repo that predates current
DIA conventions in line with them:

- **Brownfield onboarding.** An existing codebase without V-Model
  artifacts gets a full reverse walk: wayfinder, ADRs, arc42
  reference, FEATURE inventory, backlog seed, and an evidence-based
  BA draft.
- **Legacy DIA upgrade.** A project on v1 / v2 conventions (old ID
  schemas, status in frontmatter, `HANDOFFS.md`) gets a script pass
  over `tools/migration/`, then a gap walk for anything missing.
- **Current repo cleanup.** A repo already on current conventions
  gets only the gap walk and the deprecation offers.

One skill, three modes. The skill picks the mode from the repo state
and confirms it with you before writing anything.

## Mode selection via detect_state.py

The mandatory first step runs
`python3 tools/migration/detect_state.py` and picks the mode from the
JSON report:

| Detection result | Mode |
|---|---|
| No `_devprocess/` at all | **A: full reverse walk** |
| Legacy DIA signals: old IDs, `HANDOFFS.md`, v1/v2 layout | **B: script pass, then gap walk** |
| Current artifacts, nothing to migrate | **C: gap walk and deprecations only** |
| Empty repo | Not this skill. Greenfield starts at [`/business-analysis`](./business-analysis). |

Mixed states resolve toward B; the script pass is idempotent, so
running it over partially migrated artifacts is safe.

Every mode starts with a branch check. Mode A runs on
`feature/realign-<repo-name>` (a single multi-item exception: one
branch bootstraps the whole backlog). Modes B and C run on
`chore/dia-realign-<YYYY-MM-DD>`. The skill refuses to run on
`main`, `master`, or `dev`.

## The anti-fabrication contract

This is the most important part of the skill. Code tells you what
exists, not whether it solves the right problem, and the skill
refuses to fill that gap with plausible-sounding fiction.

1. **Source per claim block.** Every claim block carries a `Source:`
   line pointing at concrete evidence:
   - Code: `Source: src/api/auth/handlers.ts:42-58`
   - Docs: `Source: README.md § "Getting Started"`
   - Config: `Source: package.json "dependencies.prisma"`

   The BA draft is stricter: every non-placeholder sentence carries
   a `Source:` line.
2. **No source means placeholder, not guess.** If no evidence can be
   found, the section is marked `[NEEDS USER INPUT. No evidence
   found.]`. The skill does not write a "reasonable assumption" in
   its place.
3. **No persona from code structure.** Routes, directories, and
   endpoint signatures are technical facts, not user research.
   `/users/:id/settings` tells you the system has users; it does not
   tell you who they are. Personas come only from explicit
   statements in the documentation.
4. **No HMW question without an explicit problem statement** in the
   existing documentation.
5. **Provenance marker on every file:** `source: /dia-realign on
   {date}` in frontmatter, plus tolerated draft markers
   (`Anticipated`, `Observed`, `Inferred`, `Draft
   (reverse-engineered)`). The BACKLOG row owns lifecycle status.

Everything produced is draft, observed, inferred, or snapshot.
`/business-analysis` validates the output claim by claim afterwards.

## Mode A: full reverse walk

Walks the V backwards, one phase at a time:

```
Code  ->  Architecture  ->  Requirements  ->  Business Analysis
(facts)   (decisions)      (capabilities)    (Why, draft only)
```

| Phase | Output |
|---|---|
| A1 Scope and codebase scan | Scope tier (Simple Test / PoC / MVP) plus a Codebase Map: manifests, entry points, test setup, CI, existing docs. The only source pool for the rest of the walk. |
| A2 Wayfinder, rules, plan-context | `src/ARCHITECTURE.map`, `_devprocess/rules/` (hard cap 500 lines total), and `plan-context.md` as a 20-line reference index. Lean profile: `SYSTEM-MAP.md` and `decisions/README.md` instead of the rules files. |
| A3 ADRs and arc42 snapshot | One ADR per visible, consequential, non-obvious decision, with `kind: post-hoc` and code paths in `## Sources`. Plus `arc42-REFERENCE.md` (post-code, cap-exempt), only sections with evidence. |
| A4 Epics, FEATURE inventory, SCs | Anticipated epics from capability clusters, one FEAT per observable capability, one observable Success Criterion per capability (`[AWAITING BA]` unless the code declares a deterministic target). |
| A5 BA draft | The 40-line BA template (five questions), filled only from README, docs, manifests, CHANGELOG. Header counts `filled-from-sources` vs. `needs-user-input` so `/business-analysis` knows the remaining work. |
| A6 Backlog seed | TODO/FIXME scan, skipped tests, undocumented env vars, missing coverage, outdated dependencies. Findings are verified against code and docs before filing; survivors become backlog rows with `Source = REV` and evidence links. |

## Mode B: script pass, then gap walk

Mode B runs the migration scripts under `tools/migration/` in
sequence, each step confirmed, committed, and independently
re-runnable:

| Script | Step | Purpose |
|---|---|---|
| `detect_state.py` | 0 | Inventory the repo, classify v1/v2/mixed/brownfield. JSON output. |
| `strip_frontmatter_status.py` | 2a | Remove `status:` / `phase:` / `last_updated:` from frontmatter. |
| `strip_body_status.py` | 2b | Remove body-level `**Status:**` lines. |
| `migrate_naming.py` | 3 | Rename ID schemas (FEATURE-NNNN to FEAT-EE-FF, EPIC-NNN to EPIC-NN), rewrite cross-refs. |
| `flatten_analysis.py` | 4 | Flatten `analysis/` to four prefixes (BA, EXPLORE, RESEARCH, AUDIT). |
| `build_backlog.py` | 5 | Regenerate `BACKLOG.md` from an artifact scan; previous version saved as `BACKLOG.md.preMigration`. |
| `migrate_status_vocabulary.py` | 5b | Map legacy Status values to the GitHub-aligned vocabulary. |
| `migrate_skill_names.py` | 6 | Rewrite legacy skill names to current ones (including the two predecessors of this skill). |
| `shrink_artifacts_v3.py` | 6b | Align existing artifacts with the shrunk templates; dry-run by default, `--apply` to write. |

All scripts take the project root as argument, print a summary, are
idempotent, and exit non-zero on error so the pipeline stops.

Safety contract: dirty tree stops the run, dry-run or plan
confirmation before every destructive step, per-step commits keep
every step reversible via `git reset --hard HEAD`, source code stays
untouched except `src/ARCHITECTURE.map` and optional module READMEs.

After the script pass, the **gap walk** compares the migrated
artifact set against the Mode A output list and runs only the
missing phases (typically wayfinder and rules, observable SCs, and
the BA draft).

## Mode C: gap walk and deprecations

For repos whose artifacts are already current. The skill runs the
gap walk for anything missing, then makes the deprecation offers.
Offers only, never forced; each comes with a "keep as is" option:

- **HANDOFFS.md.** Phase transitions are DIA commit trailers now
  (`DIA-Phase`, `DIA-Handoff`, `DIA-Triage`; see
  [Handoff Rituals](../concepts/handoff-rituals)). The offer:
  prepend a deprecation header and optionally move the file to
  `_devprocess/context/archive/HANDOFFS-legacy.md`. Existing entries
  are never rewritten or deleted.
- **Long-form legacy artifacts.** Pre-v4 long BAs, monolithic
  `arc42.md` files, and prose-style `plan-context.md` files count as
  "legacy format, valid". The split (BA to 40-line core plus
  BA-EXTENDED, arc42 to CONSTRAINTS plus REFERENCE, plan-context to
  the 20-line ref index) is offered only when you ask for it or
  actively rework the artifact.

## Codebase verification gate

Before the handoff ritual, every FEATURE spec and every ADR produced
in Mode A (and every artifact the gap walk touched) gets an explicit
verification against the codebase. This lifts claims from "we wrote
it down" to "we checked it against reality". Each verified file gets
a verification footer; drift findings that are more than a one-line
doc edit become backlog rows. Large projects split the verification
into concurrent agents with non-overlapping file slices.

The Phase A6 findings are verified too: a finding whose target is
already satisfied in the code is closed as `Done` with a note; a
confirmed gap stays in the backlog; an undecidable finding is
escalated. No finding reaches GitHub while it still carries the
`needs verification` marker.

## Quality gates and closing sequence

Before handing off, the skill verifies:

1. Every claim block has a `Source:` line (BA: every sentence).
2. Provenance marker on every file.
3. No invented personas or HMW questions.
4. FEATURE count matches observable capabilities (12 routes is
   neither 4 nor 30 features).
5. Backlog is non-empty for anything but a pristine codebase.
6. Codebase verification footer present on every FEATURE and ADR.

Then: an explicit `/consistency-check` Mode A run, an advisory
parallel-branch alignment scan (`tools/renumber-for-merge.py
--list-conflicts` per unmerged branch, report only; see
[Merge workflow](./merge-workflow)), the artifact report with
counts, and the phase-end commit with DIA trailers:

```
chore(realign): <repo-name> realign complete

<N FEATUREs, M ADRs, BA draft, K backlog rows>

Refs: <repo-name>
DIA-Handoff: <repo-name> -> business-analysis
```

Realign is not a V-phase, so the commit carries no `DIA-Phase`
trailer and sets no phase tag; item-level tags are set later by
`/dia-guide` during the post-realign item promotion.

## Handoff to the forward walk

The transition question offers `/dia-guide` for the item promotion
(issues, tags), then `/business-analysis` in Validation Mode.
`/business-analysis` detects the realigned BA draft automatically
and walks through every `[NEEDS USER INPUT]` marker with you, one
section at a time. Evidence-backed claims get confirmed;
placeholders get filled.

::: info One skill, two directions
The forward and backward walks converge here. Whether the project
started with `/business-analysis` or `/dia-realign`, the BA document
is the same file at the same path, and every phase downstream treats
it identically. Realign is not a side track. It is a seed for the
forward walk.
:::

## Read the skill file

Want to see the exact instructions the agent follows?
[`skills/dia-realign/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/dia-realign/SKILL.md)
on GitHub.

## Further reading

- [Business Analysis guide](./business-analysis). The forward walk takes over here, starting in Validation Mode.
- [Architecture guide](./architecture). The ADR kinds and arc42 split the skill uses.
- [Merge workflow](./merge-workflow). Aligning unmerged branches with the realigned state.
- [V-Model concept](../concepts/v-model). How both entry points feed into the same workflow.
