# User Interaction Protocol (binding for every V-Model skill)

When any phase skill, the guide, or the bootstrap needs a decision
from the user, these rules are mandatory. They apply inside
`/dia-guide` and when any skill is invoked standalone, regardless of
project language.

1. **One question per turn.** Never batch multiple open decisions into
   one message. Finish Q1 (ask, wait, receive answer) before asking
   Q2. If three decisions block progress, ask the first, wait, then
   ask the next. Sequencing beats efficiency; users reason about one
   thing at a time.
2. **Use the `AskUserQuestion` tool.** Plain markdown lists force the
   user to type back; the tool gives clickable options plus a
   free-text "Other" slot. Free-form prose questions in chat are only
   for quick factual confirmations, not for decisions between
   alternatives.
3. **Every option states BOTH a Pro and a Con, explicitly labelled.**
   Format the `description` field so the trade-off is scannable:

   ```
   + Pro: one short sentence stating the main upside.
   - Con: one short sentence stating the main downside or cost.
   ```

   Descriptions that list only advantages (or only risks) are a bug.
   The user decides by comparing, so both sides must be visible. The
   `+ Pro:` / `- Con:` labels stay in English regardless of dialog
   language so both sides are visually identifiable at a glance.
4. **Mark the recommended option as the first entry** with
   "(Recommended)" in its label. If the rationale is not obvious from
   the Pros/Cons alone, add a one-line "Empfehlung: ... weil ..."
   sentence in the turn text BEFORE the `AskUserQuestion` call.
5. **No "dealer's choice" framing.** If you genuinely have no
   preference, say so in the lead-in text; do not silently drop the
   recommendation.
6. **Exceptions:** quick factual confirmations ("Proceed with the
   well-known Y/N step?") may stay as plain prompts. The rules target
   decisions between alternatives, not acknowledgements.
