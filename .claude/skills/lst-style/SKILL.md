---
name: lst-style
description: Writing rules for the PCGen Handbook. Use when drafting, editing or reviewing any page under docs/. Enforces short plain sentences, active voice, consistent terminology, and the project glossary. Blocks filler and marketing words.
---

# PCGen Handbook writing style

Readers are developers who have never touched PCGen. They want to get something
working, then understand why it worked. Write for that.

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
