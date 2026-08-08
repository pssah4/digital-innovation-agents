# Hotfix lane (fix-now, document-after)

Trivial bugs may fix first, document after, when ALL FIVE hold: at
most 3 files; no new feature or dependency; no breaking change to a
public API; under 15 minutes; existing FEAT as parent. Any miss ->
standard bug-capture flow.

Flow when allowed:

1. Fix immediately; run relevant tests.
2. Write the FIX BACKLOG row and detail file. Commit
   `fix: FIX-{ee}-{ff}-{nn} <desc>` with `Refs:` trailer.
3. In `github-sync` mode:
   `gh issue create --title "FIX-{ee}-{ff}-{nn}: {slug}" --label "fix,hotfix"`,
   then `python3 tools/github-integration/flow.py sync-status --item FIX-{ee}-{ff}-{nn}`.
4. Always close with
   `python3 tools/github-integration/flow.py validate-fix --item FIX-{ee}-{ff}-{nn}`.
5. Acknowledge in chat: modified files, FIX-ID, issue URL,
   validate-fix verdict.

The regression-test cycle still runs; the 15-minute budget includes
the test.

Four safety nets keep the lane honest:

- **FIX row** in BACKLOG.md (mandatory, even retroactively).
- **Commit cites FIX-ID** in subject and `Refs:` trailer.
- **Deferred-stub markers** bind `// FIXME(stub): ... -- see FIX-{id}`
  to the FIX row's Notes column.
- **Regression-test cycle** writes a `## Regression test` entry.

`validate-fix` runs the hotfix-scoped consistency check: FIX row
exists with correct id and refs; at least one commit cites the id; no
orphan `FIXME(stub):` references.

Anti-misuse: if hotfixes exceed 30% of an iteration, the lane is
being abused as a process bypass; file a quality-debt item.
