# RE Handoff Ritual snippets

Verbatim text fragments for the Handoff Ritual run at the end of
`/requirements-engineering`. The SKILL.md keeps the short summary; this
file holds the full text.

## Part 1: Artifact report template

```
Produced / updated:
- _devprocess/requirements/epics/EPIC-*.md: {count} epics
- _devprocess/requirements/features/FEATURE-*.md: {count} features
- _devprocess/requirements/handoff/architect-handoff.md: aggregated input for architect
- _devprocess/context/BACKLOG.md: {count} FIX-{ee}-{ff}-{nn} or IMP-{ee}-{ff}-{nn} entries added, dashboard updated
- ASRs identified: {critical count}, {moderate count}
```

Append one Parent-BA status line per
`references/status-promotion-prompt.md`.

## Part 2: HANDOFFS.md entry

Append a new entry to `_devprocess/context/HANDOFFS.md` with:

- **NFR summary**: key non-functional requirements (Performance, Security,
  Scalability, Availability) with quantified targets
- **Critical ASRs**: architecturally significant requirements that must
  each have an ADR
- **Open architecture questions**: uncertainties the architect should
  resolve (e.g. "should auth be federated or centralized?")
- **Constraints**: budget, timeline, compliance (GDPR, ISO 27001, etc.)
- **Forbidden-terms check**: confirmation that no tech terms leaked into
  Success Criteria (OAuth, REST, PostgreSQL, etc.)

## Part 3: Phase-end commit message

Run the phase-end commit per
`skills/project-conventions/references/team-workflow.md` section
"Phase-end commit (binding)". Canonical message:

```
chore(re): <ITEM-ID> RE complete

<one-line summary: N epics, M features, K success criteria>

Refs: <ITEM-ID>[, additional epic/feature IDs touched]
```

After the commit lands:

```
python3 tools/github-integration/flow.py tag-phase --item <ID> --phase re
python3 tools/github-integration/flow.py sync-status --item <ID>
```

`sync-status` mirrors the BACKLOG Status column to the GitHub issue and
project (and the GitHub Assignee back into the BACKLOG Claim column). It
is a no-op outside `mode = "github-sync"`.

For long RE phases that span days and produce many features,
intermediate commits per cluster of features are encouraged. Each
intermediate commit follows the same template; only the final phase-end
commit gets the `<id>/re-done` tag.

## Promote to Epic (github-sync only)

When the EPIC ID has been assigned for the first time during this RE
phase:

```
python3 tools/github-integration/flow.py promote-to-epic \
  --item EPIC-NN --rename-branch
```

The subcommand:

- renames the parent issue to `EPIC-NN: <title>` and adds the `epic`
  label
- creates one sub-issue per FEAT and IMP that lives under the EPIC in
  the BACKLOG (idempotent, skips existing sub-issues)
- writes a tasklist into the parent body so GitHub tracks the rollup
- renames the current feature branch from `feature/<provisional>` to
  `feature/epic-NN-<slug>` if `--rename-branch` is passed

No-op in `mode = "off"` and `mode = "git-only"`. Skip when the EPIC was
already promoted in a previous session.

## Part 4: Transition AskUserQuestion

> "Requirements are ready. Saved to:
> - Epics: `_devprocess/requirements/epics/`
> - Features: `_devprocess/requirements/features/`
> - Handoff: `_devprocess/requirements/handoff/architect-handoff.md`
>
> Recommended next: `/architecture` -- creates ADR proposals, arc42
> documentation, and plan-context.md.
>
> Shall I start `/architecture` now, or would you like to review the
> requirements first?"

**On agreement** ("yes" / "go" / "next") or inside `/dia-guide`:
-> start `/architecture` and pass the handoff context.

**On rejection** ("no" / "stop" / "I want to check first"):
-> pause and wait for user instruction.
