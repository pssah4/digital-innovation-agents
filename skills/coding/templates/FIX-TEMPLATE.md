<!--
Instructions for the agent: produce this file as
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` when a bug surfaces in
shipped code. Write the prose in the user's working language. Keep
keywords (Symptom, Root cause, etc.) in English so the file greps
consistently.

Status, phase, claim, and last-change live in the backlog row, not in
this file's frontmatter. The frontmatter only carries identity and
relations.

Cap: 30 lines of prose. The deeper analysis lives in
`_devprocess/analysis/` and is linked from here.
-->

---
id: FIX-{ee}-{ff}-{nn}
feature: FEAT-{ee}-{ff}
epic: EPIC-{nn}
adr-refs: []
plan-refs: []
depends-on: []
created: {YYYY-MM-DD}
---

# FIX-{ee}-{ff}-{nn}: {short title}

## Symptom

{What is the observable bad behavior? One paragraph.}

## Root cause

{Why does it happen? Causal chain.}

```
step 1 -> step 2 -> ... -> error
```

## Fix

{What changed in the code, in business terms (not file paths).}

Implementation pointer: see PLAN-{nn} or commit `<sha>` in the
backlog row. ARCHITECTURE.map carries the canonical path for the
affected concept.

## Regression test

{Which test reproduces the bug and locks the fix? Reference the test
file by path; the path may go stale, the backlog row carries the
current commit SHA.}

## Status

See the backlog row for FIX-{ee}-{ff}-{nn} in `_devprocess/context/BACKLOG.md`
(status, phase, claim, commit SHA).
