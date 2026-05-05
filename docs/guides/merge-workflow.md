---
title: Merge workflow
description: How DIA prevents id collisions when parallel feature branches independently allocate the same EPIC, FEAT, IMP, or FIX number.
---

# Merge workflow: id alignment before merge

When two feature branches each allocate `EPIC-04` (or `FEAT-04-02`,
`FIX-04-02-01`, `IMP-04-02-01`) without knowing about each other,
merging the second branch into `dev` produces an id collision.
Without a fix, the artifact graph becomes inconsistent: two epics
share an id, two features point at the same parent, the backlog
shows duplicates.

DIA solves this with three cooperating components, all installed
once via `tools/install-git-hooks.sh`.

## The three components

| Component | File | Role |
|---|---|---|
| Renumber engine | `tools/renumber-for-merge.py` | Reads target backlog, computes mapping, applies renames + reference updates |
| Wrapper | `scripts/merge-to-dev.sh` | Renumbers source branch, commits `chore(renumber)`, then merges |
| Safety net | `tools/git-hooks/pre-merge-commit` | Blocks direct `git merge` if duplicate ids land in the working tree |

## Installation

In the target project, run once:

```bash
bash <DIA-repo>/tools/install-git-hooks.sh
```

This installs both hooks (`pre-commit` and `pre-merge-commit`)
under `.git/hooks/` and copies the renumber engine to
`.git/hooks-data/renumber-for-merge.py`.

## Canonical path: through the wrapper

```bash
bash scripts/merge-to-dev.sh <source-branch> [<target-branch>]
# Default target: dev
```

The wrapper:

1. Snapshots `<target>` to `<target>-backup` (lightweight branch
   for one-step rollback).
2. Switches to the source branch.
3. Runs `tools/renumber-for-merge.py --target <target> --check-only`.
4. If collisions exist: applies the renumber and auto-commits
   `chore(renumber): align ids with <target> before merge`.
5. Switches to the target branch.
6. Runs `git merge --no-ff <source-branch>`.

The renumber commit lands on the **source** branch, so the audit
trail of "what changed" is clean: one commit shows exactly which
ids were shifted before the merge.

Rollback if needed:

```bash
git checkout <target>
git reset --hard <target>-backup
```

## Direct merge: what happens then?

```bash
git checkout dev
git merge --no-ff feature/foo
```

The `pre-merge-commit` hook scans the working tree (post-merge)
for two artifact files carrying the same id. On hit it exits 1,
the merge commit is not created, and the user sees:

```
Merge blocked: id collisions between the merging branch and dev.

Use the canonical merge path so ids are renumbered on the source
branch before the merge:

    git merge --abort
    git checkout <source-branch>
    bash scripts/merge-to-dev.sh <source-branch> dev

If you really know what you are doing: bypass with --no-verify.
```

`git merge --no-verify` skips the hook for legitimate edge cases
(hotfix that must keep its id), but should not be the default.

## What gets renumbered

The renumber maps `old-id -> new-id` and rewrites everywhere the
old id appears:

- **File names** in `_devprocess/requirements/{epics,features,fixes,improvements}/`
- **File names** of the corresponding Item-BAs in
  `_devprocess/analysis/BA-{EPIC,FEAT,IMP,FIX}-*.md`
- **Frontmatter fields**: `id`, `epic`, `feature`, `ba-ref`,
  `depends-on`, `feature-refs`, `adr-refs`, `supersedes`,
  `superseded-by`, `target-id`, `parent-feat`
- **Body refs** in every `*.md` under `_devprocess/`
- **`src/ARCHITECTURE.map`** (wayfinder)
- **`FIXME(stub):` markers** in the source tree (per
  graph-invariants E-14)

**Not renumbered:**

- ADR and PLAN ids (they have their own numbering, semantically
  decoupled from the EPIC/FEAT graph)
- `_devprocess/context/HANDOFFS.md` (append-only audit trail)

## Mapping rule

For each class, the next free id is computed from the **target**
branch's `BACKLOG.md` (read via `git show <target>:_devprocess/context/BACKLOG.md`):

- **EPIC**: `max(target.EPIC) + 1`
- **FEAT**: epic-local; `ee` from the EPIC mapping, `ff` is the
  next free counter inside the new epic
