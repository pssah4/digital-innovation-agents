---
title: Digital Innovation Agents
description: A V-Model workflow for AI coding assistants. From a rough idea to a production-ready codebase, phase by phase.
---

# Digital Innovation Agents

A V-Model workflow for AI coding assistants. You bring a rough idea,
the agent walks you through exploration, requirements, architecture,
implementation, testing, and security, one deliberate step at a time.
Every phase produces artifacts the next phase can read. At the end you
have code plus documentation that matches what you actually built.

<div style="margin: 1.5rem 0;">
  <a href="/digital-innovation-agents/tutorials/installation" class="vp-button" style="display: inline-block; padding: 0.6rem 1.2rem; background: var(--vp-c-brand-1); color: #fff; border-radius: 6px; text-decoration: none; font-weight: 500; margin-right: 0.5rem;">Getting Started</a>
  <a href="/digital-innovation-agents/tutorials/full-v-model-run" class="vp-button" style="display: inline-block; padding: 0.6rem 1.2rem; border: 1px solid var(--vp-c-divider); color: var(--vp-c-text-1); border-radius: 6px; text-decoration: none; font-weight: 500;">Walk through the full cycle</a>
</div>

## The workflow in one picture

```mermaid
flowchart LR
    BA["<b>BA</b><br/>Why"]:::design
    RE["<b>RE</b><br/>What"]:::design
    AR["<b>Arch</b><br/>How"]:::design
    RV["<b>Review</b><br/>Handoff"]:::handoff
    CC["<b>Claude Code</b><br/>Default agent"]:::agent
    TE["<b>Testing</b><br/>UT + IT"]:::verify
    SA["<b>Security</b><br/>Audit"]:::secure

    BA --> RE --> AR --> RV --> CC --> TE --> SA

    BA -.- BAdoc["BA doc"]:::artifact
    RE -.- feat["Features<br/>Handoff"]:::artifact
    AR -.- adr["ADRs<br/>plan-context"]:::artifact
    TE -.- tests["Test suites"]:::artifact
    SA -.- audit["Audit report"]:::artifact

    CC -. "Test fix loop" .-> TE
    CC -. "Security fix loop" .-> SA
    RV -. "Review sync" .-> AR

    classDef design fill:#d1f4e8,stroke:#0d9488,stroke-width:2px,color:#065f46
    classDef handoff fill:#ffedd5,stroke:#f97316,stroke-width:2px,color:#9a3412
    classDef agent fill:#f3f4f6,stroke:#6b7280,stroke-width:2px,color:#374151
    classDef verify fill:#ede9fe,stroke:#8b5cf6,stroke-width:2px,color:#5b21b6
    classDef secure fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b
    classDef artifact fill:#ffffff,stroke:#d1d5db,stroke-width:1px,color:#6b7280,font-size:11px
```

<p style="text-align: center; color: var(--vp-c-text-2); font-size: 0.9rem; margin-top: -0.5rem;">
Structured AI skills from analysis to security audit, with fix loops
and living documents. Each phase produces artifacts that feed the next.
</p>

## How it works

- **BA and RE** are your first two phases. You explore the problem
  with personas, needs, and how-might-we questions, then turn them
  into Epics and Features with tech-agnostic Success Criteria.
- **Architecture** proposes ADRs and a plan-context. The agent writes
  one decision record per architecturally significant requirement.
- **Review handoff** reconciles the design against your real codebase
  before implementation begins. This is where ADRs get adjusted if
  they do not match reality.
- **Claude Code (or your coding assistant of choice)** runs the
  implementation, guided by task-breakdown rules and a verification
  gate that blocks premature "done" claims.
- **Testing and Security** come with their own fix loops. They keep
  iterating until all tests pass and critical findings are resolved.
- **Living documents** flow back up the V. ADRs, Features, and the
  plan-context update themselves during implementation so
  documentation always reflects the actual code.

You can run the full cycle via `/v-model-workflow`, or start at any
phase with a single skill like `/business-analyse`. The workflow is
advisory: say "stop" or "ignore the V-Model today" and the agent
steps back into plain mode.

## Next steps

- **[Getting Started](./tutorials/installation)**: install on Claude Code, Cursor, Codex, OpenCode, Gemini CLI, or GitHub Copilot
- **[A full V-Model run](./tutorials/full-v-model-run)**: all 7 phases end to end with a small example project
- **[Your first Business Analysis](./tutorials/first-business-analysis)**: walk through Phase 1 on your own idea
