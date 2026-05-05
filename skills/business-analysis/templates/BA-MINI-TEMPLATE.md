---
type: ba
target-type: imp | fix
target-id: {IMP-EE-FF-NN | FIX-EE-FF-NN}
project-ba-ref: {path to BA-PROJECT.md, or null}
parent-feat: FEAT-EE-FF
personas: []                  # IDs from Project-BA, often empty for IMP/FIX
project-kpi-ref: []
scope: simple-test
created: YYYY-MM-DD
---

# Mini-BA: {Item title}

> Compact discovery for an Improvement or Fix where the cause or
> the value of the change is not obvious. Use only when the team
> would otherwise guess. For trivial changes, skip the BA and let
> `/coding` create the IMP/FIX artefact directly.
>
> Hard length cap 80 lines. If you need more, the item is probably
> a FEAT and should use `BA-TEMPLATE.md`.
>
> Status, phase, last-change, and claim live in the BACKLOG row,
> not here.

---

## 1. Observed behaviour

For FIX: what does the user see today that is wrong? Quote, error
message, screenshot path, ticket link. Two to four sentences.

For IMP: what does the user see today that works but is unsatisfying?
Friction point, drop-off, support theme.

---

## 2. Root cause hypothesis

Best current hypothesis for why the behaviour happens (FIX) or why
the gap exists (IMP). One paragraph. Mark unverified assumptions
with `Assumption:` so RE / Architect / coding know what still needs
proof.

---

## 3. Impact

Who is affected, how often, how badly?

| Dimension | Value |
|-----------|-------|
| Affected personas | {P1, P3 - referenced from Project-BA} |
| Frequency | {daily / weekly / per-release / one-off} |
| Severity | {blocker / major / minor / cosmetic} |
| Business impact | {one sentence, e.g. retention loss, revenue, support load} |

---

## 4. Acceptance

What does "done" look like, observable from outside the code?

- [ ] {observable acceptance criterion 1}
- [ ] {observable acceptance criterion 2}

For FIX: include a regression test condition. For IMP: include the
metric or qualitative signal that proves the improvement.

---

## 5. Risk and assumptions

- **Risk:** {one sentence on what could go wrong if we change this}
- **Assumption:** {what we assume to be true; flag the strongest
  assumption that, if wrong, would invalidate the BA}
- **Project-BA refs touched:** {persona IDs / value dimensions / KPIs
  affected, if any. Empty if purely technical}

---

Promotion: `/requirements-engineering` (or `/coding` for FIX) creates
`requirements/improvements/IMP-{ee}-{ff}-{nn}-{slug}.md` or
`requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` and writes
`ba-ref: ../../analysis/BA-{TARGET-ID}-{slug}.md` into its
frontmatter.
