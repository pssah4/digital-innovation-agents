# tools/internal

Internal lock files used by DIA refactor work. These are NOT part of the
public skill set and the stripped public mirror omits them.

## anchor-lock.json

Inventory of every H2/H3 heading, frontmatter key, inline marker, and
filename pattern that `tools/` and `skills/consistency-check/` parse
with regex or string matching. Generated during the v3.6.0 artifact
shrink to prevent silent tool breakage when templates are restructured.

**Rule:** any string listed in `heading_anchors`, `frontmatter_keys`,
or `inline_markers` is immutable across the shrink. Renaming requires
a coordinated change in every file under `used_by`, plus a migration
script for existing user-project artefacts.

When you add a new anchor that another tool starts parsing, append it
here and re-check the skill SKILL.md and template files for the exact
string.
