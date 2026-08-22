# Decisions

Why this handbook is built the way it is. Recorded so the reasoning outlives the
conversation it came from.

## Source of truth is the Java code, not the docs

PCGen's official documentation has drifted from the code. Its per-tag version markers
mostly stop around 6.03. Checked against `master`:

- `ACVALUE`, `BABABBREV`, `DISPLAYVARIABLE` and `ACABBREV` are documented and **no
  longer exist**.
- `MODIFY` and `MODIFYOTHER`, from the formula system added in 6.07, **exist and are
  not documented**.

Every LST tag is a Java class declaring `getTokenName()` (the literal tag string) and
`getTokenClass()` (the object type that accepts it). Those declarations are the
specification, so `tools/scan_tokens.py` reads them directly.

Order of authority: **token class → token unit test → official docs → video
transcripts.** Where sources disagree, the code wins.

## Target is `master`, not the last release

The newest tagged release is `6.08.00RC10`, February 2023. Development continues, with
commits landing through 2026. Documenting the release would document something almost
nobody runs. Pinned commit is in `PCGEN-SHA`.

## Videos supply workflow, never syntax

The 25-video playlist is the only source that shows the actual workflow. Its captions
are auto-generated, and quality was measured across all 25: **7 uppercase tokens in
41,273 words.** Tag names are uppercase, so almost no syntax is recoverable.

How-to pages take their structure and failure modes from the videos, and every tag
from `tags.json`. `check_examples.py` enforces it.

## Shipped templates are not a reliable teacher

`data/35e/homebrew/my_homebrew/` dates from 2005 and demonstrates the deprecated PCC
`FEAT:` form. An early page followed it and had to be corrected to `ABILITY:` with
`CATEGORY:`. Verify against the token class, not the templates.

## Licence is LGPL-2.1

Matching PCGen's repository licence, so the text could be contributed upstream without
a relicensing conversation.

CC BY-SA was considered and rejected: share-alike cannot be relicensed into an
LGPL-2.1 repository, so it would have silently blocked the one thing the licence choice
was meant to keep possible.

What PCGen itself states: **program → LGPL-2.1, data → Open Game License 1.0a**. Their
*documentation* is named as neither, and carries no per-file licence notice. That
ambiguity is unresolved upstream, not merely undocumented.

Two consequences, treated as hard rules because the site is public:

1. `work/` is gitignored and never published. Transcripts are the video author's
   material, kept only as local research notes.
2. Examples use invented content (`Test Blade`, `Sample Feat`). No SRD feats, spells or
   monsters, which keeps Open Game License attribution chains off the site entirely.

## Built standalone, depending on nobody

This was attempted before. `github.com/PCGen/pcgen-docs` is a complete XHTML-to-Markdown
conversion of PCGen's documentation, built as a Hugo site with a written proposal. The
organisation accepted the repository and merged six pull requests into it. **It was
never wired into the build, never hosted, and never replaced `docs/`.** Untouched since
2017.

Meanwhile pcgen.github.io still serves the raw XHTML frameset straight off
`master:/docs` with no build step, and the DOCS tracker holds 70 open tickets with none
resolved since December 2018.

What killed that effort was not quality. It was depending on someone else to flip a
switch. So nothing here is contingent on another party acting.

Worth noting `pcgen-docs` carries no licence file at all, making its converted text
more encumbered than the main repository's, not less. It is precedent, not a source.

## If upstream ever becomes interesting

The mechanical barriers are low: no contributor licence agreement, no developer
certificate of origin, no code of conduct, no branch protection. `docs/**` is copied
verbatim into the distribution and touches no CI, so a documentation change cannot
break the build. An external documentation pull request was merged in 18 days with
three approvals. pcgen.org/contribute lists "Revise documentation" as wanted work.

Two things would need settling **in writing first**: the documentation licence scope,
and who owns the switch-over decision. That is the step `pcgen-docs` never got past.

## Operating model

Adapted from Karpathy's *LLM Wiki* pattern plus grounded claims from OpenWiki. The
machinery, not the writing style — prose stays hand-written.

Three layers: raw sources (`work/`, gitignored), the wiki (`docs/`), the schema
(`WIKI-SCHEMA.md`). Three operations: ingest, author, lint. Two records:
`docs/index.md` as the navigation contract, `log.md` as the append-only history.

The point is that PCGen's docs went stale and nobody noticed. A handbook with no
staleness mechanism becomes the next set of stale docs, so `tools/ingest.py` re-reads
upstream weekly and opens an issue when a cited tag changes.
