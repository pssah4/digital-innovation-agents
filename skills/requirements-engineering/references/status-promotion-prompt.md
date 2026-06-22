# Parent BA status promotion (full prompt)

This is the verbatim AskUserQuestion text used by `/requirements-engineering`
when the parent BA is still at Draft after a successful handoff. The skill
links here; the SKILL.md keeps only the short summary.

## When the prompt fires

Parent BA resolution order:

1. `ba-ref:` in the new EPIC / FEAT artefact frontmatter (preferred,
   written by RE during this run).
2. `source-ba:` in `_devprocess/requirements/handoff/architect-handoff.md`.
3. The matching Item-BA file in `analysis/` whose ID corresponds to the
   new item (`BA-EPIC-{nn}-{slug}.md` for `EPIC-{nn}`,
   `BA-FEAT-{ee}-{ff}-{slug}.md` for `FEAT-{ee}-{ff}`).
4. The Project-BA `_devprocess/analysis/BA-{PROJECT}.md` if it is the
   only BA in the project.

If no parent BA can be located unambiguously, skip silently and log a
one-line notice in the artifact report
(`Parent BA: not located, status promotion skipped`). Do not block the
handoff.

## AskUserQuestion payload

Fire only when the BA frontmatter `status:` is `Draft` or
`Draft (reverse-engineered, ...)`.

> Title: "Promote parent BA status?"
> Question: "RE derived Epics, Features, and an architect-handoff
> from `BA-{NAME}.md`. The BA is still marked Draft. Promote it to
> Validated as part of this handoff?"
>
> Options (each with Pro/Con per User Interaction Protocol):
> 1. (Recommended) Promote to Validated
>    + Pro: BA exercised end-to-end through RE, status reflects
>      reality, downstream readers see a content-bearing artifact.
>    - Con: marks the BA as validated even if you have not personally
>      walked every section since the co-creation dialog.
> 2. Keep Draft
>    + Pro: explicit walkthrough via `/business-analysis` Validation
>      Mode happens later; status change stays manual.
>    - Con: BA stays at Draft while its derived Epics and Features
>      are already in flight; later readers must guess the BA's
>      reliability.
> 3. Other (free text)

## Apply on option 1

Update BA frontmatter:

```yaml
status: Validated
validated-by: /requirements-engineering on {YYYY-MM-DD}
validated-via: handoff (Epics + Features + architect-handoff)
```

Append a row to the BA's `## Validation Log` section (create the section
if it does not exist, place it after the Executive Summary):

```
| {YYYY-MM-DD} | /requirements-engineering | Validated through RE handoff: {N} epics, {M} features, architect-handoff at `_devprocess/requirements/handoff/architect-handoff.md` |
```

Keep `created-by:` and `reverse-engineering-provenance:` (if set) in
place as historical record.

## Apply on option 2 or 3

Leave the BA frontmatter untouched. Note the decline in the artifact
report (`Parent BA status: kept at Draft per user request`).

## On Validated or other non-Draft

Skip silently. No prompt, no edit. Idempotent on later runs.

## Artifact report lines

Pick one of the four:

- `Parent BA: BA-{NAME}.md, promoted Draft -> Validated`
- `Parent BA: BA-{NAME}.md, kept at {status} per user request`
- `Parent BA: BA-{NAME}.md, already at status {status} (no change)`
- `Parent BA: not located, status promotion skipped`

## Companion: invariant N-17

`/consistency-check` Mode A enforces N-17 (status coherence between
parent artifacts and their downstream evidence). The RE-side promotion
is the proactive path; N-17 is the safety net if the promotion was
declined or skipped, or if the BA was edited out-of-band.
