# Backlog as single source of truth

The BACKLOG row is authoritative for state. Every status-changing
skill follows the same sync chain; the row exists BEFORE the artifact
body, and the row changes BEFORE the body changes.

## Feature lifecycle (canonical sequence)

```
1. BACKLOG ROW      -- Create row in _devprocess/context/BACKLOG.md
                       FIRST. Status=Ready, Phase=Building, Refs={Epic}.
2. CLAIM            -- Set Claim column to {pair-id} @ {date}
3. FEATURE-SPEC     -- Write the substance (description, SC, NFRs)
                       AFTER the row exists. No status field in
                       frontmatter.
4. PLAN             -- Persist the plan as PLAN-{ee}-{ff}-{nn}, append
                       the PLAN id to the feature's Refs column
5. IMPLEMENTATION   -- Code, build, test after each step. Backlog row
                       reflects status (In Progress -> In Review).
6. SPEC UPDATE      -- Feature spec stays the substance reference
                       (success criteria verified, NFRs honored). Code
                       paths NEVER added to the spec.
7. WAYFINDER UPDATE -- New entry-point landed: update
                       src/ARCHITECTURE.map and write the JSDoc header
8. BACKLOG UPDATE   -- Status=Done, commit SHA, claim cleared
```

## Sync chain at every status change (binding)

1. Update the BACKLOG row (status, phase, claim, refs, commit SHA)
   BEFORE touching the artifact body.
2. Keep the row's Refs column complete: every ADR, PLAN, FIX, IMP that
   belongs to the item appears there. The relation graph derives from
   this column.
3. Detail files carry substance, never state. No status in
   frontmatter (N-15).
4. On completion: Status=Done, commit SHA in the Commit column, claim
   cleared, one line appended to `BACKLOG-HISTORY.md`.
5. Defaults for new rows: `Status=Ready`, `Phase=Building`,
   `Source={producing skill}`, `Prio` from the item's BA or the user.

See the Concurrent-agent coordination section in
`skills/dia-guide/SKILL.md` for the Claim protocol and
conflict-resolution rules when multiple pairs work in parallel.
