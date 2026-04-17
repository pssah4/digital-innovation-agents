---
title: Artifact Ownership Matrix
description: Which skill writes which file, which skill reads it, and how artifacts flow through the V-Model.
---

# Artifact Ownership Matrix

Every skill produces durable artifacts under `_devprocess/` in the
user's project. This document is the shared map of **who writes
what, and who reads it**. Two skills must never claim to own the same
file -- when they do, one of them loses edits the other made.

## Ownership principles

1. **One writer per file.** A file has exactly one owning skill. Other
   skills may read it, and may append via a clearly labelled section,
   but the owner is responsible for structure and consistency.
2. **Downstream reads, never mutates.** If `requirements-engineering`
   reads the BA document, it does not edit it. If it needs to amend
   something, it raises that back to `business-analyse`.
3. **Writeback is explicit.** The `coding` skill updates design
   artifacts (ADRs, plan-context, feature specs) when implementation
   reveals the design needs to change. This is the one exception to
   the "downstream reads, never mutates" rule, and it exists because
   implementation is where reality meets intent.
4. **Templates never get edited in place.** `templates/` files under
   `skills/<phase>/` are scaffolds. The skill copies a template into
   `_devprocess/` and edits the copy.

## The matrix

| Artifact (under `_devprocess/`) | Owner | Readers | Notes |
| --- | --- | --- | --- |
| `00_project/PROJECT.md` | `project-conventions` | all | Ground truth for project name, dirs, naming |
| `01_business-analysis/BA-{PROJECT}.md` | `business-analyse` | `requirements-engineering`, `v-model-workflow`, `reverse-engineering` | Personas, HMW, value prop, hypotheses |
| `01_business-analysis/method-cards/*.md` | `business-analyse` | `business-analyse` (next iteration) | One card per innovation method run |
| `02_requirements-engineering/epics/EPIC-*.md` | `requirements-engineering` | `architecture`, `coding`, `testing` | One file per epic |
| `02_requirements-engineering/features/FEATURE-*.md` | `requirements-engineering` | `architecture`, `coding`, `testing`, `security-audit` | One file per feature |
| `02_requirements-engineering/architect-handoff.md` | `requirements-engineering` | `architecture` | Summary for the architect |
| `03_architecture/ADR-*.md` | `architecture` | `coding`, `testing`, `security-audit` | MADR format |
| `03_architecture/arc42.md` | `architecture` | `coding`, `testing`, `security-audit` | arc42 skeleton |
| `03_architecture/plan-context.md` | `architecture` | `coding` | Context bridge to the implementation agent |
| `04_coding/implementation-notes.md` | `coding` | `testing`, `security-audit` | What actually shipped vs. what was designed |
| Updates to `03_architecture/*` during implementation | `coding` (writeback) | `architecture` (review sync) | See principle 3 |
| `05_testing/test-plan.md` | `testing` | `security-audit` | Scope and coverage decisions |
| `05_testing/results/*.md` | `testing` | `security-audit` | Run logs, not the code-under-test |
| `06_security-audit/findings-*.md` | `security-audit` | `coding` (for fixes) | Prioritised, with remediation plan |
| `06_security-audit/remediation-plan.md` | `security-audit` | `coding` | What to fix in which order |

Numbers in the directory names match the V-Model phases; they make the
order obvious when browsing the filesystem.

## Orchestrators and bootstrap skills

These skills do not own phase-scoped artifacts. They read them all.

| Skill | What it reads | What it writes |
| --- | --- | --- |
| `v-model-workflow` | every phase artifact | nothing -- it dispatches |
| `using-digital-innovation-agents` | nothing | nothing -- orientation only |
| `reverse-engineering` | the codebase and existing docs | the full `_devprocess/` tree, marked as reverse-engineered |

`reverse-engineering` is the exception: it is the only skill that
legitimately writes into phases it does not own. Its outputs are
marked "reverse-engineered" so downstream runs can tell the difference
between a reverse-engineered BA and one that came from interviews.

## When skills need to share state

Use explicit handoff files, not shared ones:

- `architect-handoff.md` is RE's last word to the architect, not a
  shared scratch pad.
- `plan-context.md` is the architect's last word to the implementer.
- `implementation-notes.md` is the implementer's last word back up the
  V.

If you find yourself wanting a file that two skills both write, the
usual fix is to split it into two files (one each) and have the
reader concatenate mentally.

## Working around ownership

Sometimes a skill legitimately needs to annotate a file it does not
own. The convention is a labelled append-only section at the end of
the file:

```markdown
<!-- begin: security-audit annotations -->
- finding SEC-2026-001 affects Feature FEAT-017
- finding SEC-2026-014 affects Feature FEAT-023
<!-- end: security-audit annotations -->
```

The owning skill preserves these sections on regeneration. If that
contract is too heavy, it is a sign the information belongs in the
annotating skill's own artifact instead.

## Evolving the matrix

This table is the single source of truth. When you add a skill or
change an artifact path:

1. Update the matrix in this file.
2. Update the affected skills to match.
3. Note the change in `CHANGELOG.md` (see
   [versioning](./versioning.md) for classification).
