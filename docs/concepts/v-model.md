---
title: The V-Model
description: Why the V-Model shape, the seven phases, and how Digital Innovation Agents adapts it for AI-augmented development.
---

# The V-Model

Digital Innovation Agents is built around the V-Model, a sequential
development process that bends in the middle. The left side is design
(what are we building?), the bottom is implementation (build it), and
the right side is verification (does it work? is it safe?). Each
left-side phase has a matching right-side phase that verifies it.

## Why the V-Model?

Traditional AI coding sessions look like this:

```
User idea -> Agent writes code -> PR
```

That skips everything that matters for real projects: understanding
the problem, defining the solution scope, making deliberate
architecture decisions, verifying the implementation. Small features
survive this shortcut. Anything bigger does not.

The V-Model forces a deliberate path:

1. Understand the problem before designing the solution
2. Define requirements before making architecture decisions
3. Design the architecture before implementing
4. Verify tests before running a security audit
5. Audit security before releasing

Every phase produces artifacts that the next phase reads. Nothing is
ad-hoc, nothing is only in the agent's head. Everything lives in
`_devprocess/` so you can review, audit, and reproduce.

## The seven phases

![V-Model workflow for Claude Code](/v-model-overview.svg)

The design phases (BA, RE, Arch) sit on the left. Implementation
(Claude Code) is in the middle. Verification (Testing, Security) is on
the right. Each phase produces a durable artifact below it, the fix
loops iterate until tests pass and findings are resolved, and the
review sync keeps architecture decisions in sync with the real codebase.

**Phase 1: Business Analysis.** Exploration, Ideation, Validation.
Produces the `BA-{PROJECT}.md` document with personas, HMW question,
value proposition, idea potential, and critical hypotheses.

**Phase 2: Requirements Engineering.** Transforms the BA into Epics,
Features, and tech-agnostic Success Criteria. Produces the
`architect-handoff.md`.

**Phase 3: Architecture.** Creates ADRs (one per Critical ASR),
arc42 documentation, and the `plan-context.md` context bridge.

**Phase 4: Coding.** Critical review against the real codebase,
implementation with task-level guidelines, writeback to all artifacts.
This is the bottom of the V.

**Phase 5: Testing.** Integration tests, unit-test gap-filling,
fix-loop until all tests are green.

**Phase 6: Security Audit.** OWASP Top 10, OWASP LLM Top 10, SAST,
SCA, Zero Trust. Fix-loop until all critical findings are resolved or
explicitly deferred.

**Closing Handoff (not a phase).** After a green `/security-audit`,
the guide runs `/consistency-check` mode B, outputs a closing report
(Feature/bug/security counts, finalised artifacts), and emits the
`release-to-ba` HANDOFFS template. The actual release act
(version bump, merge, tag, publish) is delegated to a project-
specific release skill outside the public DIA plugin.

## The traceability chain

Every artifact traces back to the one that produced it:

```
BA document (Why?)
  -> Epic (What, strategic?)
    -> Feature (What, concrete?)
      -> ASR (What is architecture-relevant?)
        -> ADR (How do we solve it?)
          -> plan-context.md (Context bridge)
            -> Critical Review (Does it fit the codebase?)
              -> Code
                -> Tests (Does it work?)
                  -> Security Audit (Is it safe?)
                    -> Closing Handoff (consistency-check mode B + optional release)
```

If you open a random line of code, you can walk backwards through this
chain and end up at a business motivation in the BA document. No
orphans, no "we added this because it seemed useful".

## Why the writeback matters

Every step in this chain also writes backwards. When `/coding` finds
that an ADR does not match the real codebase, it updates the ADR
before implementing. When a bug is fixed, the
`FIX-{ee}-{ff}-{nn}` row in `BACKLOG.md` carries the commit SHA, and
the detail file under `_devprocess/requirements/fixes/` carries the
regression test. When a Feature's Success Criterion cannot be met as
specified, the Feature file is updated with the reason.

This is the [Living Documents pattern](./living-documents). It keeps
documentation in sync with reality. The
[Three-layer documentation model](./three-layer-documentation)
explains why state lives in the backlog row and substance lives in
the detail artifact, never both.

## Phase transitions

Every phase ends with a mandatory 4-part [Handoff Ritual](./handoff-rituals)
(artifact report, handoff context, phase-end commit plus
`tag-phase`, transition question), followed by `/consistency-check`
Mode A at the phase boundary. The
[V-Model workflow guide](../guides/dia-guide) drives
transitions when you run `/dia-guide`. Individual phase skills
run the ritual too when invoked directly.

## The V is iterative, not linear

The diagram above shows a straight walk from Phase 1 through the
Closing Handoff. In
practice the V is a decision graph. Real projects discover things mid
flight: a bug surfaces during `/coding` that nobody predicted, an
architectural choice turns out to be wrong once the code exists, a
FEAT spec reveals a gap once you try to design around it, and
sometimes coding hits a capability the architecture never anticipated.

Four cross-phase feedback triggers make the iteration explicit:

- **Mid-course bug discovery** in `/coding`. A new bug pauses the
  implementation. Triage routes the issue to a fix or a feature, root
  cause analysis lands in the FIX detail file, and the
  `FIX-{ee}-{ff}-{nn}` backlog row appears BEFORE any fix gets
  written.
- **Mid-course design discovery** in `/coding`. An ADR no longer
  matches reality. The coding flow pauses, amends or supersedes the
  ADR, updates `arc42.md`, the wayfinder, and `plan-context.md`, and
  only then continues the feature.
- **Mid-course requirements discovery** in `/architecture`. A FEAT
  spec has a gap or an impossible constraint. Architecture pauses
  and routes the issue back to `/requirements-engineering` for a FEAT
  update.
- **Mid-course capability discovery** in `/coding`. The
  implementation needs something the architecture never planned (a
  new library, a new infrastructure component, a new pattern). The
  coding flow pauses, captures the capability gap as an ADR, and
  routes back through `/architecture` to integrate the decision
  before the implementation continues.

Each trigger follows the same 6-step pattern (STOP, triage, root
cause, backlog, change with commit Refs, Final sync). The forward
walk remains the default. Iteration is an option, not a detour.

## Scope adaptation

The same V-Model runs for:

- **Simple Test / Feature** (hours to 1-2 days): minimal Exploration,
  skip Validation, focus on Definition of Done
- **Proof of Concept** (1-4 weeks): shortened Exploration, full
  Ideation, hypothesis-driven Validation
- **Minimum Viable Product** (2-6 months): full Exploration, full
  Ideation, complete market Validation

The phases are the same. The depth adapts.

## See also

- [V-Model workflow guide](../guides/dia-guide): the guide
- [A full V-Model run tutorial](../tutorials/full-v-model-run): end-to-end walkthrough
- [Living Documents](./living-documents): the writeback pattern
- [Handoff Rituals](./handoff-rituals): phase transitions
