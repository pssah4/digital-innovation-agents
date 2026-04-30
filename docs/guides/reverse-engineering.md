---
title: Reverse Engineering
description: Brownfield entry point for the V-Model workflow. Walk the V backwards to turn an existing codebase into evidence-based V-Model artifacts.
---

# Reverse Engineering

`/reverse-engineering` is the brownfield entry point for the V-Model workflow. Most real projects are not greenfield. When you land in an existing codebase (legacy, inherited, or organically grown), you cannot start with Business Analysis. The code already exists, the decisions have already been made, and the knowledge about why things are the way they are is scattered across people's heads, outdated wikis, and commit messages.

This skill rebuilds the artifacts that should have existed from day one, so the team has a stable, shared project context to carry forward.

## Walk the V backwards

The forward V-Model walks from Why to What to How to Code. Reverse engineering walks the same V in the opposite direction.

```
Code  →  Architecture  →  Requirements  →  Business Analysis
(facts)  (decisions)      (capabilities)   (Why, draft only)
```

Each level is filled with what you can prove from the code or from the existing documentation. Nothing else. The output is a foundation, not a product. The team validates it in the forward walk.

::: info Why backwards?
Because that is the only direction in which you have evidence. The code is ground truth for the How. You can read the tech stack, the architecture style, the routes, the tests. But the code cannot tell you whether the product solves the right problem, who the real users are, or which hypotheses the team was originally testing. That knowledge lives outside the repository, and reverse engineering refuses to fabricate it.
:::

## When to use this entry point

Use `/reverse-engineering` when:

- You are onboarding an existing codebase into the V-Model workflow.
- You inherited a legacy system without architecture documentation.
- A team already shipped a PoC or MVP and now needs a proper context.
- You want to run `/coding` on code you did not write and the [`plan-context.md`](../concepts/living-documents) does not exist yet.
- Architecture decisions exist in the code but not as ADRs.
- Nobody on the team can answer "why did we choose X?" with confidence.

If the problem space is unclear and no code exists yet, start with [`/business-analysis`](./business-analysis) instead. Reverse engineering is a brownfield tool.

## The anti-hallucination contract

This is the most important part of the skill and the reason it exists as its own phase instead of being rolled into BA or Architecture.

Every sentence this skill writes has to obey three rules:

1. **Source per claim.** Every non-placeholder sentence carries a `Source:` line pointing at concrete evidence.
   - Code: `Source: src/api/auth/handlers.ts:42-58`
   - Docs: `Source: README.md § "Getting Started"`
   - Config: `Source: package.json "dependencies.prisma"`

2. **No source means placeholder, not guess.** If no source can be found, the section is marked `[NEEDS USER INPUT, no evidence found]`. The skill does not write a "reasonable assumption" in its place.

3. **Status markers everywhere.** Every artifact carries a status in its frontmatter: `Snapshot`, `Inferred from codebase`, `Observed (not validated)`, `Draft (reverse-engineered)`. There are no silent documents.

These rules are non-negotiable because the cost of a hallucinated persona or an invented problem statement is enormous. The team carries it forward through RE and Architecture, and nobody notices until a feature misses its real users by a wide margin.

::: warning Code is not user research
You will never infer personas from route names, directory names, or endpoint signatures. `/users/:id/settings` tells you the system has users. It does not tell you who they are, what they want, or why the product exists. The persona section stays as `[NEEDS USER INPUT]` unless the README or marketing copy explicitly names a user type.
:::

## Phased workflow

The skill walks up the V in six phases. Each phase produces its own artifact before moving to the next level.

### Phase 0: Scope and codebase scan (5 to 10 min)

Pick the depth, same three tiers as `/business-analysis`.

| Scope | Depth | Typical duration |
|---|---|---|
| Simple Test | Single-module onboarding | 30 to 60 min |
| Proof of Concept | Tech stack, 3 to 8 ADRs, 5 to 15 features, BA draft | 1 to 3 h |
| MVP | Full arc42, 8+ ADRs, 15+ features, complete BA draft, backlog seed | 3 to 8 h |

