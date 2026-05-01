<!--
Instructions for the agent: produce this file as
`_devprocess/rules/domain.md`. Write the prose in the user's working
language. Keep section names in English.

Hard cap: 100 lines. Glossary entries that grow beyond a one-line
definition belong in `_devprocess/analysis/`, not here.
-->

# Domain rules for {project-name}

> Max 100 lines. Loaded when business logic or domain modeling is in
> scope.

## Glossary

| Term       | Definition                                                |
|------------|-----------------------------------------------------------|
| {Term-1}   | {one-sentence definition}                                 |
| {Term-2}   | {one-sentence definition}                                 |

## Business rules

- {e.g. "A user can hold at most N active workspaces simultaneously."}
- {e.g. "Sessions archive after 24h of inactivity."}
- {e.g. "Pricing: quantity x unit price, discount above 10 units."}

## Domain model (compact)

```
{Entity-1} --1:n--> {Entity-2}
{Entity-2} --n:m--> {Entity-3}
```

## Invariants

- {e.g. "Every session belongs to exactly one workspace."}
- {e.g. "No delete on entities with active references."}
