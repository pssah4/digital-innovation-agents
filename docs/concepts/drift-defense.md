---
title: Drift defense
description: How DIA prevents documentation, specification, and code from drifting apart. The full catalog of drift sources and the mechanism that defends each one.
---

# Drift defense

Documentation rots. Specs go stale. ADRs end up describing yesterday's
codebase. The most expensive failure mode in long-running engineering
projects is not a bug in the code, it is a slow divergence between
what the code does, what the spec says it should do, and what the
documentation claims it does.

DIA names this failure mode **drift** and treats it as a structural
problem to be defended against, not a hygiene issue to be cleaned up
later. This page is the full catalog: every drift source DIA
recognizes and the mechanism that defends each one.

## The catalog

DIA recognizes ten drift sources. They are independent. A project
that defends only one of them still rots through the other nine.

| ID | Drift source | Example |
|---|---|---|
| D1 | Unanchored change | Code edited without any artifact link, no FEATURE / IMP / FIX / ADR ID |
| D2 | Duplicate state | Status field in artifact frontmatter AND in backlog row, both maintained, slowly diverging |
| D3 | Stale code paths in artifacts | FEATURE spec lists `src/login.ts:42`, code refactor moves it to `src/auth/login/index.ts:18`, spec is silently wrong |
| D4 | Code-spec drift during implementation | Plan said X, implementation deviates to Y, spec still says X |
| D5 | Orphan artifacts | FEATURE spec exists, no code references it (or vice versa) |
| D6 | Cross-artifact contradiction | Two ADRs cover overlapping decisions with conflicting outcomes |
| D7 | Build / test drift | Code shipped, lint or tests are red, nobody noticed |
| D8 | Stale frontmatter status | ADR frontmatter says `Proposed`, the decision was implemented and shipped a month ago |
| D9 | Spec-level Done without runtime evidence (since v3.2.0) | FEATURE marked Done because tests pass and build is green, but the new module has no caller, no command registration, no UI element. Surfaced in the BA-25 Karpathy-Wiki run: 15 of 28 features Done with backend modules that nothing called. |
| D10 | Silent stub / no-op deferral (since v3.2.0) | A listener handler returns no-op while waiting on later wiring. The deferral lives only in code; the backlog has no FIX-row to track it. Removal never happens. |

## The defense map

Each drift source maps to one or more mechanisms. The mechanism lives
in a specific skill or convention file, with a clear owner and trigger.

| Drift | Mechanism | Lives in | Trigger |
|---|---|---|---|
| D1 | Artefakt-Triage at entry | `MANDATORY Phase 0` block in every phase skill, hardened in `/coding` Phase 1a as a technical stop before the first edit | Skill invocation, before first content change |
| D2 | Backlog as single source of truth | `_devprocess/context/BACKLOG.md` is the only place that carries `status`, `phase`, `last-change`, `claim`. Artifact frontmatter carries identity and relations only. Enforced by every skill that updates state | Every status change writes the backlog row first, then the artifact body |
| D3 | ADR abstraction rule + wayfinder | `/architecture` writes ADR core sections without code paths. Code-level hints belong in optional `## Implementation Notes` appendix. Current paths live in `src/ARCHITECTURE.map`, JSDoc headers, module READMEs | Every ADR write, every entry-point edit |
| D4 | Continuous writeback during `/coding` | `/coding` Phase 4 lists explicit triggers: ADR deviation, Success Criterion gap, new pattern, scope change, unexpected constraint. On any trigger, the agent updates the artifact BEFORE the next code edit | During implementation, on every detected deviation |
| D5 | `/consistency-check` mode A at phase end | Every phase skill (`/business-analysis`, `/requirements-engineering`, `/architecture`, `/coding`, `/testing`, `/security-audit`, `/reverse-engineering`, `/dia-migration`) runs mode A in its handoff ritual | Phase end, before commit |
| D6 | ADR consolidation duty in `/architecture` | When proposing a new ADR, the skill first checks whether an existing ADR can be merged or extended. ADR inflation is reported as a warning. Mode B of `/consistency-check` runs the full pairwise check on demand | Every new ADR proposal, on demand for the cross-check |
| D7 | Verification gate in `/coding` and `/testing` | No completion claim without fresh verification evidence in the current message. Hard threshold: 0 test failures, 0 lint errors, 0 build errors, coverage not regressed. Forbidden phrases like "should work" trigger a re-run | After every implementation step, before every completion claim |
| D8 | Eliminated by D2 | When status lives only in the backlog row, frontmatter cannot drift because it does not carry the field | Structural, not enforced |
| D9 | Subtype-aware Done-definition (`/coding` Phase 4a steps 6 and 7) + N-18 invariant in `/consistency-check` Mode A + S-6 / S-7 in Mode B | FEATURE frontmatter declares `subtype: user-facing \| library`. Definition of Done requires a `## Activation Path` section with `Type` and `Identifier`. `/coding` Phase 4a checks reachability (caller exists outside definition file and tests, OR public API export) and that the activation path string actually exists in the code. N-18 (Mode A) flags Done-FEATUREs without a filled Activation Path. S-6 / S-7 (Mode B subagent) verify the SC-to-code mapping and the activation-path identifier presence. | At Done-status writeback in `/coding`, at phase end via `/consistency-check`, before release via Mode B |
| D10 | FIXME(stub) marker convention + E-14 invariant | Every stub MUST carry `// FIXME(stub): ... -- see FIX-{ee}-{ff}-{nn}` AND a paired FIX-row in the backlog. E-14 in `/consistency-check` Mode A enforces bidirectional binding: every marker references an open FIX-ID; every FIX-row tagged as stub has at least one source-side marker. | At every stub introduction in `/coding`, on phase end in Mode A |

