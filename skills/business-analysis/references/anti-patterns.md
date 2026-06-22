# BA anti-patterns (detailed examples)

Linked from `skills/business-analysis/SKILL.md` ("Anti-patterns" section).
These are the long-form wrong/right pairs. The SKILL.md keeps only the
one-liner rules.

## Do not prescribe technical solutions

- Wrong: "We need a React app with PostgreSQL."
- Right: "We need a modern web application reachable from a browser."

The BA captures the problem, the user, and the value. Technology choices
belong in `/architecture` (ADRs).

## No vague problem statements

- Wrong: "The current solution is not good."
- Right: "The process takes 5 hours per week and produces a 20% error rate."

Quantify duration, frequency, error rate, cost, or user friction.
Without a number the problem cannot be measured after release.

## Always quantify KPIs

- Wrong: "Faster processing."
- Right: "Processing time from 5 hours per week to 1 hour per week
  within 3 months."

Every KPI carries baseline, target, and timeframe. Otherwise the
Post-Release Review (Phase 8) cannot classify the hypothesis as
Confirmed or Contradicted.

## Do not jump to solutions too early

- Wrong: Discuss the solution immediately after the problem statement.
- Right: Complete EXPLORE (User, Needs, Insights) first, then move to
  IDEATION via the HMW question.

The HMW is the only legal bridge from EXPLORATION to IDEATION. Solutions
formulated before EXPLORE is complete encode unverified assumptions.

## Do not forget How-Might-We

- The HMW question is the synthesis of EXPLORATION and the input for
  IDEATION.
- Without HMW the thread between problem and solution is missing, and
  the resulting solution cannot be traced back to a user need.

## Do not duplicate Project-BA content in Item-BAs

- Wrong: Re-list personas P1, P2 in every FEAT-BA with their full
  descriptions.
- Right: Reference them as `personas: [P1, P3]` and let the Project-BA
  hold the definitions. `/consistency-check` flags duplication.