- **IMP / FIX**: feature-local; `ee` and `ff` from the FEAT
  mapping, `nn` is the next free counter inside the new feature

The order of operations is deterministic: EPIC first, FEAT next
(propagating the EPIC remap), IMP and FIX last (propagating the
FEAT remap). Every source id has exactly one target id.

## Modes of `tools/renumber-for-merge.py`

| Mode | Purpose |
|---|---|
| `--check-only` | Exit 1 if collisions exist, else 0. No output. Used by hooks. |
| `--list-conflicts` | Prints the mapping as JSON. No file changes. |
| `--dry-run` | Computes mapping, prints plan, writes nothing. |
| `--check-tree-duplicates` | Scans the working tree for two files with the same id. The pre-merge-commit hook uses this mode. |
| `--source-ref <ref>` | Read source ids from a git ref instead of the working tree. Combine only with the read-only modes above. |
| (default) | Computes mapping, applies renames + updates. |

## Edge cases

**Same id on both sides, identical file.** No collision, no
rename. Common when both branches share a common upstream commit
that introduced the artifact.

**`BACKLOG.md` three-way conflict.** A normal markdown merge
conflict, orthogonal to the id collision. Resolve manually after
the renumber. Tip: keep the source branch up to date with `git
rebase <target>` before running the wrapper, so `BACKLOG.md` is
not in conflict at merge time.

**Source branch without `_devprocess/`.** Script prints "No
`_devprocess/` found; nothing to renumber" and exits 0. Hook lets
the merge through.

**Multiple parallel feature branches.** Each merge handles only
the branch being merged. Other branches stay untouched and may
need their own renumber when they merge later.
[`/dia-migration` Phase 8](./dia-migration#what-it-does) and
[`/reverse-engineering` Phase 6.5](./reverse-engineering#phase-6-5-parallel-branch-alignment-advisory)
list all parallel branches with collision status, so the
maintainer can plan ahead.

## Test the workflow

Manual end-to-end verification:
[`tools/test-merge-hook.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/tools/test-merge-hook.md)
on GitHub. Five scenarios against a temp repo under `/tmp`:

1. Direct merge is blocked by the hook
2. Wrapper renumbers and merges through cleanly
3. Idempotency (second run is no-op)
4. FEAT and FIX renaming including body refs
5. Mode self-test (`--list-conflicts`, `--check-only`,
   `--dry-run`, `--check-tree-duplicates`)

## Bypass rules

- `git merge --no-verify` skips the `pre-merge-commit` hook.
  Acceptable for: a deliberate hotfix that must keep its id (for
  example, an external tracker references the id literally).
- There is no environment-variable override for the script. The
  explicit hook bypass is the only escalation path.

## Known stumbling blocks

- `pre-merge-commit` only fires for actual merge commits, not for
  fast-forward merges. If the source branch is directly ahead of
  the target tip, no hook runs. Force a real merge commit with
  `git merge --no-ff` or use `scripts/merge-to-dev.sh`.
- `MERGE_HEAD` is not reliably present at the `pre-merge-commit`
  point (depends on merge strategy and git version). The hook
  uses `--check-tree-duplicates` instead, which sees two files
  with the same id directly in the working tree.
- macOS bash 3.x works, but `set -e` interactions inside `if !`
  constructs can be subtle. To debug a hook problem: run
  `bash -x .git/hooks/pre-merge-commit` after a `git merge --no-commit`
  to inspect the trace.

## Read the source

Tool source on GitHub:

- [`tools/renumber-for-merge.py`](https://github.com/pssah4/digital-innovation-agents/blob/main/tools/renumber-for-merge.py)
- [`tools/git-hooks/pre-merge-commit`](https://github.com/pssah4/digital-innovation-agents/blob/main/tools/git-hooks/pre-merge-commit)
- [`scripts/merge-to-dev.sh`](https://github.com/pssah4/digital-innovation-agents/blob/main/scripts/merge-to-dev.sh)
- [`tools/install-git-hooks.sh`](https://github.com/pssah4/digital-innovation-agents/blob/main/tools/install-git-hooks.sh)

Skill integrations:

- [`/dia-migration` Phase 8](./dia-migration#what-it-does)
- [`/reverse-engineering` Phase 6.5](./reverse-engineering#phase-6-5-parallel-branch-alignment-advisory)
