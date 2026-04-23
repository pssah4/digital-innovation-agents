---
title: PULSE
description: A team operating model for AI-native development. PULSE is the collaboration layer on top of the Digital Innovation Agents V-Model workflow.
---

# PULSE

> **A team operating model for AI-native development.**
> PULSE is the collaboration layer on top of the V-Model workflow.

The V-Model gives a single human-agent pair a structured walk from
problem to release. PULSE is what happens when several pairs work the
same product at the same time. It takes the workflow that already
runs inside one pair and turns it into a rhythm the whole team can
move to.

Not a process. A pulse. Regular, lightweight, essential.

## Why PULSE exists

Single-player AI development is a productivity question. One person,
one agent, optimise the prompts and the toolchain and ship.

Multiplayer AI development is a coordination question. Multiple people,
each with their own agent, working on the same codebase, each fast
enough to ship a feature in an afternoon. Scrum was built for human
cycle times. Kanban can absorb the pace but loses the rhythm. Shape Up
runs in six-week cycles. None of them fit a team where the bottleneck
is no longer implementation, it is alignment.

PULSE is what we use day to day at one of Germany's energy companies
where small teams build internal products with coding agents. It
exists because the team needed something that does not slow the pairs
down but keeps them coherent.

## The shift

When a pair ships a feature in hours, three things change at once:

- **The plan becomes the product.** Writing code is cheap. Deciding
  what should exist is the expensive work.
- **Speed amplifies whatever is already there.** A team without
  structure ships incoherent features faster. A team with structure
  ships coherent ones faster.
- **The ability to say "no" matters more than the ability to say "yes".**
  Implementation cost no longer filters ideas. Something else has to.

The principles of product development have not changed. The cycle
time has. That changes how teams coordinate, not what they coordinate
on.

## The four values

In the spirit of the original Agile Manifesto, which worked because
it stated values and not procedures, PULSE values:

> **Shared artifacts** over status meetings.
> **Team coherence** over individual speed.
> **Conscious filters** over unlimited backlogs.
> **Structural governance** over approval gates.

**Shared artifacts over status meetings.** A coding agent has no memory
between sessions. A teammate does not know what you built yesterday.
Written artifacts are the only synchronisation that works for both
audiences. A spec, an ADR, a backlog entry. Not a standup, not a Teams
message.

**Team coherence over individual speed.** Each pair is fast. Speed
without direction is drift. A team that ships five coherent features
beats a team where three pairs each ship five uncoordinated ones.

**Conscious filters over unlimited backlogs.** When implementation is
cheap, every idea feels worth building. PULSE prevents ideas from
becoming work without passing through a deliberate filter. That filter
separates a product team from a feature factory.

**Structural governance over approval gates.** Nobody wants to wait
for someone to sign off a PR at 11pm. The answer is governance baked
into structure: automated quality gates, fitness functions, conventions
that agents and humans follow equally. The rules live in the code and
the specs, not in someone's calendar.

## Three layers, three tempos

This is the part that distinguishes PULSE from Scrum, Kanban, or
Shape Up. Instead of one cadence for everything, three tempos run at
the same time.

| Layer | Cadence | What it produces |
|---|---|---|
| Execution | Hourly | Working features, PRs, updated artifacts |
| Coordination | Daily | Shared situational awareness, blocker resolution |
| Product | Weekly to bi-weekly | Direction, learning, roadmap fit |

### Execution layer (hourly)

Each human-agent pair works autonomously. Pick a feature from the
shared backlog, spec it, implement it, test it, open a PR. In hours,
not weeks. One constraint: nobody works on something that is not in
the backlog. Spontaneous ideas go to the Ideas channel, not directly
into code.

The pair runs the V-Model walk inside this layer. Specifically, the
pair invokes [`/v-model-workflow`](/guides/v-model-workflow) for
end-to-end runs or the individual phase skills
([`/business-analyse`](/guides/business-analyse),
[`/requirements-engineering`](/guides/requirements-engineering),
[`/architecture`](/guides/architecture),
[`/coding`](/guides/coding),
[`/testing`](/guides/testing),
[`/security-audit`](/guides/security-audit)) for partial cycles.

