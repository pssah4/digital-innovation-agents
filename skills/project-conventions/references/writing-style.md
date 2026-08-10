# Writing style (canonical home)

The writing style applies to every artifact produced by every V-Model
skill (BA, EXPLORE, EPIC, FEATURE, ADR, arc42, plan-context,
architect-handoff, backlog rows, FIX, IMP, audit reports, release
notes, CHANGELOG, METRICS). It applies to prose written at runtime,
not only to templates. `/humanizer` uses the same blacklist; this file
is its single home inside the plugin.

**Zero em dashes, zero en dashes.** No U+2014, no U+2013, no
double-hyphen substitute written as two ASCII hyphens to fake an em
dash. Use a period, a comma, parentheses, or a plain `and` / `but`.
The user has explicitly said they hate em dashes; every single one is
a regression.

**Pre-save scan (binding).** Before writing or editing an artifact,
the producing skill mentally greps the output for:

- U+2014 (em dash), U+2013 (en dash): zero hits required.
- AI vocabulary: `landscape`, `nuanced`, `delve`, `leverage`,
  `utilize`, `intricate`, `crucial`, `pivotal`, `robust`,
  `seamless`, `game-changing`, `revolutionary`, `unlock`,
  `empower`, `comprehensive`, `holistic`, `foster`, `ensuring`,
  `highlighting`, `underscoring`, `emphasizing`, `reflecting`,
  `symbolizing`.
- Negative parallelisms: `not X but Y`, `it is not about A, it is
  about B`, `more than just X`. Rewrite to the positive form.
- Filler phrases: `in order to`, `it is important to note`,
  `needless to say`, `due to the fact that`.
- Inflated symbolism: `at its core`, `fundamentally`, `the real
  question is`, `this matters because`.
- Copula avoidance: `X serves as Y`, `X stands as Y`. Write `X is Y`.
- Superficial -ing tails: `highlighting the importance of X`,
  `reflecting the commitment to Y`.
- Rule-of-three padding: if a default list has exactly three parallel
  items, drop to two, add a fourth, or rewrite.
- Vague attributions: `it is often said`, `many believe`, `experts
  argue` (unless a source is named).
- Meta-signposting: `let me break this down`, `here is what you need
  to know`. Write the content instead.
- Promotional language, boasting adjectives.

**Active voice by default. Sentence case in headings.** No title case.

Any hit is rewritten before the artifact is saved. This applies
equally to brand-new artifacts, edits, and promotions from draft to
validated.

**Templates follow the same rule.** Every `skills/*/templates/*.md`
file is held to the same standard. When a skill copies a template into
`_devprocess/`, it copies the clean version, and any prose it fills
into the placeholders is written in the same style.
