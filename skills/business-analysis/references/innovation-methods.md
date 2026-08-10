# Innovation method catalog (trigger -> method lookup)

Runtime trigger logic. The user-facing method cards with step-by-step
guidance live under `docs/reference/methods-{discovery|ideation|validation}.md`;
always link the matching card when proposing a method. Proposal wording
lives in SKILL.md ("Core principle: propose methods when input has
gaps").

## Discovery (cards: `docs/reference/methods-discovery.md`)

| When (trigger) | Method | In a nutshell |
|---|---|---|
| Answers to "why is that a problem" feel like guesses | Qualitative interview | One open 60-90 min conversation, verbatim notes, extract raw observations |
| Problem space fuzzy; verify it exists before deep research | Explorative interviews | 7-10 short conversations, cluster the surprises |
| Average users give generic answers | Extreme users | Interview power users and quitters; they bracket the design space |
| Regulatory/technical questions beyond the user | Expert conversations | 30-45 min with a domain expert, one specific question |
| Described workflow contradicts reality | Fly on the wall | Silent observation, 60+ min: actions, workarounds, hesitations |
| Nobody has experienced the problem first-hand | Self-test (immersion) | Walk the process yourself, log friction, verify with real users |
| Behaviour happens in private / over weeks | Cultural probes | Diary kit for 4-6 users, 1-2 weeks, debrief per participant |
| Insights exist but needs are unranked | User motivation analysis | Cluster insights into needs and obstacles, rank frequency x intensity |
| Too much data for one persona | Persona synthesis cluster | Affinity-cluster by behaviour, one persona seed per cluster |
| Design decisions drift, user too abstract | Persona | One evidenced, named persona, one page max |
| B2B, buyer is not the end user | Value proposition chain | Map actors and hand-offs, find where value leaks |
| Problem too broad to interview about | Research mind map | Decompose into 4-6 research fields, prioritise, assign |
| Unclear who to talk to, political friction | Stakeholder map | Influence-by-interest matrix with labelled relationships |
| No competitors named, trend risk | Market and trend analysis | Desk research, 4-6 theme clusters, one potential field each |
| Pain lives in one phase of usage | User journey | Stage map with four lanes, emotion line shows where to intervene |

## Ideation (cards: `docs/reference/methods-ideation.md`)

| When (trigger) | Method | In a nutshell |
|---|---|---|
| Sharp HMW, empty solution space | Brainstorming | 15-20 min group session, one HMW, cluster without evaluating |
| Loud voices dominate | Brainwriting | Silent 6-3-5 grid passing, 30 min |
| Seed idea too thin to prototype | Idea tower | Additive-only enrichment, one element per person per round |
| Complex problem needs soak time | Collective notebook | Personal notebooks for 1-2 weeks, one synthesis session |
| Team repeats the same 3-4 ideas | Inspiration cards | Random unrelated cards force new associations |
| 30-50 ideas, no shortlist | Idea clustering and selection | Cluster, score on max 4 criteria, top three; scores aid, not verdict |
| Nobody can say why users would switch | Jobs to be done | Functional, emotional, social job; hiring and firing criteria |
| Genuine technical contradiction | TRIZ | Contradiction matrix -> inventive principles -> one idea each |
| Team too close to the product | Kill your company | Attack your own product as a startup, then write the defence |

## Validation (cards: `docs/reference/methods-validation.md`)

| When (trigger) | Method | In a nutshell |
|---|---|---|
| Early feedback needed before code | Wireframes / paper prototypes | Sketch the risky part, watch a user hesitate, iterate |
| Visual direction untested | Appearance prototype | 1-3 visual variants, 10-second cold exposure, verbatim reactions |
| Success depends on the environment | Context and system prototypes | Smallest version that survives the real context, days to weeks |
| Feature expensive, usage unproven | Wizard of Oz | Visible surface, human behind it, 6-8 users |
| Navigation or taxonomy confuses | Card sorting | Users cluster 30-60 cards; their labels become navigation |
| Findings pile up across sessions | Test grid | Criteria rows x session columns, scan rows for patterns |
| "Can this even exist?" | Expert review | One pager + three focused questions to a specific expert |
| Idea passed user testing | Business plan | Canvas with one sentence per field, rough numbers, mark assumptions |
| Competing value propositions | Value proposition quantification | Score 4-6 dimensions 0-10 against evidence, weakest = next test |
| Team too optimistic before commit | Pre-mortem | "It failed, why?" silent writing, cluster, assign preventions |

## Probing techniques (inside interviews, both directions)

- **5-Why:** ask "why is that a problem?" up to five times.
- **Concretisation:** "Give me a concrete example." "When did this last happen?"
- **Future projection:** "Problem solved tomorrow, what changes?"
- **Perspective shift:** "What would your customer / boss / another industry say?"
- **Emotional level:** "How did that feel? What frustrated you most?"
- **Analogy trigger:** "Where have you seen this pattern before?"
- **Contrast:** "What if it were the opposite? Worst case?"

## Anti-patterns

- No method without a trigger; if the input is sufficient, keep going.
- Light before heavy (explorative before qualitative, self-test before
  cultural probes).
- Never dump a method name and disappear; help prepare the artifact.
- The agent never runs interviews, observations, or tests. It prepares
  and synthesises; the user runs the method.

Anchors follow VitePress slug rules (lowercase, spaces to hyphens,
parentheses dropped).
