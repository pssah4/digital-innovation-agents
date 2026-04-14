---
title: Artifacts
description: The _devprocess/ directory structure and the files every phase produces.
---

# Artifacts

Every V-Model phase produces artifacts that feed the next phase. All
user-project artifacts live under `_devprocess/` in the user's project
repository (not in this plugin's repo).

## Directory tree

```
_devprocess/
  analysis/
    BA-{PROJECT}.md                    Phase 1: Business Analysis
    EXPLORE-{PROJECT}.md               Phase 1: Exploration Board (PoC/MVP)
    security/
      AUDIT-{PROJECT}-{YYYY-MM-DD}.md  Phase 6: Security Audit report
  requirements/
    epics/
      EPIC-{NNN}-{slug}.md             Phase 2: Epic spec
    features/
      FEATURE-{EPIC}-{NNN}-{slug}.md   Phase 2: Feature spec (epic-local)
    handoff/
      architect-handoff.md             Phase 2 -> 3: aggregated ASRs + NFRs
      plan-context.md                  Phase 3 -> 4: tech stack + integrations
  architecture/
    ADR-{NNN}-{slug}.md                Phase 3: Architecture Decision Record
    arc42.md                           Phase 3: arc42 documentation
  context/
    10_backlog.md                      Single source of truth for project state
                                       (per BACKLOG-TEMPLATE.md)
    20_bugs.md                         FIX-NN bug log (/coding Phase 3c)
    30_handoffs.md                     Append-only phase handoffs log (all phases)
```

## Living Documents

Artifacts are **not one-off specifications**. They are continuously
updated during and after implementation. At the end of a V-Model cycle,
every artifact reflects the actually-implemented state, not the
originally-planned state.

For example, an ADR proposal created in Phase 3 may be modified in
Phase 4 (Critical Review) when `/coding` finds that the proposal
doesn't match the existing codebase. The ADR file is updated in place
with `Status: Accepted (modified by review)` and the justification for
the change. See [Living Documents](../concepts/living-documents).

## The three context files

`10_backlog.md`, `20_bugs.md`, and `30_handoffs.md` serve different
purposes:

- **`10_backlog.md`**: living backlog and **single source of truth
  for the project state**. Follows the binding format in
  [`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md):
  dashboard on top, entries grouped by Epic (BL-NNN rows with status,
  priority, Feature-Spec, ADR, source, commit), standalone items for
  epic-free findings, a reference list of open bugs, deferred items.
  Every phase skill that changes project state updates this file in
  the same edit pass (new row, status transition, dashboard refresh).
- **`20_bugs.md`**: FIX-NN bug log. Every bug found during `/coding`
  Phase 3c (Debugging Protocol) gets an entry with causal chain and
  priority. Resolved bugs carry the commit SHA and regression-test
  verification status.
- **`30_handoffs.md`**: append-only phase handoffs log. Each phase
  skill appends one entry at the end of its run with artifacts produced,
  handoff context (open questions, assumptions, risks), and the next
  phase.

The numbering (`10_`, `20_`, `30_`) leaves room for future additions.

## Traceability chain

```
BA document (Why?)
  -> Epic (What, strategic?)
    -> Feature (What, concrete?)
      -> ASR (What is architecture-relevant?)
        -> ADR (How do we solve it?)
          -> plan-context.md (Context bridge)
            -> Critical Review (Does it fit the codebase?)
              -> Code (Implementation)
                -> Tests (Does it work?)
                  -> Security Audit (Is it safe?)
                    -> Release Closure (Close the cycle)
```

Every step writes back into the source artifacts so the chain is never
broken.

## Project initialization

When starting a new project, initialize the structure:

```bash
mkdir -p _devprocess/{analysis/security,requirements/{epics,features,handoff},architecture,context}
touch _devprocess/context/20_bugs.md _devprocess/context/30_handoffs.md
cp skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md \
   _devprocess/context/10_backlog.md
```

`10_backlog.md` is seeded from the template (not created empty) so
the first write already follows the binding format. Replace
`{PROJECT}` in the header with the actual project name.

The `/project-conventions` skill runs this for you if you invoke it.

## See also

- [Conventions](./conventions): naming rules and language conventions
- [V-Model concept](../concepts/v-model): why this structure
- [Living Documents concept](../concepts/living-documents)
