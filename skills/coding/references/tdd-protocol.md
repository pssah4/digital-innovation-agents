# TDD protocol (default active)

TDD is the DEFAULT for every implementation task in `/coding`. The
skill hands this rule to the coding agent for the session. Opt-out
exists only for the three exceptions below, each requiring explicit
user confirmation and a PLAN Change Log entry naming the exception.
The user can opt out for a session by starting `/coding` with a
`--no-tdd` hint; that too lands in the Change Log.

**The rule:** No production code without a failing test written first.

**The cycle:**

1. **RED:** Write a failing test (one behavior, one assertion).
2. **Verify RED (with evidence, binding):** BEFORE running, state the
   expected failure signature (for example
   `expected AssertionError: sorted == True, got False`). Run the
   test. Quote the actual failure output VERBATIM (at least the
   failing assertion or error line). Then give the verdict:

   ```
   Expected: <failure signature stated before the run>
   Observed (verbatim): <actual output line(s)>
   RED verdict: pass | fail
   ```

   The observed output must match the stated expectation. A test that
   passes immediately, fails with a syntax error, or fails for a
   DIFFERENT reason than stated is a failed RED step: fix the test and
   repeat. Never proceed to GREEN on a failed RED.
3. **GREEN:** Write the minimal code to pass the test (no more).
4. **Verify GREEN:** Run the test. It MUST pass, no other tests broken.
5. **REFACTOR:** Clean up while keeping tests green (no new behavior).

**Bug fixes are always test-first:** write the failing test that
reproduces the bug, then the fix (see the debugging protocol and the
regression test cycle).

**Exceptions (only with explicit user confirmation, logged in the
PLAN Change Log):**

- Throwaway prototypes
- Generated code
- Configuration files
