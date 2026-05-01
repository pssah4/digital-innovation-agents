---
title: Humanizer
description: Remove signs of AI-generated writing. Strip em dashes, AI vocabulary, negative parallelisms, and filler so the text reads like a human wrote it.
---

# Humanizer

`/humanizer` is the writing-style enforcer. It removes signs of
AI-generated text from any artifact (BA, FEAT spec, ADR,
README, commit message, release notes) so the result reads like a
human wrote it. The skill is based on Wikipedia's
[Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup/Signs_of_AI_writing)
guide.

## When to use

Trigger phrases that route to the skill: "humanize this", "remove
AI tells", "make this sound less like ChatGPT", "/humanizer".

The other DIA skills also reference these rules in their writing
output, so the worst patterns rarely make it into a final
artifact in the first place. `/humanizer` is the explicit pass
when:

- A draft was generated quickly and reads stilted
- A team member pasted AI-generated copy into the repo
- A release note or README needs final polish
- A `/consistency-check` Mode B run flagged style drift

## What it removes

### Punctuation

- **No em dashes (U+2014), no en dashes (U+2013).** Use periods,
  commas, parentheses, "and", or "but" instead. Em dashes are the
  most reliable AI tell.
- **No rule-of-three lists where one example will do.** "fast,
  reliable, and scalable" reads like a marketing brochure. Pick
  the one that matters.

### Vocabulary

The skill flags and rewrites the following words on sight:

| Word | Why it gets flagged |
|---|---|
| `landscape` | Vague. What landscape? |
| `nuanced` | Hedge. Say what the actual subtlety is. |
| `delve` | Bot tell. Use "look at" or "examine". |
| `leverage` | Use "use". |
| `crucial` | Empty intensifier. |
| `robust` | Almost always meaningless. |
| `seamless` | Marketing word. |
| `holistic` | Means nothing on its own. |
| `foster` | Use "build" or "create". |
| `ensuring` | Use "so that" or split the sentence. |
| `highlighting` / `underscoring` | Bot transitions. Just say it. |

### Sentence patterns

- **No negative parallelisms.** "Not X but Y" is an AI tell. Say
  "Y" directly, or contrast both with concrete reasons.
- **No inflated symbolism.** "This represents a paradigm shift"
  almost always means "this is new". Say what is new.
- **No vague attributions.** "Critics argue" without naming the
  critic. Either name them or drop the sentence.
- **No superficial -ing analyses.** "highlighting the importance
  of..." is bot transition glue. Cut it.
- **No filler phrases.** "It is important to note that", "It
  goes without saying", "In today's fast-paced world".
- **No meta-signposting.** "In this section we will explore..."
  Just explore.

### Voice and tone

- **Active voice.** "The agent updates the backlog" beats "The
  backlog is updated by the agent".
- **Sentence case in headings.** "How the guide works",
  not "How The Guide Works".
- **First person where it fits.** "I keep coming back to..."
  signals a real person thinking. Avoid in objective reference
  docs; encourage in tutorials and PR descriptions.
- **Vary sentence length.** Short. Then longer ones that take
  their time. Algorithms produce uniform rhythm.

### Umlauts

In German artifacts:

- **Correct umlauts** (`ä`, `ö`, `ü`, `ß`) when the project file
  is Unicode-clean.
- **ASCII fallback** (`ae`, `oe`, `ue`, `ss`) only when the
  existing project file uses ASCII consistently. Do not mix.

## Voice calibration (optional)

If the user provides a writing sample (their own previous
writing), the skill matches the rewrite to that voice instead of
the default. Useful for personal blog posts, internal team docs,
or any artifact where the author has a recognisable style.

Inline: "Humanize this text. Here's a sample of my writing for
voice matching: ..."

File: "Humanize this text. Use my writing style from ./samples/
as a reference."

## What it does not do

- It does not "improve" technical accuracy. If the underlying
  claim is wrong, fix the claim first, then run the humanizer.
- It does not enforce length. A 300-word section may shrink to
  200 words after the AI tells are stripped, but the skill does
  not aggressively cut.
- It does not change the language of the artifact. German stays
  German, English stays English.

## Integration with other skills

Every other DIA skill follows the same writing rules in its
output. The `/humanizer` skill is the explicit pass when
something slipped through, or when older content needs cleanup.

The rules also apply to:

- Commit messages (every commit, every phase)
- Release notes (the Closing Handoff)
- README and documentation
- Skill prose itself (this very file)

If you read a DIA artifact and want to know whether it follows
the rules, run a quick grep:

```bash
grep -nP "[\x{2014}\x{2013}]|landscape|nuanced|delve|leverage|crucial|robust|seamless|holistic|foster|ensuring|highlighting|underscoring" {file}
```

Zero hits is the bar.

## Read the skill file

[`skills/humanizer/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/humanizer/SKILL.md)
on GitHub.

## See also

- [Project Conventions guide](./project-conventions): the
  binding writing-style rules
- [Conventions reference](../reference/conventions): the
  rules in one table
