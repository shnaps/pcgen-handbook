---
name: lst-style
description: Writing and working rules for the PCGen Handbook. Use when drafting, editing or reviewing any page under docs/, when replying to the user, and when scoping a research agent. Enforces short plain sentences, active voice, consistent terminology, and the project glossary. Blocks filler and marketing words.
---

# PCGen Handbook writing style

Readers are developers who have never touched PCGen. They want to get something
working, then understand why it worked. Write for that.

## Scope

These rules cover `docs/` **and replies to the user**. Chat is not exempt. The cost
rules at the end cover any work on this repo, not only writing.

For replies:

- Lead with the answer. No preamble, no restating the question.
- A status question gets a status: "yes, working on it", "checking to confirm",
  "no, finished", "no, moved to a different task".
- No self-narration. Do not praise the question or announce what comes next.
- Add detail only when it changes what the user does next.
- Report a problem as one line of fact, not a story about finding it.

## Two modes

**Strict** — reference pages, syntax, procedures, `lst/reference/`, `lst/files/`.
Every rule below is enforced.

**Normal** — concept pages, internals prose, `start/`, `internals/`. Structural rules
enforced; the sentence-length cap is a target, not a hard limit.

## Structure

| Rule | Limit |
|---|---|
| Sentence length, instructions | 20 words |
| Sentence length, explanation | 25 words |
| Paragraph length | 6 sentences, one topic |
| Noun stacks | 3 words max |
| Semicolons | none |
| Instructions per sentence | one |

- Active voice. Imperative for steps: "Open the file", not "The file should be opened".
- Explicit subjects and verbs. Keep articles even when they cost a word.
- Vertical lists for sequences and sets of options.
- Lead with what the reader does, then why it works.

## Words

**One word, one meaning.** Pick a term and never rotate synonyms:

- A `TAG:` in a file is a **tag**. The Java class implementing it is a **token**.
  Never swap these. Never call either one a "field".
- A tab-separated part of a line is a **field**.
- **Load** data, **parse** a line, **resolve** a reference. Not "process".

**Never use:** simply, just, easily, obviously, of course, leverage, delve, seamless,
robust, powerful, comprehensive, rich, elegant, it's important to note, in order to,
please note, as we can see, let's dive in.

If a sentence still reads correctly after deleting a word, delete it.

**Do not oversell.** Say what the tag does. Do not say the format is elegant or the
system is powerful. Do not apologise for it either.

## Readability

Seven things make prose harder to read. Each has a cheap fix, and the fix is always
the more concrete word.

| Fault | Instead of | Write |
|---|---|---|
| Uncommon wording — rare in ordinary speech | commence the task | start the task |
| Very uncommon wording — rare in speech and in writing | ameliorate the problem | fix the problem |
| Abstract vocabulary — a quality with no object or actor | capability, governance, ownership | name the class, the file, the tag |
| Abstract sentences — abstraction carried across several sentences | the strategy establishes capability ownership | say who does what to which file |
| Noun stacks — three or more nouns compressed into one phrase | repository state mutation verification | the check that the repo did not change |
| Phrase load — several dense phrases in a short passage | two stacked phrases in one answer | one idea per sentence |
| Formulaic cues — inflated framing or filler | here's where it gets interesting | delete the sentence |

Test a sentence by asking what you could point at. If the answer is a file, a tag or
a person, it is concrete. If the answer is another abstraction, rewrite it.

## Accuracy

- Syntax comes from the token class, never from a video transcript. Transcripts are
  auto-captions and mangle tag names.
- Every material claim carries provenance. See `WIKI-SCHEMA.md`.
- If upstream behaviour is unclear, say so plainly and link the class. Do not guess.
- Examples use invented content: `Test Blade`, `Sample Feat`. Never SRD material.

## Shape of a good explanation

1. What it does, in one sentence.
2. The syntax.
3. A working example, small enough to read at a glance.
4. What breaks, and the error the reader will actually see.
5. Where to look in the code.

Skip any step that has nothing to say. Do not pad it.

## Cost

The PCGen clone is 151 MB and 6,311 `.lst` files. Rederiving a fact that is already
written down is the largest single waste on this project.

- Put settled facts in the agent's prompt. Never let an agent rediscover the pinned
  SHA, a measured count, or anything in `log.md`, `DECISIONS.md` or `tags.json`.
- One question per agent, with a cap: at most 350 words, cite `file:line`, be terse.
- Scope agents to disjoint files.
- Do cheap edits inline. Nav changes, wording, links and anything already verified
  cost less done directly than delegated.
- Verify an agent's claim with one grep before acting on it.
- Prefer an agent when the alternative is pulling large files into the main context.
