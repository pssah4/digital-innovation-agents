# Verification gate -- reachability and activation-path subtypes

Detail rules for Phase 4a step "Verify" claims. The SKILL.md keeps a
4-row Claim / Required-proof / Pass-Fail table; this file carries the
deeper subtype rules.

## Reachability subtypes

For every new top-level symbol introduced in a session (class, function,
module, command, route, handler, tool registration), verify a caller
exists outside the definition file and outside test files.

- `subtype: user-facing` (default): caller MUST exist outside definition
  file and outside tests. A symbol that compiles but is never called
  fails the check.
- `subtype: library`: caller MUST exist OR the symbol is exported as a
  public API entry point and documented as such.

On fail, the FEATURE Done-status is locked. Options:
1. Wire it up (add the caller).
2. Demote `subtype:` to `library` with public API documentation.
3. Open a `FIX-{ee}-{ff}-{nn}` row with the note `Wiring offen` and
   keep the FEATURE at `In Progress` in the backlog.

Stack-specific tooling for the reachability scan lives in
`reachability-by-stack.md`. Projects may override via
`dia.config.json -> reachability_check`.

## Activation Path entry types

For every FEATURE moving to Done in this session, read the
`## Activation Path` section in the FEATURE spec and verify each entry
exists in the code (grep or AST query). The string in the FEATURE spec
MUST match an actual identifier in the code.

| Type            | Required proof                                            |
|-----------------|-----------------------------------------------------------|
| command         | command name registered in command registry              |
| route           | route path registered in router                          |
| UI-element      | element rendered in component tree or template           |
| endpoint        | handler registered with the framework                    |
| scheduled-job   | schedule registered with the scheduler                   |
| tool            | tool name registered in the agent tool registry          |
| hotkey          | hotkey registered with the platform                      |
| public-API      | symbol exported in the package's public surface          |

On fail, the FEATURE Done-status is locked.

## Forbidden language without fresh verification

- "should work", "probably okay", "looks good"
- "tests should be green now"
- "the change should fix the bug"
- Any statement implying success without running the command.

## What is not enough (common failures)

| Claim            | Sufficient proof                                |
|------------------|-------------------------------------------------|
| Tests pass       | Test command output with 0 failures             |
| Linter clean     | Linter output with 0 errors                     |
| Build works      | Build command with exit code 0                  |
| Bug fixed        | Test reproducing the original symptom passes    |
| Subagent done    | VCS diff shows the expected changes             |
| Requirements met | Line-by-line checklist against the plan         |