### Coordination layer (daily)

The team synchronises through three lightweight rituals:

- **Async status (daily, 2 min writing).** What is done, what is next,
  any blockers. Structured, not prose. Machine-readable enough that
  an agent could generate a team summary.
- **Sync call (twice a week, 30 min).** Not "what did you do", that is
  in the async status. Resolve blockers, review ideas from the Ideas
  channel, adjust priorities.
- **Code review (continuous, async).** PRs reviewed within 4 hours.
  Focus on architecture conformance, not syntax. The agent handles
  syntax.

Total meeting overhead: under 2.5 hours per week.

### Product layer (weekly to bi-weekly)

Direction, not tickets.

- **Direction session (every two weeks, 90 min).** Replaces sprint
  planning, sprint review, and retrospective in one. Focus: what 3 to
  5 outcomes do we want in the next two weeks? What did we learn?
  What needs to change?
- **Roadmap review (monthly, 60 min).** Does the roadmap still match
  the Business Analysis?

The three layers are nested. The execution layer runs continuously
inside the coordination layer, which runs inside the product layer.
A pair might ship three features in a single day while the product
direction stays stable for two weeks.

## The Shared Context Layer

This is where PULSE lives or dies. Coding agents have no memory
between sessions. Teammates do not know each other's context. Shared
living artifacts are the only synchronisation that works.

The [V-Model workflow](/concepts/v-model) defines the structure that
PULSE relies on. Every pair reads from and writes to the same files
in `_devprocess/`:

