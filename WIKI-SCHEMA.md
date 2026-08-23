# Wiki schema

What a page of each type must contain, how pages link, and how the handbook is kept
current. The style skill in `.claude/skills/lst-style/` covers *how to write a
sentence*. This covers *what a page is*.

## Three layers

1. **Raw sources** — `work/`. Gitignored, never published. Video transcripts, the
   pinned PCGen clone, `tokens.json`, `docs_tags.json`. Never hand-edited.
2. **The wiki** — `docs/`. Hand-written pages. What ships.
3. **This schema** — committed. Read it before adding a page.

## Grounded claims

Every material claim about PCGen's behaviour cites its source. A claim with no source
is a claim nobody can check, and unverifiable claims are how documentation rots.

Source of truth order:

1. The token class in `code/src/java/plugin/...` — decides what a tag does.
2. The token unit test in `code/src/test/plugin/lsttokens/...` — shows accepted and
   rejected syntax.
3. PCGen's official docs — useful for intent, not authoritative. Parts are stale.
4. The video transcripts — workflow and gotchas only. **Never syntax.** They are
   auto-captions and mangle tag names.

Where sources disagree, **the code wins**.

### Citation format

Visible, on `lst/reference/` and `internals/` pages:

```markdown
*Source: [`KeystatToken.java`](https://github.com/PCGen/pcgen/blob/<sha>/code/src/java/plugin/lsttokens/skill/KeystatToken.java)*
```

Hidden, on `start/` and narrative pages, so a beginner is not reading Java paths:

```markdown
<!-- src: code/src/java/plugin/lsttokens/skill/KeystatToken.java -->
```

`<sha>` is the pin in `PCGEN-SHA`. Both forms are machine-readable; `lint_wiki.py`
treats them identically.

## Page types

### `start/` — on-ramp

Ordered. Each page ends by naming the next one. Assumes nothing.

Required: what you will have at the end · numbered steps · what success looks like ·
what to do when it fails · link to next page.

### `lst/concepts/` — one idea

Required: what it is, in one sentence · why it exists · a small example · how it
interacts with related ideas · links to the file pages that use it.

No exhaustive tag lists. Concepts explain; reference enumerates.

### `lst/files/` — one LST file type

Required: what the file defines · minimum working line · required tags · commonly
used tags, as a table linking to reference pages · a complete worked example ·
gotchas · the loader class that reads it.

### `lst/howto/` — one task

Required: the goal in one sentence · what you need first · numbered steps · the
finished file · how to verify it loaded · common failures.

Task pages link to concept and reference pages. They never restate syntax in full.

### `lst/reference/tags/` — one tag

Required: what it does · syntax · at least one example · which file types accept it ·
deprecation status if any · source citation.

Strict mode writing. Terse. No narrative.

### `internals/` — how the code works

Required: what the component does · where it lives, with paths · how it connects to
what comes before and after · a concrete trace or example · source citations.

Diagrams welcome where they show a real mechanism. Mermaid renders natively.

## Counting shipped data

Every usage figure in the handbook is measured the same way. State nothing that was not
measured this way, because two scopes produce two numbers for one claim.

- Scope is **`data/**/*.lst`**. Not `.pcc`, unless the claim is about a `.pcc` tag, and
  then say so.
- Skip a line whose first character is `#`.
- Split the line on tabs and test `field.startswith("TAG:")`. **Never count substrings.**
  `ADD:` matches inside `DONOTADD:`, and `REMOVE:` matches inside `TYPE:.REMOVE.`.
- A subtoken figure counts the text between the tag's colon and the first `|`.

Three published figures were wrong from substring counting and two more from a mixed
`.lst` and `.pcc` scope. No tool validates a number, so the method is the only guard.

## One fact, one owner

Every material fact has exactly one page that explains it. Other pages may name the
subject and link to the owner. They may not restate the rule.

This is not a style preference. It is the failure this handbook was built to avoid,
observed inside the handbook itself: the rule for resolving two objects with the same
key was explained on five pages, and one of the five drifted into stating the opposite
of the code. Every copy is a place a fact can go stale independently, and a correct
copy looks exactly like a stale one.

| Fact | Owner |
|---|---|
| Duplicate keys resolve by `SOURCEDATE` | `lst/concepts/keys-and-names.md` |
| `datatest` skips a `.pcc` with no `SHOWINMENU` | `internals/testing.md` |
| The PCC `FEAT:` tag is deprecated | `appendix/whats-changed.md` |
| Dots in a `TYPE=` match mean and, not or | `lst/concepts/types.md` |
| `BONUS:VAR` applies only to a declared variable | `lst/concepts/declaring-variables.md` |
| Aspect names are invented by data, not validated | `lst/concepts/display-text.md` |

`tools/lint_wiki.py` checks that table and reports any other page that re-explains an
entry. Add a row when you notice a fact acquiring a second explanation.

When two pages genuinely need the same fact, the reader-facing one keeps a sentence
naming the consequence and links out. The owner keeps the rule, the citation and the
edge cases.

## Linking rules

- First mention of a tag on any page links to its reference page, if one exists.
- First mention of a concept links to its concept page.
- Every page is reachable from `docs/index.md` or from a page that is. Orphans fail
  lint.
- Never deep-link into PCGen's official docs for something this handbook covers.
  Link out only for the long tail.

## Generated content

`lst/reference/tag-index.md` is generated by `tools/gen_index.py` from
`work/tokens.json`. **Do not hand-edit it.** It carries a banner saying so.

Everything else is hand-written.

## Operations

**Ingest** — `tools/ingest.py`. Re-scan PCGen at a newer SHA, diff `tokens.json`,
write a worklist of added, removed and changed tags with the pages citing them,
append to `log.md`. Runs weekly in CI.

**Author** — write against this schema and the style skill.

**Lint** — `tools/lint_wiki.py`. Orphans, dead links, stale claims, tags in the index
with no page, pages missing required sections.

## Example content

Examples use invented content: `Test Blade`, `Sample Feat`, `Testburg`. Never SRD
feats, spells, monsters or classes. This keeps Open Game License attribution
obligations off the site entirely.
