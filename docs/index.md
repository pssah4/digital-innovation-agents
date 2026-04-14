---
title: Digital Innovation Agents
description: A V-Model workflow for AI coding assistants. Methodology-driven discovery for WHAT to build, plus a state-of-the-art coding loop for HOW to build it.
---

# Digital Innovation Agents

The AI coding workflow that figures out **what** to build before writing
**how**. Seven phases, proven innovation methodology on the left side
of the V, a state-of-the-art coding loop on the right side, and living
documents that stay in sync with reality.

<div style="margin: 1.5rem 0;">
  <a href="/digital-innovation-agents/tutorials/installation" class="vp-button" style="display: inline-block; padding: 0.6rem 1.2rem; background: var(--vp-c-brand-1); color: #fff; border-radius: 6px; text-decoration: none; font-weight: 500; margin-right: 0.5rem;">Getting Started</a>
  <a href="/digital-innovation-agents/tutorials/full-v-model-run" class="vp-button" style="display: inline-block; padding: 0.6rem 1.2rem; border: 1px solid var(--vp-c-divider); color: var(--vp-c-text-1); border-radius: 6px; text-decoration: none; font-weight: 500;">Walk through the full cycle</a>
</div>

![V-Model workflow for AI coding assistants](/v-model-overview.svg)

## The hard part is not the code

The hardest part of shipping software is not writing the code. It is
deciding **what** the code should do, for **whom**, and **why**.
Most AI coding tools skip that part. You describe your app, they write
code, and three sprints later you are rewriting it because nobody
asked who the users were or whether the feature should have existed
in the first place.

Digital Innovation Agents spends the first three phases on exactly
that question, using methods product teams have relied on for decades.
Then it hands off to a coding loop that is just as disciplined as the
discovery, with a verification gate that blocks the "looks done"
failure mode that plagues AI coding sessions.

## What makes it different

### 1. Real discovery, not a chat wrapper

Phase 1 (Business Analysis) is a facilitated discovery process, not a
prompt box. The agent walks you through structured innovation methods:

- **Exploration**: personas, needs, insights, stakeholder maps, user
  journeys, trends, competitors
- **Ideation**: Jobs to be Done, hypothesis framing, idea potential
  scoring (value / transferability / feasibility), the "Wow" feature,
  value proposition synthesis
- **Validation**: pricing, channels, market viability, critical
  hypotheses to test, unfair advantage, revenue streams

Every persona is proposed and confirmed by you. Every insight cites
the specific user statement it came from. Nothing is invented in the
background. The output is a **How-Might-We question** that bridges
problem to solution, plus a Business Analysis document backed by
20+ proven methods.

Requirements Engineering then turns the HMW into Epics, Features, and
**tech-agnostic Success Criteria**. No OAuth, no REST, no PostgreSQL
leaking into requirements. Technology choices belong in the separate
Technical NFRs section, which is the architect's problem, not the
business side's.

Architecture produces ADRs in MADR format (with at least two
alternatives and trade-offs per decision), an arc42 document, and the
`plan-context.md` that bridges design to implementation.

### 2. A coding loop that is actually state of the art

Phase 4 (Coding) is not a free-for-all. Before any implementation
starts, a **critical review** reconciles the design artifacts against
your real codebase. ADRs that conflict with existing patterns get
adjusted **before** a single line of code is written.

The implementation itself is briefed with:

- **Bite-size tasks** with complete code. No placeholders, no "TBD",
  no "similar to Task N"
- **Optional TDD mode**: RED -> verify RED -> GREEN -> verify GREEN
  -> REFACTOR. Opt-in when you want the discipline, off when you are
  prototyping
- **4-phase debugging protocol** when bugs appear: Root Cause ->
  Pattern Analysis -> Hypothesis -> Implementation. After 3+ failed
  fix attempts an "architecture alarm" kicks in and forces a step
  back instead of a fourth patch
- **Verification gate**: no completion claims without fresh evidence.
  "Tests pass" requires the actual test command output with 0 failures.
  "Build works" requires an exit-code-0 build. No hallucinated "done"
- **Regression test cycle**: every bug fix goes through red-green-red
  validation (write test, verify it catches the bug without the fix,
  verify it passes with the fix)

### 3. Verification that actually verifies, documents that stay alive

Testing runs an integration-focused fix-loop that does not stop until
all tests pass. Security Audit covers OWASP Top 10, OWASP LLM Top 10,
SAST, SCA, and Zero Trust validation, with its own fix-loop for
findings.

Throughout the whole cycle, artifacts are **living documents**. ADRs,
Features, `plan-context.md`, and arc42 update themselves during and
after implementation. At the end, documentation reflects what was
actually built, not what was originally planned.

### 4. Handoffs at every phase transition

Every phase ends with a mandatory 3-part Handoff Ritual: an artifact
report, a handoff context entry appended to `_devprocess/context/30_handoffs.md`,
and an explicit transition question. The orchestrator drives phase
transitions actively when you run `/v-model-workflow`. You can always
opt out by saying "stop" or "I want to check first". The workflow is
advisory, not enforcing.

## Next steps

- **[Getting Started](./tutorials/installation)**: install on Claude Code, Cursor, Codex, OpenCode, Gemini CLI, or GitHub Copilot
- **[A full V-Model run](./tutorials/full-v-model-run)**: all seven phases end to end with a small example project
- **[Your first Business Analysis](./tutorials/first-business-analysis)**: walk through Phase 1 on your own idea