- [`BA-{PROJECT}.md`](/guides/business-analyse): the product north star.
  Lives across releases through [Post-Release Review](/guides/business-analyse#phase-8-post-release-review-ba-as-living-document).
- [`EPIC-*.md` and `FEATURE-*.md`](/guides/requirements-engineering):
  the unit of work, written tech-agnostic so anyone (or any pair) can
  pick them up.
- [`ADR-*.md` and `arc42.md`](/guides/architecture): architecture
  decisions and the architecture document that survives individual
  iterations.
- `architect-handoff.md` and `plan-context.md`: the connective tissue
  between phases, with [Dialog sections](/concepts/handoff-rituals#dialog-handoffs-not-blockers)
  for questions a pair cannot answer alone.
- `10_backlog.md`: the source of truth for project state, with the
  [Claim column](/reference/conventions#pair-ids-concurrent-agent-coordination)
  that lets pairs work concurrently without a central lock service.
- `30_handoffs.md`: append-only log of every phase transition.
- `40_metrics.md`: the [signal layer](/reference/artifacts#the-four-context-files).
  Cycle time, drift count, hypothesis status, phase transitions,
  cross-phase trigger counts. Append-additive, no rituals.
- `CLAUDE.md` and `memory/MEMORY.md`: institutional memory loaded by
  every agent at session start.

Every artifact serves two audiences: humans who need alignment, and
agents who need context. If a teammate can read it, an agent can read
it. If an agent needs it, a teammate needs it too.

For the full pattern see [Living Documents](/concepts/living-documents).

## The conscious filter

The most important part of PULSE is what it prevents.

When implementation is cheap, the temptation is to turn every idea
into a feature immediately. PULSE creates a deliberate pipeline:

```
Ideas channel  ->  Sync call filter  ->  Backlog  ->  Pair claim  ->  Work
   (free flow)    (10 min review,      (filtered,    (Claim col)
                  matches against BA   prioritised)
                  and roadmap)
```

The filter is lightweight. It happens in 10 minutes during the sync
call. But it exists. Its existence keeps the product coherent.

No pair works on anything that has not passed the filter. Discoveries
made mid-implementation also flow through the filter via the
[cross-phase feedback triggers](/concepts/v-model#the-v-is-iterative-not-linear),
not through ad-hoc code changes.

## Communication channels

Four channels, in any tool the team uses (Teams, Slack, Discord):

| Channel | Purpose | Example |
|---|---|---|
| Ideas | Free-flowing impulses | "Could we add a CSV export?" |
| Async status | Daily structured updates | "Done X, next Y, blocked on Z" |
| Code reviews | PR-level architecture conformance | Comment thread on PR-42 |
| Direction | Bi-weekly outcome decisions | Direction session notes |

If something is in Ideas, it is an impulse. Only when it passes the
sync call filter and lands in the backlog does it become work.

## Roles as hats

In a 3 to 4 person team, these are hats, not dedicated positions:

| Hat | Responsibility |
|---|---|
| Product direction | Owns the BA, runs the direction session, calls the filter decisions |
| Architecture | Owns ADRs and arc42, reviews PRs for architectural conformance |
| Quality | Owns testing strategy, security findings, and the metrics layer |

The person wearing the product direction hat still works as a pair
and ships features. These are responsibilities, not full-time jobs.
The hats move. Whoever is closest to a decision wears the hat for it.

## PULSE and the V-Model

PULSE defines how a team collaborates. The V-Model defines what
happens inside a pair.

```
Team layer        PULSE       (this page)
                    |
                    v
Pair layer        V-Model     (/concepts/v-model)
                    |
                    v
Phase layer       Skills      (/guides/*)
```

A pair ships a feature by walking the V (Business Analysis ->
Requirements -> Architecture -> Coding -> Testing -> Security Audit ->
Release Closure). The walk is not strictly linear. The
[V is a decision graph](/concepts/v-model#the-v-is-iterative-not-linear)
with three cross-phase triggers (mid-course bug, mid-course design,
mid-course requirements) that close the iteration loop.

The team layer (PULSE) consumes the artifacts the pair layer
produces. The Direction Session reads `40_metrics.md`. The Sync Call
reads `30_handoffs.md` and pending Dialog entries. The conscious
filter reads against the BA. Nothing in PULSE asks pairs to produce
extra artifacts. Every artifact PULSE relies on is already produced
by the V-Model.

## What PULSE is not

- **Not anti-planning.** The Direction Session is planning. It is
  compressed and focused on outcomes, not estimation.
- **Not anti-meeting.** It defines fewer meetings, sharper meetings,
  and more written async work.
- **Not a complete framework.** It is a starting point. Teams adapt
  the cadences and the filter to their reality, the same way teams
  adapt Scrum.
- **Not Scrum's replacement on principle.** Scrum solved a real
  problem. The problem has changed. Teams that already work well with
  Scrum can keep what fits and pull in what closes their gaps.

## Adoption notes

PULSE is built around the V-Model artifact set. To run it you need:

1. The [Digital Innovation Agents](/) skill set installed (provides
   the V-Model phases and the artifact templates)
2. A `_devprocess/` directory in the project (set up by
   [`/project-conventions`](/guides/project-conventions))
3. A backlog with the binding format (BL-NNN rows, dashboard, Claim
   column)
4. A `40_metrics.md` seeded from the template

Once the artifacts exist, the rituals layer on top. Start with the
async status and the sync call. Add the Direction Session at the
first natural rhythm break. The Roadmap Review can wait until the
first month is in.

## Open conversations

PULSE is not finished. The article that introduced it
([LinkedIn, April 2026](https://www.linkedin.com/in/sebastian-hanke-product/))
attracted dozens of substantive challenges. The ones that shaped the
v2.2.0 workflow update are recorded here. Each is a real critique
with a real reply. The replies that prompted code changes link to the
feature that closed the gap.

### "The V looks like waterfall"

Helder A. (Agile Coach):

> While PULSE seems to espouse some constructs aimed at building
> shared understanding, it relies heavily on handoffs in a linear
> workflow. Shared understanding comes from interaction, not docs.

Reply. The V-Model phases are sequential. That is true. The
difference to waterfall: in waterfall, each phase runs once and gets
thrown over the fence to a different team. In PULSE, the same pair
runs through all phases in hours. The handoffs are not between
people, they bridge agent sessions that have zero memory. Without
`architect-handoff.md`, the next agent session does not know what the
previous one decided.

The artifacts do not replace conversation. They make conversation
productive. Sync calls, code reviews, and the Ideas channel are the
interaction loops. The docs ensure those conversations are not
wasted on "wait, what did you build yesterday?".

What changed in v2.2.0:
[`/concepts/v-model#the-v-is-iterative-not-linear`](/concepts/v-model#the-v-is-iterative-not-linear)
makes explicit that the V is a decision graph with three cross-phase
triggers (mid-course bug, mid-course design, mid-course requirements).
The forward walk is the default, iteration is a first-class option.

### "Architecture decisions get made implicitly"

A mobile engineering lead asked:

> ADRs record decisions, but architecture emerges the moment the
> first code lands in the repo, before any decision is named. With
> five parallel pairs the first merge holds de facto authority. How
> does PULSE catch these implicit commitments before the next
> Direction Session can react?

Reply. Two mechanisms close this gap.
[`/reverse-engineering`](/guides/reverse-engineering) discovers
implicit and explicit design decisions that already exist in the
codebase, surfaces them as `ADR-NNN-{slug}.md` files marked
`Inferred`, and folds them into the architecture record so the next
pair adapts to a named decision instead of an unnamed pattern.
[`/coding`](/guides/coding) runs a critical review against the real
codebase before any new feature implementation begins. If the
existing code conflicts with a planned ADR, the ADR is amended or
superseded before the implementation, not after.

What changed in v2.2.0: the
[mid-course design discovery trigger](/concepts/v-model#the-v-is-iterative-not-linear)
formalises the second pattern. Code that proves a design wrong now
amends the ADR with a commit reference, in the same flow as the bug
trigger.

### "The reading budget per person is not in the model"

Mark Zimmermann (second comment):

> When a pair generates 60 pages of context in two days, nobody
> absorbs it all and consensus shifts to whoever summarises loudest.
> PULSE names three tempos, but the reading budget per person is not
> in the model. Have you found a compression layer for this?

Reply. Not yet. The constraint is real. The V-Model is built so the
agents read the artifacts in full and the humans can read summaries.
Specifically: every Sync Call reads only `30_handoffs.md` (the latest
entries) and pending Dialog entries, not the full FEATURE specs.
Direction Sessions read `40_metrics.md` for the trend, not the
underlying detail.

A dedicated narrator skill that summarises the latest Sprint of
artifacts is on the roadmap. Until then, the asymmetry holds: agents
absorb depth, humans absorb shape.

### "Where does the Verifier role live?"

Mark Zimmermann (third comment):

> The InfoWorld piece framed it as a coordination-layer failure. DORA
> 2025 finds AI is negatively correlated with delivery stability when
> control systems lag behind change volume. Three tempos buy you the
> control surface. Open question: where in PULSE does the Verifier
> role live, with the pair, the reviewer, or the artifact itself?

Reply. The verifier lives in the artifact and the workflow, not the
person. The
[Verification Gates](/concepts/verification-gates) inside each phase
skill produce evidence-bound status transitions. The
[Security Audit](/guides/security-audit) phase runs OWASP, OWASP LLM,
SAST, SCA, and Zero Trust checks before release. Code reviews focus
on architecture conformance.

PULSE is integrated with the skills and workflow of Digital Innovation
Agents. Every team can adapt and add skills for their own needs.
Treat PULSE as a starting point, not a process manual.

### "The signal layer is missing"

Martin König (Senior Atlassian Architect):

> Good operating model. I am missing the signal layer for
> observability. Without it, you do not really see if the system is
> pulsing in the right direction or just moving fast somewhere else.

Reply. This was the most actionable critique and shaped v2.2.0
directly.

What changed: the new
[`40_metrics.md` signal layer](/reference/artifacts#the-four-context-files)
records cycle time per FEATURE, drift count
(`plan-context.md` vs. real code), BA hypothesis validation status,
phase transition counts, and cross-phase trigger counts. Writes
happen inside existing phase actions, no separate metrics-collection
ceremony, no new tool. The Direction Session reads this file to
distinguish "moving in the right direction" from "moving fast
elsewhere".

### "Kanban has rhythm"

Björn Schotte (Mayflower GmbH):

> Kanban itself is based on rhythm, and you set your rituals at a
> pace the system needs. "Kanban has no rhythm" is wrong.

Vlad Georgescu (Optimistic Tech Leader):

> Why would Kanban not work with delivering full epics or full
> components multiple times per day? In a two-week sprint, instead of
> 20 stories, we might deliver 20 epics, each with 20 stories.

Reply. Both are correct that Kanban can carry a rhythm. Pure Kanban
is a pull system without prescribed cadences. With STATIK or
replenishment meetings, it gains the cadences explicitly.

PULSE is essentially Kanban with three explicit cadences bolted on.
The execution layer is a pull system. The coordination and product
layers add the rhythm that the team found missing when they tried
pure Kanban with agents working asynchronously at wildly different
speeds.

The broader point stands: bad planning was always bad planning,
agents or not. PULSE is not anti-planning, it is anti-ceremony. The
Direction Session is planning, just compressed and focused on
outcomes.

### "Decision provenance"

Yauheni Kurbayeu (Provenance Manifesto):

> The natural next step is decision provenance: preserving not only
> the artifacts but the decision lineage behind them, so teams and
> agents inherit the why, not just the latest file.

Reply. Provenance is exactly the design intent of the V-Model
artifact set.
[Living Documents](/concepts/living-documents) keep ADRs and FEATURE
specs in sync with the code. ADRs in MADR format record context,
decision, alternatives, and consequences. Backlog rows carry the
commit SHA back to the source feature. The
[traceability chain](/concepts/v-model#the-traceability-chain) means
any line of code traces back through the chain to a business
motivation in the BA.

The new `40_metrics.md` signal layer extends this to the trend level:
hypothesis status over time, drift count over releases, trigger
counts as a signal of where the workflow is straining.

### "Speed asymmetry is the real problem"

Ben Gusberg (AI for Partnerships, ex-Stanford):

> When anyone can ship a feature in an afternoon, the bottleneck
> moves to coordination and vision alignment almost overnight. Most
> teams are not ready for that shift.

Mattias Tronje (Transformation Lead):

> You are describing at team-scale what keeps breaking at org-scale.
> Three devs with three agents building three implementations is the
> micro version of three functions deploying three AI tools that
> cannot talk to each other.

Sami Niemelä (Head of Design, In Parallel):

> Where many current processes fail to output sufficient quality is
> exactly that design is only a box in the process instead of
> horizontal capability throughout.

Reply (collected). All three are pointing at the same edge: PULSE was
designed for a single-team, single-codebase setting. Cross-team flows
need a layer above PULSE that PULSE does not yet describe. Design as
a horizontal capability is similarly a gap, not a position.

These are open. The repo is open source for exactly this reason:
teams that stretch PULSE past its current scope will find the
breakpoints first, and contributions back are the way the framework
matures.

## References

- [LinkedIn article: Introducing PULSE](https://www.linkedin.com/in/sebastian-hanke-product/) (April 2026)
- [V-Model concept](/concepts/v-model)
- [Living Documents pattern](/concepts/living-documents)
- [Handoff Rituals (with Dialog handoffs)](/concepts/handoff-rituals)
- [Verification Gates](/concepts/verification-gates)
- [Artifacts reference](/reference/artifacts)
- [Conventions (Pair IDs)](/reference/conventions#pair-ids-concurrent-agent-coordination)
- [GitHub repository](https://github.com/pssah4/digital-innovation-agents)