Then scan the repository for the inventory you will draw from.

- Package and build manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`).
- Top-level directories and their apparent purpose.
- Entry points, test directories, CI config.
- Lint, format, and type-checker configs.
- Existing documentation (`README.md`, `docs/`, `CHANGELOG.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`).

This becomes the Codebase Map, the only set of sources allowed for the rest of the walk.

### Phase 1: Tech stack to plan-context.md

Extract the concrete stack from manifests and entry points. For each layer, cite the source.

```markdown
- **Runtime:** Node.js 20 (package.json "engines.node": ">=20")
- **Language:** TypeScript 5.4 (tsconfig.json, devDeps)
- **Framework:** Next.js 14 App Router (package.json "next": "14.x")
- **Database:** PostgreSQL via Prisma (prisma/schema.prisma)
- **Auth:** NextAuth 5 (package.json "next-auth": "5.x")
- **Testing:** Vitest and Playwright (vitest.config.ts, e2e/)
```

The result goes into `_devprocess/requirements/handoff/plan-context.md` with status `Snapshot from existing code`. `/coding` can start from this file on day one. It is the same document the forward `/architecture` skill produces.

### Phase 2: Architecture reverse engineering to ADRs and arc42

Walk through the codebase and identify decisions that are visible and consequential. Typical candidates:

- Database engine and ORM choice.
- API style (REST, GraphQL, RPC) and framework.
- Frontend framework and state management.
- Auth and session strategy.
- Deployment target (serverless, container, VM).
- Package manager and monorepo tooling.
- Observability stack.
- Testing strategy.

For each, write one ADR in MADR format with `Status: Inferred from codebase`. The `Alternatives considered` block stays as `[NEEDS USER INPUT, not visible in code]` unless the alternatives are mentioned in a comment or a doc.

Then build `_devprocess/architecture/arc42.md` as a snapshot. Fill only the sections you can back with sources.

- **§1 Goals:** from README, or placeholder.
- **§2 Constraints:** from engines, CI targets, license.
- **§3 Scope and Context:** from entry points and external integrations.
- **§4 Solution Strategy:** reference the inferred ADRs.
- **§5 Building Blocks:** from top-level directories and module boundaries.
- **§7 Deployment:** from CI config, Dockerfile, k8s manifests.
- **§8 Crosscutting:** from config (auth, logging, error handling).

Sections §6 Runtime View and §9 through §12 stay as placeholders unless explicit evidence exists. arc42 lets you leave sections empty when you have nothing to say. That is a feature, not a bug.

See the [Architecture guide](./architecture) for the full arc42 and ADR structure.

### Phase 3: Functional reverse engineering to FEATURE inventory

A feature is anything the system lets a user (or an API consumer) do. Sources:

- Routes, controllers, CLI commands, public API endpoints.
- Rendered pages, navigation entries.
- Public exports if the project is a library.
- Test descriptions (`describe('user can ...')`, `it('admin should ...')`).

For each, write a `FEATURE-XXX-slug.md` with `Status: Observed (not validated)`. The Feature Description comes from the code. Benefits Hypothesis, User Stories, and Success Criteria stay as `[NEEDS USER INPUT]`. Those come from the forward walk through `/business-analysis` and `/requirements-engineering`.

### Phase 4: Business reverse engineering to BA draft

This is the most constrained phase. Read:

- `README.md` for intro, use cases, motivation.
- `docs/` or `documentation/` content.
- `package.json` or `pyproject.toml` description and keywords.
- `CHANGELOG.md` for historical goals and removed features.
- Landing-page copy if present in the repo.
- Issue and PR templates if they describe target users.

Fill the BA template section by section, obeying the evidence rule.

| BA section | Fill from | If no source |
|---|---|---|
| Project purpose and scope | README intro | `[NEEDS USER INPUT]` |
| Primary persona | Explicit user-type mention in docs (quoted) | `[NEEDS USER INPUT]` |
| Problem statement | README motivation section | `[NEEDS USER INPUT]` |
| HMW question | Only if docs contain an explicit problem | `[NEEDS USER INPUT]` |
| Value proposition | README or marketing copy | `[NEEDS USER INPUT]` |
| Jobs to be Done | Only if docs mention concrete jobs | `[NEEDS USER INPUT]` |
| Idea Potential, Pricing, Competitors | Only if explicitly documented | `[NEEDS USER INPUT]` |
| Critical hypotheses | Only if docs mention tested assumptions | `[NEEDS USER INPUT]` |

Every non-placeholder sentence carries a `Source:` line.

When you finish, count two numbers:

- `filled-from-sources`: how many sections are evidence-backed.
- `needs-user-input`: how many sections are placeholders.

Both counts go into the BA header so `/business-analysis` can enter Validation Mode and knows exactly how much work remains.

### Phase 5: Backlog extraction to BACKLOG.md

Scan for:

- `TODO`, `FIXME`, `HACK`, `XXX` comments in code.
- Failing or skipped tests (`.skip`, `xit`, `pytest.mark.skip`).
- Undocumented env vars (referenced in code but missing from `.env.example`).
- Observable features without matching test files.
- Outdated dependencies or major versions pinned to old releases.
- Missing CI steps (no security scan, no type-check, no linter).

Append each finding as a `BL-NNN` entry with priority `P2` by default and a `Source:` line pointing at the evidence. The team will reprioritise during BA and RE.

### Phase 6: Handoff to `/business-analysis`

The handoff follows the standard three-part [Handoff Ritual](../concepts/handoff-rituals).

1. Artifact report with counts (plan-context, ADRs, features, arc42 sections, backlog entries) plus the BA coverage ratio (filled over total).
2. Handoff context entry in `_devprocess/context/HANDOFFS.md` with scope, risks, gaps, and recommended next phase (always `/business-analysis`).
3. Transition question. "Shall I start `/business-analysis` now in Validation Mode, or do you want to review the draft first?"

On agreement, `/business-analysis` detects the reverse-engineered BA draft automatically and walks through every `[NEEDS USER INPUT]` marker with the user, one section at a time. Evidence-backed claims get confirmed. Placeholders get filled. Each validated section gets its status promoted from `Draft` to `Validated`.

::: info One skill, two entry points
The forward and backward walks converge here. Whether the project started with `/business-analysis` or `/reverse-engineering`, the BA document is the same file at the same path, and every phase downstream (`/requirements-engineering`, `/architecture`, `/coding`) treats it identically. Reverse engineering is not a side track. It is a seed for the forward walk.
:::

## Quality gates

Before the Handoff Ritual, the skill verifies:

1. Every non-placeholder sentence has a `Source:` line.
2. Every file has a status marker.
3. No invented personas. Persona content must quote the source.
4. No invented HMW. Same rule.
5. FEATURE count matches observable capabilities. If the code has 12 routes and you produced 4 features, you under-counted. If you produced 30, you over-fragmented.
6. Backlog is non-empty for anything but a pristine codebase.

If any gate fails, the skill fixes it before handing off. The user will not catch silent hallucinations. The gates are the skill's responsibility.

## Read the skill file

Want to see the exact instructions the agent follows? [`skills/reverse-engineering/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/reverse-engineering/SKILL.md) on GitHub.

## Further reading

- [Business Analysis guide](./business-analysis). The forward walk takes over here, starting in Validation Mode.
- [Architecture guide](./architecture). The ADR and arc42 structure the skill uses.
- [Living Documents concept](../concepts/living-documents). Why the reverse-engineered artifacts are meant to evolve.
- [V-Model concept](../concepts/v-model). How both entry points feed into the same workflow.
