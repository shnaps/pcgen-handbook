---
name: pcgen-handbook-rules
description: How to work on the PCGen Handbook repo - terminology, provenance and citation rules, the checks that must pass before a commit, and how to scope a research agent against the PCGen source. Use when drafting, editing or reviewing any page under docs/, when citing PCGen code, when measuring usage counts, and before committing. Layers on top of the plain-writing skill, which carries the sentence and word rules.
---

# PCGen Handbook rules

**Load the `plain-writing` skill first.** It carries the sentence limits, the banned
words, the readability rules and the reply style, and they apply here unchanged. This
file adds only what is specific to PCGen and to this repo.

Readers are developers who have never touched PCGen. They want to get something
working, then understand why it worked.

## Two modes

**Strict** — reference pages, syntax, procedures, `lst/reference/`, `lst/files/`.
Every rule is enforced.

**Normal** — concept pages, internals prose, `start/`, `internals/`. Structural rules
enforced; the sentence-length cap is a target, not a hard limit.

## Terminology

One word, one meaning. These four are the ones that drift:

- A `TAG:` in a file is a **tag**. The Java class implementing it is a **token**.
  Never swap these. Never call either one a "field".
- A tab-separated part of a line is a **field**.
- **Load** data, **parse** a line, **resolve** a reference. Never "process".

The full list is in `references/glossary.md`.

## Provenance

- Syntax comes from the token class, never from a video transcript. Transcripts are
  auto-captions and mangle tag names.
- Every material claim carries a citation. The rules are in `WIKI-SCHEMA.md`, and
  `tools/lint_wiki.py` enforces them.
- Usage counts are measured by the one method pinned in `WIKI-SCHEMA.md`. Two scopes
  produce two numbers for one claim, and a number recalled rather than measured has
  been wrong three times on this project.
- Examples use invented content: `Test Blade`, `Sample Feat`. Never SRD material. The
  site is public and this keeps licence attribution off it.
- Teach the current form only. A tag in `plugin/lsttokens/deprecated/` is not it.
  Changes go to `appendix/whats-changed.md`, never into a how-to page.

## Checks

Run all four from the repo root before committing:

```text
python tools/check_style.py
python tools/lint_wiki.py
python tools/check_examples.py
python -m mkdocs build --strict
```

Fence any non-LST example as `text`. `check_examples.py` reads an untagged fence as LST
data and rejects `.pcg` or log output as unknown tags.

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
