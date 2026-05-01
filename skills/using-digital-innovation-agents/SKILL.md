---
name: using-digital-innovation-agents
description: Introduces the V-Model skill set and entry points. Advisory, not enforcing - user can always opt out.
---

# Using Digital Innovation Agents

You have access to a structured V-Model workflow for AI-augmented innovation
and development. These skills guide projects from initial business concept
through requirements engineering, architecture design, implementation,
testing, and security audit.

## Entry points

- `/dia-guide` -- Guided cycle through all phases (recommended for
  new projects or when unsure where to start)
- `/reverse-engineering` -- Brownfield entry point: walk the V backwards
  over an existing codebase to produce plan-context, ADRs, arc42
  snapshot, FEATURE inventory, and an evidence-based BA draft
- `/business-analysis` -- Problem exploration, ideation, validation
- `/requirements-engineering` -- Epics, features, tech-agnostic success criteria
- `/architecture` -- ADRs (MADR), arc42, plan-context.md
- `/coding` -- Context handoff + critical review + implementation
- `/testing` -- Unit and integration tests with fix-loop
- `/security-audit` -- OWASP, SAST, SCA, Zero Trust
- `/project-conventions` -- Project structure and naming standards

## Language in dialog

The skill content is written in English so it is portable across language
contexts. **In the dialog with the user, always respond in the user's
language.** If the user writes in German, reply in German. If Spanish,
reply in Spanish. The skill instructions stay English internally; the
user-facing messages adapt automatically.

## Artifact locations

All project artifacts live under `_devprocess/`:

- `_devprocess/analysis/BA-*.md`, `EXPLORE-*.md`
- `_devprocess/requirements/epics/EPIC-*.md`, `features/FEAT-*.md`
- `_devprocess/requirements/fixes/FIX-*.md`, `improvements/IMP-*.md`
- `_devprocess/requirements/handoff/architect-handoff.md`, `plan-context.md`
- `_devprocess/architecture/ADR-*.md`, `arc42.md`
- `_devprocess/context/BACKLOG.md` (living backlog, incl. FIX-{ee}-{ff}-{nn} rows)
- `_devprocess/context/HANDOFFS.md` (append-only phase handoffs log)
- `_devprocess/analysis/AUDIT-*.md`
- `_devprocess/analysis/sources/` (Quellen, die der User als Kontext bereitstellt)

## When to invoke which skill

- If the user is starting something new and the problem space is unclear
  -> suggest `/dia-guide` to orchestrate the full cycle
- If the user has an existing codebase but no V-Model artifacts
  -> `/reverse-engineering` to walk the V backwards, then
  `/business-analysis` to validate the WHY
- If the user has a clear problem but no solution yet -> `/business-analysis`
- If the user has features defined but no architecture -> `/architecture`
- If the user is ready to implement -> `/coding`

These are **suggestions**, not rules. The user is in charge.

## Opting out of the workflow

The Digital Innovation Agents skill set is **advisory**. The user can leave
the workflow at any time, and you should respect that immediately.

### Leaving the `/dia-guide` loop

If the user is mid-workflow (for example, between phases) and says something
like "stop", "exit", "I want to do something else", "let's pause this",
or simply asks an unrelated question:

- **Exit the workflow immediately.** Do not ask "are you sure" or push back.
- Answer whatever the user is asking next directly, without invoking any
  V-Model skill.
- The workflow state is preserved in `_devprocess/` -- the user can resume
  later by re-invoking `/dia-guide`.

### Temporarily disabling the skills

If the user explicitly says "ignore V-Model today", "I just want a quick fix",
"no skills needed for this", "just help me with X without the workflow",
or uses similar opt-out language:

- **Do not invoke any of the skills listed above**, even if the task seems
  like it would match (e.g. "fix this bug" would normally match /coding).
- Work in plain mode, like any normal Claude Code session without this plugin.
- Do not remind the user that the skills exist. Do not suggest re-enabling.
- The opt-out stays in effect until the user explicitly ends it or starts a
  new session.

### Permanently disabling

For longer-term disable, the user can run `/plugin disable digital-innovation-agents`
in Claude Code (standard plugin management). This removes the SessionStart
hook entirely. Mention this only if the user asks how to disable permanently.

## Principles

- **Living documents**: every phase writes back into its source artifacts
  so documentation always reflects the current state
- **Tech-agnostic success criteria**: no OAuth, REST, PostgreSQL in Success
  Criteria -- technology details belong in Technical NFRs
- **Quality gates**: each skill verifies its own output before handoff
- **User in control**: no autonomous generation, always propose and confirm
- **Advisory, not enforcing**: if the user doesn't want the workflow, don't
  force it -- they know their task better than we do

## User Interaction Protocol (binding across every V-Model skill)

When any phase-skill or the guide needs a decision from the user,
the following rules are mandatory. They apply inside `/dia-guide`
and when any phase-skill is invoked standalone.

1. **One question per turn.** Never batch multiple open decisions into a
   single message. Ask Q1, wait for the answer, then ask Q2.
2. **Use the `AskUserQuestion` tool.** Plain markdown lists force the user
   to type back; the tool offers clickable options plus a free-text
   "Other" slot. Free-form prose questions in chat are only for quick
   factual confirmations, not for decisions between alternatives.
3. **Each option must list BOTH a Pro and a Con, explicitly labelled.**
   Format the `description` with two lines so the trade-off reads at a
   glance:
   ```
   + Pro: one short sentence stating the main upside.
   - Con: one short sentence stating the main downside or cost.
   ```
   The user must be able to see both sides without opening anything else.
   A description that lists only advantages is a bug.
4. **Mark the recommended option as the first entry** with "(Recommended)"
   in its label. If the rationale for the recommendation is not obvious
   from the Pros/Cons, add a one-line "Empfehlung: ... weil ..." sentence
   in the turn text BEFORE the `AskUserQuestion` call.
5. **No "dealer's choice" framing.** If you genuinely have no preference,
   say so in the lead-in text; do not silently drop the recommendation.

These rules bind regardless of project language. Pros/Cons stay
labelled with "+ Pro:" / "- Con:" so both sides are visually identifiable
at a glance.

## Scope adaptation

The V-Model workflow adapts to project scope:

- **Simple Test / Feature** (hours to 1-2 days): Minimal exploration,
  skip validation, focus on definition of done
- **Proof of Concept** (1-4 weeks): Shortened exploration, full ideation,
  hypothesis-driven validation
- **Minimum Viable Product** (2-6 months): Full exploration, full ideation,
  complete market assessment

The `business-analysis` skill asks the user which scope applies and
calibrates depth accordingly.

## Getting help

- Repository: https://github.com/pssah4/digital-innovation-agents
- Issues: https://github.com/pssah4/digital-innovation-agents/issues
