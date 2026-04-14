---
title: Digital Innovation Agents
description: A V-Model workflow for AI coding assistants. From a rough idea to a production-ready codebase, phase by phase.
---

# Digital Innovation Agents

A V-Model workflow for AI coding assistants. You bring a rough idea,
the agent walks you through exploration, requirements, architecture,
implementation, testing, and security, one deliberate step at a time.

No more "write me a todo app" one-shots that ship hallucinated
requirements. Every phase produces artifacts the next phase can read,
and at the end you have code plus documentation that matches what you
actually built.

<div style="margin: 1.5rem 0;">
  <a href="/digital-innovation-agents/tutorials/installation" class="vp-button" style="display: inline-block; padding: 0.6rem 1.2rem; background: var(--vp-c-brand-1); color: #fff; border-radius: 6px; text-decoration: none; font-weight: 500; margin-right: 0.5rem;">Install</a>
  <a href="/digital-innovation-agents/tutorials/full-v-model-run" class="vp-button" style="display: inline-block; padding: 0.6rem 1.2rem; border: 1px solid var(--vp-c-divider); color: var(--vp-c-text-1); border-radius: 6px; text-decoration: none; font-weight: 500;">Walk through the full cycle</a>
</div>

---

## See it in action

Here is what starting a new project looks like. A rough idea comes
in, the agent guides you through Phase 1 (Business Analysis), and
walks out with a usable artifact. Watch how the agent proposes, cites
sources, and lets you steer. Nothing happens without your confirmation.

<div class="dialog-step">Phase 1: Business Analysis begins</div>

<div class="dialog-turn user">
<div class="speaker">You</div>

I want to build an async retrospective tool for distributed teams.
Our current Zoom retros are 90 minutes, half the team zones out, and
action items never ship.

</div>

<div class="dialog-turn agent">
<div class="speaker">Agent</div>

Got it. Before diving into features, what is the scope?

- **A)** Simple test or feature (hours to 1-2 days)
- **B)** Proof of Concept (1-4 weeks, prove it works)
- **C)** Minimum Viable Product (2-6 months, real product)

</div>

<div class="dialog-turn user">
<div class="speaker">You</div>

B. Let's do a PoC first.

</div>

<div class="dialog-turn agent">
<div class="speaker">Agent</div>

Good. With PoC scope, I will ask 8-12 questions about users and needs,
then move to ideation. First: who exactly are you thinking about? What
kind of team?

</div>

<div class="dialog-turn user">
<div class="speaker">You</div>

Distributed product teams, 5-10 people, 2-week sprints, spread across
3-4 time zones.

</div>

<div class="dialog-turn agent">
<div class="speaker">Agent</div>

Based on what you said, here is a draft persona:

**Maria, Senior Product Manager**
- Leads a 7-person distributed product team across EU and US
- Runs bi-weekly retros that feel stale
- Wants actionable outcomes, not venting sessions

Does this fit, or should we adjust something?

</div>

<div class="dialog-turn user">
<div class="speaker">You</div>

That fits. Maria is the primary.

</div>

<div class="dialog-turn agent">
<div class="speaker">Agent</div>

Noted. Next: when was Maria's last frustrating retro? Can you describe
a specific moment?

</div>

<div class="dialog-turn user">
<div class="speaker">You</div>

Last sprint. Ran 45 minutes over, same issues came up again that never
got fixed in previous retros.

</div>

<div class="dialog-turn agent">
<div class="speaker">Agent</div>

That is the classic "root cause never surfaces" pattern. Let me probe
one level deeper using the 5-Why technique: **why** do you think the
same issues keep resurfacing instead of getting fixed?

</div>

<div class="dialog-turn user">
<div class="speaker">You</div>

Because the action items are too vague and nobody owns them.

</div>

<div class="dialog-turn agent">
<div class="speaker">Agent</div>

Now I have enough for the first insight. Synthesizing:

**Insight (grounded in your example)**
- Retros surface symptoms but not root causes
- Action items lack clear ownership
- Same issues recur sprint after sprint

Source: your last-sprint example (45-minute overrun, repeat issues).
I am adding this to the Exploration Board with the citation.

Should I continue with the next question, or do you want to adjust the
insight first?

</div>

<div class="dialog-turn user">
<div class="speaker">You</div>

Continue.

</div>

<div class="dialog-step">Phase 1 wraps up after 8-12 turns</div>

<div class="dialog-turn agent">
<div class="speaker">Agent</div>

Exploration complete. Here is the synthesis:

**How-Might-We question (the bridge from problem to solution)**

> How might we help distributed product teams run retros that surface
> root causes, so action items actually ship?

Artifacts produced:
- `_devprocess/analysis/BA-retrospectives.md`
- `_devprocess/analysis/EXPLORE-retrospectives.md`

The handoff context was appended to `_devprocess/context/30_handoffs.md`
so the next phase can pick it up. Ready for Ideation (critical
hypotheses, value proposition, the Wow feature), or do you want to
review the Exploration Board first?

</div>

<div class="dialog-turn user">
<div class="speaker">You</div>

Looks good. Let's move to Ideation.

</div>

---

## Why this works

**Nothing is invented in the background.** Every persona, insight,
and hypothesis gets proposed to you with a source citation. You
confirm before it becomes part of the artifact. If the agent synthesizes
from your statement, it cites the statement.

**Scope adapts to the project.** A Simple Test asks 3-5 questions, a
PoC asks 8-12, an MVP goes through the full 20+ method catalog. Same
phases, different depth.

**Structure is visible.** The agent shows which phase you are in,
which technique it is applying (5-Why, concretization, future
projection), and why it is asking each question. The methodology is
not hidden behind a friendly chat wrapper.

**You can always opt out.** Say "stop" or "I want to check first" and
the agent pauses. Say "ignore the V-Model today" and it works in
plain mode. The workflow is advisory, not enforcing.

## Next steps

- **[Install](./tutorials/installation)** on Claude Code, Cursor, Codex, OpenCode, Gemini CLI, or GitHub Copilot
- **[Run the full cycle](./tutorials/full-v-model-run)**: all 7 phases end to end with a small example
- **[Start with your own Business Analysis](./tutorials/first-business-analysis)**: walk through Phase 1 on your project
