# PCGen Handbook

An unofficial guide to modifying PCGen. Readers are developers who have never touched
it. They want to get something working, then understand why it worked.

## Writing

Applies to every page under `docs/` and to replies in chat. Chat is not exempt.

- Lead with the answer. No preamble, no restating the question, no announcing what
  comes next.
- Sentences: 20 words for instructions, 25 for explanation. One instruction per
  sentence. No semicolons. Noun stacks of three words or fewer.
- Active voice with an explicit subject. "Open the file", not "The file should be
  opened".
- One word, one meaning. Rotating synonyms tells the reader they mean different things.
- Prefer the concrete word. If you cannot point at a file, a value or a person,
  rewrite the sentence.
- Never: simply, just, easily, obviously, leverage, delve, seamless, robust, powerful,
  comprehensive, elegant, utilize, in order to, it's important to note, at the end of
  the day, here's where it gets interesting.
- Delete any word the sentence still reads correctly without.
- Do not oversell and do not apologise. Say what the tag does.
- Report a problem as one line of fact, not a story about finding it.

Two modes. **Strict** for reference pages, syntax and procedures — `lst/reference/`,
`lst/files/` — where every rule holds. **Normal** for concept pages and internals
prose, where the sentence cap is a target.

The seven readability faults and their replacements are in the `plain-writing` skill,
which also covers writing outside this repo.

## Terminology

These four drift, so they are fixed:

- A `TAG:` in a file is a **tag**. The Java class implementing it is a **token**.
  Never swap these. Never call either one a "field".
- A tab-separated part of a line is a **field**.
- **Load** data, **parse** a line, **resolve** a reference. Never "process".

The full list is `.claude/glossary.md`.

## Provenance

- Syntax comes from the token class, never from a video transcript. Transcripts are
  auto-captions and mangle tag names.
- Every material claim carries a citation. The rules are in `WIKI-SCHEMA.md` and
  `tools/lint_wiki.py` enforces them.
- Usage counts are measured by the one method pinned in `WIKI-SCHEMA.md`. Two scopes
  produce two numbers for one claim, and a number recalled rather than measured has
  been wrong four times on this project.
- Examples use invented content: `Test Blade`, `Sample Feat`. Never SRD material. The
  site is public and this keeps licence attribution off it. `tools/check_srd.py`
  enforces this against the shipped RSRD data. Naming one shipped object to explain a
  mechanism is documentation rather than an example, and goes in that script's
  `ALLOWED` set with its reason.
- Teach the current form only. A tag in `plugin/lsttokens/deprecated/` is not it.
  Changes go to `appendix/whats-changed.md`, never into a how-to page.

## Checks

Run all five from the repo root before committing:

```text
python tools/check_style.py
python tools/lint_wiki.py
python tools/check_examples.py
python tools/check_srd.py
python -m mkdocs build --strict
```

`check_srd.py` needs the sparse clone and skips without it, as `lint_wiki.py` does.

`lint_wiki.py` also checks cross-page heading links. `mkdocs --strict` does not.

Fence any non-LST example as `text`. `check_examples.py` reads an untagged fence as
LST data and rejects `.pcg` or log output as unknown tags.

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

## Review

A structural review runs three reviewers: two on system design from different seats,
and a code expert on which parts of the PCGen source deserve documenting. They
cross-review each other, hold authority to cut or split a published page, and cite
`file:line` for every claim. Re-measure a reviewer's number before acting on it — two
have been wrong so far.

Log the result in `log.md` and move what survives to `BACKLOG.md`.
