---
title: Skill Authoring Style Guide
description: Conventions for writing and reviewing skills so that the whole set reads like one voice and triggers reliably.
---

# Skill Authoring Style Guide

Skills in this repository are user-facing prose. A skill that reads badly
or triggers unpredictably does more harm than no skill at all. This
document is the shared baseline for authors and reviewers.

## Anatomy of a skill

Every skill is a directory under `skills/`:

```
skills/<phase>/
├── SKILL.md          # required -- the skill itself
├── references/       # optional -- long-form material loaded on demand
└── templates/        # optional -- artifact scaffolds
```

`SKILL.md` has two parts: YAML frontmatter and Markdown body.

### Frontmatter

```yaml
---
name: <phase>
description: >
  One or two sentences describing what the skill does, followed by
  trigger keywords the model can match against. Triggers matter more
  than elegance; write for selection, not for reading.
disable-model-invocation: false
---
```

Rules:

- `name` must equal the directory name. This is enforced by
  `scripts/validate-skills.sh`.
- `description` is the selector. Keep it under 2000 characters; aim
  for 200--800. Include concrete trigger words the user would actually
  type.
- `disable-model-invocation: true` means "only run when explicitly
  invoked" -- use for orchestrators (`v-model-workflow`) and skills
  with side effects (`security-audit`).

### Body

Structure the body so a reviewer can skim:

1. **Purpose.** One paragraph. Who calls this, why, what they get.
2. **Inputs and outputs.** What the skill reads, what it writes. Be
   explicit about paths under `_devprocess/`.
3. **Workflow.** The steps the skill performs. Numbered lists beat
   prose.
4. **Quality gates.** What the skill refuses to do, what it escalates.
5. **Keywords.** Bottom of file. Repeats the triggers so Ctrl-F finds them.

## Voice

- **Write for the operator, not the framework.** Second person ("you")
  is fine when giving instructions to the model; avoid first-person
  plural.
- **Short sentences.** If a sentence has two "and"s, break it up.
- **No buzzwords unless defined.** "Holistic", "synergy", "leverage"
  without a specific meaning slow readers down. If a term is
  methodology-specific (Jobs to be Done, ASR, NFR), link to where it
  is defined.
- **Advisory, not enforcing.** Skills guide; they do not gate. Respect
  user opt-outs immediately.
- **Stay in English.** The repository voice is English. Translated
  variants may come later, but authors write in English so the whole
  set reads consistently.

## Length

| Section | Budget | Why |
| --- | --- | --- |
| `description` | 200--1500 chars | long enough for triggers, short enough to stay in attention |
| `SKILL.md` body | 200--600 lines | beyond this, split into `references/` |
| `references/*.md` | unlimited | loaded on demand, not in selector |
| `templates/*.md` | unlimited | user copies these; they are not read by the model |

If a skill body exceeds the budget, the usual cause is prose where a
list would do, or material that belongs in `references/`.

## What goes in `references/`

Anything the skill occasionally consults but does not always need:

- Deep method descriptions (interview techniques, scoring matrices)
- Example artifacts
- Cross-platform adaptation notes
- Historical context

`SKILL.md` references these by relative path. The model loads them
only when the current task needs them.

## What goes in `templates/`

Scaffolds the user (not the model) copies into `_devprocess/`:

- Epic, Feature, Bugfix, Improvement, Issue templates
- arc42 template, ADR template
- Checklist templates

Templates are artifacts, not instructions. Keep them filler-free so the
user sees empty slots rather than stock phrases to edit away.

## Review checklist

Before approving a skill PR, check:

- [ ] Frontmatter parses (`bash scripts/validate-skills.sh` passes)
- [ ] `description` includes at least three concrete trigger words
- [ ] Inputs and outputs are explicit (paths, file names, expected state)
- [ ] Workflow steps can be performed top-to-bottom without jumping
- [ ] Nothing in the body duplicates what `project-conventions`
      already says
- [ ] References and templates are linked, not pasted
- [ ] Voice matches the existing set (short sentences, advisory tone)

## Common mistakes

**Descriptions that read well but trigger badly.** A polished sentence
with no noun phrases the user would type is useless to the selector.
Write *"Use when the user mentions 'ADR', 'arc42', 'architecture
decision'"* explicitly.

**Skills that do two jobs.** If you find yourself writing "this skill
also...", split it. One skill, one purpose.

**Instructions mixed with examples.** Put examples in `references/`
and link them. Keep `SKILL.md` the minimum the model needs.

**Copy-pasted phrasing across skills.** If three skills say the same
thing about `_devprocess/` structure, that content belongs in
`project-conventions` and the others link to it.

## See also

- [Versioning policy](./versioning.md) -- when a skill change is a
  breaking change
- [Artifact ownership](./artifact-ownership.md) -- which skill writes
  which file
