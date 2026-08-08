# Bug-capture entry point (no implementation required)

`/coding` is also the entry point when the user reports a bug OUTSIDE
of an active implementation run ("ich habe einen Bug in Feature X
gefunden", "Login bricht ab"). The skill MUST be able to capture the
bug without forcing the user into an immediate fix. Flow:

1. Run the same Phase 0 triage. The user's prompt usually maps to FIX.
2. Identify the affected `FEAT-{ee}-{ff}` (ask if unclear).
3. Write the BACKLOG row first (status `Ready`, phase `Building`,
   priority from the user, Source `BUG`).
4. Create the detail file at
   `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` from
   `templates/FIX-TEMPLATE.md`. Fill Symptom and what is currently
   known about the cause; leave Fix and Regression test empty.
5. Run the phase-end commit (per `team-workflow.md`) with message
   `chore(fix): FIX-{ee}-{ff}-{nn} bug captured`. The commit creates
   the `fix/<id-lower>-<slug>` branch via the commit-boundary check.
6. Ask the user: "Bug erfasst. Soll ich jetzt den Fix implementieren
   (`/coding` Phase 1+ auf diesem Branch), oder reicht die Erfassung
   fuer jetzt?"

If the user picks "nur erfassen", the skill ends after the commit and
the bug waits in the backlog as a regular FIX item. The next `/coding`
invocation on that FIX-ID resumes from Phase 1.

The capture path is identical to the in-flight mid-course `bug`
trigger; only the entry condition differs. Both converge on the same
artefact shape: BACKLOG row + FIX detail file + branch.