## Where the defense is hard, where it is soft

Not every defense is mechanically enforced. DIA mixes hard gates,
soft rules, and structural elimination depending on the cost of the
drift and the cost of the defense.

| Defense type | Means | Drift sources |
|---|---|---|
| Hard gate | Skill stops before the first content change until the rule is satisfied | D1 (in `/coding` Phase 1a only), D7 (verify gate is a hard stop on completion claims), D9 (Phase 4a steps 6 and 7 lock Done-status until reachability and activation-path are confirmed) |
| Soft rule | `MANDATORY` block in the skill body. Agent compliance, no technical block | D1 (in other phase skills), D3, D4, D6 |
| Phase-end check | `/consistency-check` mode A runs at end of every phase, surfaces violations | D2, D3, D5, D8, D9 (N-18 catches the breach if Phase 4a was skipped), D10 (E-14) |
| Structural elimination | Schema makes the drift impossible to express | D8 (frontmatter does not carry status), D3 (ADR core sections do not carry code paths) |

The intentional design choice: hard gates are reserved for the two
sources that bite hardest in practice (D7 build/test drift, D1 in the
implementation phase). Everything else relies on the agent following
the skill instructions plus the phase-end check. This trades absolute
guarantees for low ceremony.

## Known limits

Two drift sources retain residual exposure:

1. **D1 outside the phase skills.** A user who bypasses skill triggers
   and asks the default agent "implement the login button" will not
   hit any DIA mechanism. The phase skill is never invoked, the
   triage never happens, the backlog row never gets created.
   Mitigation today: the user-project documentation lists which
   triggers invoke each skill. Mitigation under evaluation:
   `PreToolUse` hook that blocks edits to `src/` and `_devprocess/`
   without an active triage ID. See [SPIKE-001 in the plugin
   repo](https://github.com/sh-hanke/digital-innovation-agents) for
   the analysis.

2. **D6 cross-ADR-contradiction.** The consolidation duty fires on
   new ADR proposals. ADR pairs that already exist and quietly
   contradict each other are only caught by `/consistency-check`
   mode B (semantic check), which runs on demand. A project that
   never runs mode B can accumulate latent contradictions.

## How to use this map

For a project owner, the map is the audit checklist. After every
release cycle, verify the eight defenses are still active:

- D1: triage IDs in HANDOFFS entries for every code change since the
  last release
- D2: spot-check three artifacts, confirm no `status` field in the
  body, only in the backlog row
- D3: spot-check three ADRs, confirm no code paths in core sections
- D4: read the change log of the most recent PLAN, confirm every
  deviation produced a writeback entry
- D5: run `/consistency-check` mode A on a clean checkout, confirm
  zero orphan findings
- D6: run `/consistency-check` mode B with focus on ADR pairs,
  confirm zero contradictions
- D7: open the latest CI run, confirm zero failures across lint,
  test, build
- D8: spot-check three artifact frontmatters, confirm no `status` or
  `phase` field appears outside the backlog row
- D9: spot-check three Done-FEATUREs created since the last release,
  confirm `subtype:` field is set in frontmatter, `## Activation Path`
  section is filled, and the claimed identifier resolves in the code
- D10: grep `FIXME(stub):` in the source tree, confirm every match
  references a FIX-ID that exists and is open in the backlog

If a defense has slipped, the corresponding skill is the entry point
to repair it.

## See also

- [Three-layer documentation model](./three-layer-documentation): the
  structural source of D2 / D3 / D8 elimination
- [Living Documents](./living-documents): the writeback pattern
  defending D4
- [Verification Gates](./verification-gates): the verify gate
  defending D7
- [Handoff Rituals](./handoff-rituals): the phase-end check
  defending D5
